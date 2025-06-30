# Activity List

## 1. Linear Model
* Build a grey-box model for the "ball and hoop" dataset, using the same testing prococol as before.
* Start with the linear viscous friction case, which is analogous to the DC motor example with synthetic data.
* The result you be very similar to what you obtained in the ARX activity. The overall fitting will not be good for the whole operating envelope due to nonlinearities inherent to the system.

---

## 2. Introduce Nonlinearity
Incorporate additional terms to account for nonlinearity. Consider the following options:

### Option A: Polynomial Friction Model
* Implement a polynomial model for nonlinear friction with the following form:

$$ f_f(\omega) = \theta_0 + \theta_1\omega + \theta_2\omega^2 + \dots $$

where $f_f(\omega)$ is the nonlinear viscous friction torque opposing the driving torque.

### Option B: Neural Network Friction Model
* Use a neural network to model the remaining friction terms:

$$ f_f(\omega) = F(\omega) $$

where $F(.)$ represents the nonlinear neural network mapping velocity ($\omega$) to friction-related energy losses.

---

### Implementation Note
**Important:** These models are defined **within** the state-space equations. You must modify the relevant state-space equation in the example to implement them alongside the other system parameters.
