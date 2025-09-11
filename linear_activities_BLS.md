# Activities - BLS

This activity builds upon the batch least squares system identification example. You will enhance the existing code by creating reusable functions and applying the methodology to real-world data.

1.  **Implement a Regression Matrix Function:**
    *   Create a Python function that takes the input time series data (`u`), the output time series data (`y`), and the model orders ($n_a$ for the autoregressive part and $n_b$ for the exogenous part) as arguments.
    *   This function should construct and return two arguments: the regression matrix $\Phi$ and the output vector $Y$ (which represents the target outputs for the model).
    *   The function should handle the initial conditions appropriately, considering the maximum delay ($max(n_a, n_b)$).
    *   For each time step $k$ from $max(n_a, n_b)$ up to the end of the data, create a row in the regression matrix $\Phi$. This row should contain the values `[-y(k-1), -y(k-2), ..., -y(k-na), u(k-1), u(k-2), ..., u(k-nb)]`. The corresponding value in the output vector $Y$ should be `y(k)`.
    *   Ensure the dimensions of $\Phi$ and $Y$ are consistent with the number of data points used after accounting for initial conditions.
    *   Improve the "Identification" section of the notebook by calling this new function with the training data to obtain `Phi_TRA` and `y_target_TRA`, and with the test data to obtain `Phi_TEST` and `y_target_TEST`.
    *   *Tip:* Consider a function like `matReg` in https://github.com/helonayala/narx_narendra/blob/main/narendra.ipynb.

2.  **Implement a Free-Run Simulation Function:**

    *   Create a Python function that performs a free-run simulation of the identified model. This function should take the estimated parameter vector ($\hat{\theta}$), the input signal for simulation, and the initial conditions for the simulation as arguments.

    *   The free-run simulation means that future output values are calculated based on the previously simulated output values, not the measured data.

    *   The initial conditions for the simulation (the first $max(n_a, n_b)$ output values) should be taken from the measured data used for identification.

    *   Within the function, for each time step $k$ after the initial conditions, construct the regression vector using the *simulated* past outputs and the current or past *input* values from the provided input signal. Use the function you created in step 1 to build these individual regression vectors.

    *   Calculate the predicted output for time step $k$ by multiplying the regression vector at time $k$ by the estimated parameter vector $\hat{\theta}$.

    *   *Tip:* Consider a function like `freeRun` in https://github.com/helonayala/narx_narendra/blob/main/narendra.ipynb.

3. **Generate metrics for evaluating predictions (both in OSA and FR)**

    *  Evaluate the model predictions using $RMSE$ and $R^2$ (check sklearn implementations for those functions)

    * Compare the spectrum of the measured signal, the predictions (OSA and FR), and the errors (OSA and FR). Compare the spectrum of the best and the worst models in terms of $R^2$.

4.  **Apply to Real-World Data (Coupled Drives Data):**
    *   Substitute the synthetic data generated in the notebook with the provided coupled drives data.
    *   **Part a: Linearity Assessment:**
        *   Use the data from the random steps experiment as your training data.
        *   Use the data from the increasing/decreasing sequence of steps experiment as your test data.
        *   Plot the predictions in free-run for training and test data against measured data. Based on the plot, assess whether a single linear model adequately represents the system behavior across different operating points (steps).

    *   **Part b: Segmented Linear Models:**
        *   Focus solely on the increasing/decreasing sequence of steps data for this part.
        *   Try to obtain a separate linear model for each distinct operating envelope within this dataset (e.g., one model for each constant step level). You will need to segment the data accordingly.
        *   Evaluate how well each individual linear model performs in predicting the output within its specific operating segment. You can plot the measured output for each segment against its corresponding free-run simulation.
