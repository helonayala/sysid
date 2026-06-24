#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/helonayala/sysid/blob/main/phys_14_drone.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Physics-based model
# 
# Nonlinear, physics-based **continuous-time state-space** model of the 1/4 drone, with state `x = [theta, theta_dot]` (angle, angular velocity).
# 
# From Euler-Lagrange (see the *1/4 drone Lagrangian* example) the rotary arm obeys `J*theta_ddot = -m g l * sin(theta) - b*theta_dot + tau_motor`. The motor is a propeller: thrust grows with the **square of the propeller speed**, and the command `u` is (approximately) proportional to that speed, so the motor torque is **proportional to `u^2`**. Lumping the constants gives the identifiable form
# 
# $$\ddot\theta = c_1\,\sin\theta + c_2\,u^2 + c_3\,\dot\theta$$
# 
# - `c1 sin(theta)` : gravity restoring torque / inertia
# - `c2 u^2`        : propeller thrust / inertia (motor force ~ u^2)
# - `c3 theta_dot`  : viscous friction / inertia (linear in velocity)
# 
# The three parameters are identified from data **two ways** — `scipy.optimize.least_squares` and a **Neural-ODE-style** PyTorch fit (`torchdiffeq` + Adam) — both minimizing the short-rollout simulation error, using the same train/test protocol as the NARX/NODE models.

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from scipy.signal import savgol_filter
from scipy.optimize import least_squares

try:
    from torchdiffeq import odeint
except ImportError:
    get_ipython().system('pip install -q torchdiffeq')
    from torchdiffeq import odeint
try:
    from sysid import readData
except ImportError:
    get_ipython().system('pip install -q git+https://github.com/helonayala/sysid.git')
    from sysid import readData

torch.manual_seed(0); np.random.seed(0)
Ts = 0.05; L = 20; d2r = np.pi / 180.0


# ## Load and preprocess
# 
# Same selection as the other 1/4 drone models: slice 20-80 s, decimate by 5. The angle is converted to radians and the velocity is estimated with a Savitzky-Golay filter.

# In[2]:


T_START, T_END, DECIMATION = 20.0, 80.0, 5
SG_WIN, SG_POLY = 11, 3

def load_processed(name):
    y, u, t, ref = readData('quarter_drone', name, return_ref=True)
    idx = np.where((t >= T_START) & (t <= T_END))[0]
    sl = slice(idx[0], idx[-1] + 1, DECIMATION)
    theta_deg = y[sl].astype(float)
    th = theta_deg * d2r
    return dict(u=u[sl].astype(float), th=th, theta_deg=theta_deg,
                thd=savgol_filter(th, SG_WIN, SG_POLY, deriv=1, delta=Ts),
                t=t[sl].astype(float))

data = {n: load_processed(n) for n in ['multiseno', 'degraus', 'swept_sine']}


# ## Semi-static check: motor force ~ u^2
# 
# On the slow (semi-static) experiment, holding a larger angle needs more motor force. Plotting `u` vs angle gives a parabola, and `u^2` is (nearly) linear in `sin(theta)` — i.e. the propeller thrust `~ u^2` balances the gravity torque `~ sin(theta)`.

# In[3]:


ss = load_processed('semi_estatica')
fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 4))
a1.scatter(ss['theta_deg'], ss['u'], s=5, alpha=0.4)
a1.set_xlabel('angle y [deg]'); a1.set_ylabel('u [%]')
a1.set_title('Semi-static: u vs angle (parabola)'); a1.grid(True)
a2.scatter(np.sin(ss['th']), ss['u'] ** 2, s=5, alpha=0.4)
a2.set_xlabel('sin(theta)'); a2.set_ylabel('u^2')
r = np.corrcoef(ss['u'] ** 2, np.sin(ss['th']))[0, 1]
a2.set_title(f'u^2 vs sin(theta)   (corr = {r:.3f})'); a2.grid(True)
plt.tight_layout(); plt.show()


# ## Train / test split and rollout windows
# 
# `multisine` and `steps`: 80% train / 20% test; `swept sine`: test only. Short rollouts (length 20) are extracted from the pooled training portions.

# In[4]:


TRAIN_FRAC = 0.8
def split(name, frac=TRAIN_FRAC):
    d = data[name]; k = int(len(d['th']) * frac)
    return ({x: v[:k] for x, v in d.items()}, {x: v[k:] for x, v in d.items()})

mult_tr, mult_te = split('multiseno')
step_tr, step_te = split('degraus')
train_segs = [mult_tr, step_tr]

def make_windows(seg, L=L):
    th, thd, u = seg['th'], seg['thd'], seg['u']
    TH0, THD0, US, TG = [], [], [], []
    for i in range(len(th) - L):
        TH0.append(th[i]); THD0.append(thd[i]); US.append(u[i:i+L]); TG.append(th[i:i+L])
    return map(np.array, (TH0, THD0, US, TG))

TH0, THD0, US, TG = [], [], [], []
for seg in train_segs:
    a, b, c, d = make_windows(seg)
    TH0.append(a); THD0.append(b); US.append(c); TG.append(d)
TH0 = np.concatenate(TH0); THD0 = np.concatenate(THD0)
US = np.concatenate(US); TG = np.concatenate(TG)
print(f'Training windows: {len(TH0)}  (rollout length L={L})')


# ## Continuous model, integrator and equation-error initialization
# 
# `theta_ddot = c1 sin(theta) + c2 u^2 + c3 theta_dot`, integrated with fixed-step RK4 (ZOH input). The parameters are first initialized by linear least squares on the acceleration (equation error).

# In[5]:


def accel(th, thd, u, p):
    return p[0] * np.sin(th) + p[1] * u ** 2 + p[2] * thd

def rk4_rollout(th0, thd0, useq, p):
    """Fixed-step RK4 with ZOH input. Vectorized over windows; returns theta(.,L)."""
    th = np.array(th0, float); thd = np.array(thd0, float); out = [np.array(th)]
    for k in range(useq.shape[-1] - 1):
        u = useq[..., k]
        f = lambda a, b: (b, accel(a, b, u, p))
        k1 = f(th, thd)
        k2 = f(th + Ts/2*k1[0], thd + Ts/2*k1[1])
        k3 = f(th + Ts/2*k2[0], thd + Ts/2*k2[1])
        k4 = f(th + Ts*k3[0], thd + Ts*k3[1])
        th = th + Ts/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0])
        thd = thd + Ts/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        out.append(np.array(th))
    return np.stack(out, -1)

# equation-error LS init: theta_ddot ~ [sin(theta), u^2, theta_dot]
sa = np.concatenate([s['th'] for s in train_segs])
ua = np.concatenate([s['u'] for s in train_segs])
da = np.concatenate([s['thd'] for s in train_segs])
Phi = np.column_stack([np.sin(sa), ua ** 2, da])
ddot = np.concatenate([savgol_filter(s['th'], SG_WIN, SG_POLY, deriv=2, delta=Ts) for s in train_segs])
p_init, *_ = np.linalg.lstsq(Phi, ddot, rcond=None)
print('equation-error init [c1, c2, c3] =', np.round(p_init, 6))


# ## Version A - scipy.optimize.least_squares (simulation error)
# 
# Refine the parameters by minimizing the 20-sample rollout residuals (Levenberg-Marquardt), starting from the equation-error estimate.

# In[6]:


res = least_squares(
    lambda p: (rk4_rollout(TH0, THD0, US, p) - TG).ravel(),
    p_init, method='lm', max_nfev=400)
p_scipy = res.x
print('scipy.least_squares params [c1, c2, c3] =', np.round(p_scipy, 6))


