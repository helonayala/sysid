# Activities - BLS

This activity builds upon the batch least squares system identification example. 

You will enhance the existing code by creating reusable functions and applying the methodology to real-world data.

1. Improve the baseline code (using the simulated dataset)

a.  **Implement a Regression Matrix Function:**
    *   Create a Python function that takes the input time series data (`u`), the output time series data (`y`), and the model orders ($n_a$ for the autoregressive part and $n_b$ for the exogenous part) as arguments.
    *   This function should construct and return two arguments: the regression matrix $\Phi$ and the output vector $Y$ (which represents the target outputs for the model).
    *   The function should handle the initial conditions appropriately, considering the maximum delay ($max(n_a, n_b)$).
    *   For each time step $k$ from $max(n_a, n_b)$ up to the end of the data, create a row in the regression matrix $\Phi$. This row should contain the values `[-y(k-1), -y(k-2), ..., -y(k-na), u(k-1), u(k-2), ..., u(k-nb)]`. The corresponding value in the output vector $Y$ should be `y(k)`.
    *   Ensure the dimensions of $\Phi$ and $Y$ are consistent with the number of data points used after accounting for initial conditions.
    *   Improve the "Identification" section of the notebook by calling this new function with the training data to obtain `Phi_TRA` and `y_target_TRA`, and with the test data to obtain `Phi_TEST` and `y_target_TEST`.
    *   *Tip:* Consider a function like `matReg` in https://github.com/helonayala/narx_narendra/blob/main/narendra.ipynb.

b.  **Implement a Free-Run Simulation Function:**

    *   Create a Python function that performs a free-run simulation of the identified model. This function should take the estimated parameter vector ($\hat{\theta}$), the input signal for simulation, and the initial conditions for the simulation as arguments.

    *   The free-run simulation means that future output values are calculated based on the previously simulated output values, not the measured data.

    *   The initial conditions for the simulation (the first $max(n_a, n_b)$ output values) should be taken from the measured data used for identification.

    *   Within the function, for each time step $k$ after the initial conditions, construct the regression vector using the *simulated* past outputs and the current or past *input* values from the provided input signal. Use the function you created in step 1 to build these individual regression vectors.

    *   Calculate the predicted output for time step $k$ by multiplying the regression vector at time $k$ by the estimated parameter vector $\hat{\theta}$.

    *   *Tip:* Consider a function like `freeRun` in https://github.com/helonayala/narx_narendra/blob/main/narendra.ipynb.

c. **Generate metrics for evaluating predictions (both in OSA and FR)**

    *  Evaluate the model predictions using $RMSE$ and $R^2$ (check sklearn implementations for those functions)

    * Compare the spectrum of the measured signal, the predictions (OSA and FR), and the errors (OSA and FR). Compare the spectrum of the best and the worst models in terms of $R^2$.

2.  Apply to Real-World Data:
    
a. Substitute the synthetic data generated in the notebook with the dataset you'll use for your project. You may choose an example from the case studies section too. Ask the insctructor if unsure.

b. Try increasing model orders and compare the outcome (tables / figures). Check if it is possible to improve the error metrics in free-run simulation.

