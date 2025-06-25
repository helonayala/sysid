# Linear Systems

In this section, we explore two different types of estimation:

## Batch Least Squares (BLS)

A common model for identification and simulation in discrete-time is the AutoRegressive with eXogenous inputs (ARX) model, which is linear in its parameters. The difference equation for the ARX model is

$$y(k) = -a_1y(k-1) - \ldots - a_{na}y(t-na) + b_1u(k-1) + \ldots + b_{nb}u(t-nb) + \xi (k)$$

This can be expressed in a compact matrix form:

$$\pmb y = \Phi \pmb \theta + \pmb \xi$$ 

The components of this equation are defined as follows:

* **Regression Vector**: A column vector containing past values of the system's input and output. It has a dimension of $na+nb$, where $na$ and $nb$ are the model orders.

    $$
    \phi(k) = \begin{bmatrix}
    -y(k-1) &
    \dots &
    -y(k-na) &
    u(k-1) &
    \dots &
    u(k-nb)
    \end{bmatrix}^\intercal
    $$
  
* **Vector of Model Parameters**: A column vector containing the model coefficients to be estimated.

    $$
    \pmb \theta = \begin{bmatrix}
    a_1 & \dots & a_{na} & b_1 & \dots & b_{nb}
    \end{bmatrix}^\intercal
    $$

* **Regression Matrix**: A matrix constructed by stacking the transposed regression vectors, $\phi^\intercal(k)$, for a series of measurements. Assuming $N$ total measurements are available, the matrix is formed for time steps from $p$ to $N$, where $p=1+\max(na,nb)$.

    $$
    \Phi = \begin{bmatrix}
    \phi^\intercal(p) \\
    \phi^\intercal(p+1) \\
    \vdots \\
    \phi^\intercal(N)
    \end{bmatrix}
    =
    \begin{bmatrix}
    -y(p-1) & \ldots & -y(p-na) & u(p-1) & \ldots & u(p-nb) \\
    -y(p) & \ldots & -y(p+1-na) & u(p) & \ldots & u(p+1-nb) \\
    \vdots & \vdots & \vdots & \vdots & \vdots & \vdots \\
    -y(N-1) & \ldots & -y(N-na) & u(N-1) & \ldots & u(N-nb)
    \end{bmatrix}
    $$

* **Measurement and Error Vectors**: The target measurement vector $\pmb y$ and error vector $\pmb \xi$ are given respectively by:

    $$
    \pmb y = \begin{bmatrix}
    y(p) \\ y(p+1) \\ \vdots \\ y(N)
    \end{bmatrix},
    \pmb \xi = \begin{bmatrix}
    \xi(p) \\ \xi(p+1) \\ \vdots \\ \xi(N)
    \end{bmatrix}
    $$

The Batch Least Squares algorithm finds the estimated parameter vector $\hat{\pmb \theta}$ that solves the optimization problem. The solution is given by:

$$\hat{\pmb \theta} = \left[ \Phi^\intercal \Phi \right]^{-1}\Phi^\intercal \pmb y$$ 

This can be demonstrated by solving the least squares problem of the error. The condition for the solution to exist is that $\left[ \Phi^\intercal \Phi \right]$ is positive definite.

## Recursive Least Squares (RLS)

The RLS algorithm updates the parameter estimates at each time step as new data becomes available. The algorithm proceeds as follows, starting with initial values for $P(0)$ and $\hat{ \theta}(0)$:

1.  **Measure** current input/output of the system: $y(k),u(k)$.
2.  **Update** the regression vector, $\phi(k+1)$, using the new measurements.
3.  **Calculate** the prediction error: $e(k+1) = y(k+1) - \phi^\intercal(t+1)\hat{ \theta}(k)$.
4.  **Calculate** the estimator gain: $K(k+1) = \dfrac{P(k)\phi(k+1)}{1+\phi^\intercal(k+1)P(k)\phi(k+1)}$.
5.  **Update** the estimated parameters: $\hat{  \theta}(k+1) = \hat{ \theta}(k) + K(k+1)e(k+1)$.
6.  **Update** the covariance matrix: $P(k+1) = P(k) - K(k+1)\left[ P(k) \phi(k+1) \right]^\intercal$.

**Tuning:**
* **Initial Parameters**: If no prior information is available, $\hat{ \theta}(0)$ can be initialized with small values.
* **Initial Covariance Matrix**: This matrix reflects the confidence in the initial parameter estimates. If initial estimates are poor, $P(0)$ should be initialized with high values on its main diagonal. A common practice is to set $P(0) = mI$, where $I$ is the identity matrix and $m$ is a large number (e.g., greater than $10^{3}$). As the estimation improves, the elements of $P(k)$ and the estimator gain $K(k)$ tend to zero, leading to $\hat{ \theta}(k+1) \approx \hat{ \theta}(k) $.

Covariance resetting, or other strategies like forgetting factor, but not only, can be used to adapt RLS to model tive-variant systems.
