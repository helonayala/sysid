# NARMAX Activity List

1.  **ARX Model Term Selection (OLS)**
    * Using the [Orthogonal Least Squares (OLS) code](https://helonayala.github.io/sysid/orthogonal_least_squares.html), select the most relevant terms for the ARX model you built previously for the ball and hoop case study.
    * Your selection must be based on the Error Reduction Ratio (ERR) metric.
    * Perform all test routines and compare with previous results.

2.  **NARX Model Construction (FROLS)**
    * Build a NARX model for the "ball and hoop" dataset.
    * You must use the Forward Regression Orthogonal Least Squares (FROLS) algorithm provided in [this example](https://helonayala.github.io/sysid/NARX_FROLS_Model.html).

3.  **NARMAX Model Extension (Extended FROLS)**
    * Extend the [FROLS implementation](https://helonayala.github.io/sysid/NARX_FROLS_Model.html) to build a NARMAX model.
    * This is a two-step process: first, implement the base NARX model using FROLS, and then incorporate noise terms to create the full NARMAX model. 
