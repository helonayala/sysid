# Activities - RLS

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

