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

### Implementation Note
**Important:** These models are defined **within** the state-space equations. You must modify the relevant state-space equation in the example to implement them alongside the other system parameters.

---

## 3. 1/4 Drone Case Study

* Inspect measured data in the respective case study section;
* Obtain the state-space equations for the [1/4 drone](https://helonayala.github.io/sysid/lagrange_quarter_drone.html) using the provided script;
* Refer to [this presentation](docs/references_quarter_drone.pptx) for the angle and energy terms used in the script;
* Identify the physics-related parameters from the closed-loop data using the provided [multiple-shooting code](https://helonayala.github.io/sysid/multiple_shooting.html);
* **Recursive Least Squares (RLS) Follow-up Activity:**
  * Discretize the nonlinear system to estimate the appropriate model orders.
  * Using the input-output data (u: motor %; y: angular deflection), apply RLS to estimate the parameters of a standard linear model, treating them as time-varying. Because linearization results in a Linear Time-Varying (LTV) system dependent on the operating envelope, estimate the *a* and *b* coefficients and observe how they change with respect to the angular position (the output).
  * Next, use the nonlinear model directly. Adapt the [RLS code](https://helonayala.github.io/sysid/recursive_least_squares.html)—specifically the regression vector—to recursively estimate the physical parameters of the system.
 

