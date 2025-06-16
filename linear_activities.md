# Activities

## BLS

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

## RLS

This project focuses on applying **Recursive Least Squares (RLS)** methods to estimate parameters of time-varying systems. You'll work wit real-world datasets, analyzing how model parameters change over time and in response to system variations.

1. Ball and Hoop System Estimation

For this task, you'll revisit the ball and hoop system from the Batch Least Squares exercise, but this time using a **sequential estimation** approach.

* Use the uniform step dataset for estimation.
* **Compare parameter changes with Batch Least Squares.** After each step, verify if the estimated parameter changes align with the results you obtained using Batch Least Squares, segmenting the datasets accordingly. Use the batch least squares to compare the results in the cell "Plot output: real vs estimated parameters"

2. LTV System Estimation from IFAC SYSID 2015 Benchmark

You'll work with a real-world dataset from the IFAC SYSID 2015 benchmark session to estimate a **Linear Time-Varying (LTV)** system.

* **Review the benchmark paper and data.**
    * Read the paper [here](https://www.sciencedirect.com/science/article/pii/S2405896315029663)
    * Access the measured data [here](https://www.kth.se/social/group/system-identificatio/page/17th-ifac-symposium-on-system-identifica/)
* **Select and prepare your dataset.** Choose one dataset that features a **ramp scheduling signal**. Treat the system as LTV, assuming the scheduling signal is **not** directly available for estimation.
* **Generate RLS results for time-varying processes.** Apply RLS to estimate the system parameters over time.
* **Document and visualize your findings.**
    * **Describe your numerical experiments** in detail.
    * **Summarize the results in a table**, comparing different RLS configurations or performance metrics.
    * **Present clear graphs** showing the predictions and model parameters over time for your chosen best-performing RLS configuration.
* **Tip:** Figure 2 in the paper provides transfer function information that can help you define appropriate **model orders ($n_a, n_b$)**.

3. LTV System Estimation for Wind Blade Crack Detection

This task involves reproducing and analyzing results from a paper on damage detection in a small-scale wind turbine blade using black-box system identification.

* **Reproduce paper results.**
    * Access the paper [here](https://github.com/helonayala/sysid/blob/a641f018fde1875bc7d9565cc4e79bed934a4a56/docs/ICEAF%207th%20Small-scale%20WT%20blade%20black%20box%20SysID.pdf)
    * Refer to Sections 2, 3, and 4 in the paper [here](https://onlinelibrary.wiley.com/doi/full/10.1002/stc.2660)) for detailed descriptions.
* **Understand the provided data.** You'll be working with input/output data for two cases: the **nominal case (R)** and the **worst crack case (L)**, both at 0 degrees Celsius. The excitation signal is a white noise filtered force waveform. Input data `u(t)` files have the suffix `exgn`, and output data `y(t)` files have the suffix `acln`. Each column in `acln` corresponds to a different accelerometer; for simplicity, **choose only one accelerometer** to analyze.
* **Tips for your analysis:**
    * **Determine optimal model orders ($n_a, n_b$).** Using your existing code from the previous delivery, identify `na` and `nb` values that provide a good fit for both the nominal (R) and cracked (L) datasets.
    * **Apply consistent model orders for RLS.** Use the same `na` and `nb` values for your RLS estimation.
    * **Implement covariance resetting.** Apply RLS with any covariance resetting strategy for the **concatenated dataset** (nominal followed by cracked data).
    * **Analyze parameter behavior.** Observe how the model parameters $\theta$ change over time and specifically how they are influenced by the presence of cracks in the structure. What insights can you draw from these changes?

