# Activity

Repeat, for the "ball and hoop" bench, the whole pipeline already carried out for the
[ball and beam](https://helonayala.github.io/sysid/mpc_ball_and_beam.html):

* Identify a **NARX model** from the bench data, using the same testing protocol as before
  (estimate on one dataset, validate in free run on the others). Report R² and RMSE.
* Write the identified model as a **state-space model** and build the **MPC** (multiple shooting),
  with the input bounded to the motor range. Report the solve time per step and compare it with
  the sampling period.
* Approximate the MPC with a **neural network**, as in the ball and beam example.
* Run the network in **real time on the dSpace** bench and compare the measured run against the
  simulation.

*Tip:* the network is what makes the sampling period achievable — the solver does not fit in it.
