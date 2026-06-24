"""
narx_frols
==========

Polynomial NARX system identification with Forward Regression Orthogonal
Least Squares (FROLS) term selection.

This module encapsulates the methods used throughout the SYSID notes so they
can be reused with a single import:

    from narx_frols import regMatARX, regMatNARX, frols_py, NARX

Term selection is controlled by ``n_components``: the number of model terms
(regressors) to select, instead of an ERR threshold.
"""

import numpy as np
from itertools import combinations_with_replacement
from tqdm.auto import tqdm  # tqdm.auto selects the best bar for console/notebook


# --- Function: regMatARX ---
def regMatARX(y_signal_in,
              u_signal_in,
              ny: int,
              nu: int):
    """
    Creates the initial ARX regression matrix and the target vector y(k).
    AR (y-lag) terms are NOT negated.

    Args:
        y_signal_in (array-like): Output data vector.
        u_signal_in (array-like): Input data vector.
        ny (int): Number of past y lags (autoregressive order).
        nu (int): Number of past u lags (exogenous input order).

    Returns:
        P0_data (np.ndarray): The ARX regressor matrix. Shape (NP, ny + nu).
        P0_colnames (list): Column names for P0_data.
        y_target (np.ndarray): The target vector y(k). Shape (NP,).
    """
    if not isinstance(y_signal_in, np.ndarray):
        y_signal = np.array(y_signal_in, dtype=float)
    else:
        y_signal = y_signal_in.astype(float)

    if not isinstance(u_signal_in, np.ndarray):
        u_signal = np.array(u_signal_in, dtype=float)
    else:
        u_signal = u_signal_in.astype(float)

    if len(y_signal) != len(u_signal):
        raise ValueError("Input signals y_signal and u_signal must have the same length.")
    if ny < 0 or nu < 0:
        raise ValueError("Lags ny and nu must be non-negative.")

    N_total_samples = len(y_signal)

    max_lag = 0
    if ny > 0: max_lag = max(max_lag, ny)
    if nu > 0: max_lag = max(max_lag, nu)

    y_target = y_signal[max_lag:]
    num_effective_rows = len(y_target)

    P0_colnames = []
    if ny > 0: P0_colnames.extend([f'y(k-{i})' for i in range(1, ny + 1)])
    if nu > 0: P0_colnames.extend([f'u(k-{i})' for i in range(1, nu + 1)])
    num_P0_cols = len(P0_colnames)

    if num_effective_rows == 0:
        return np.empty((0, num_P0_cols), dtype=float), P0_colnames, np.empty((0,), dtype=float)

    P0_rows_list = []
    for k_target_idx in range(max_lag, N_total_samples):
        current_regressor_row = []
        for j_lag_idx in range(1, ny + 1):
            current_regressor_row.append(y_signal[k_target_idx - j_lag_idx])
        for j_lag_idx in range(1, nu + 1):
            current_regressor_row.append(u_signal[k_target_idx - j_lag_idx])
        P0_rows_list.append(current_regressor_row)
    P0_data = np.array(P0_rows_list, dtype=float)
    return P0_data, P0_colnames, y_target


# --- Function: regMatNARX ---
def regMatNARX(u_signal_in,
               y_signal_in,
               nu: int,
               ny: int,
               poly_order_l: int):
    """
    Generates the full candidate regression matrix for a NARX model
    and the corresponding target vector y(k).
    """
    if not isinstance(y_signal_in, np.ndarray): y_signal = np.array(y_signal_in, dtype=float)
    else: y_signal = y_signal_in.astype(float)
    if not isinstance(u_signal_in, np.ndarray): u_signal = np.array(u_signal_in, dtype=float)
    else: u_signal = u_signal_in.astype(float)

    if len(y_signal) != len(u_signal): raise ValueError("Signals must have same length.")
    if ny < 0 or nu < 0: raise ValueError("Lags must be non-negative.")
    if poly_order_l < 1: raise ValueError("Polynomial order l must be at least 1.")

    P0_data, P0_colnames, y_target = regMatARX(y_signal, u_signal, ny, nu)
    NP = len(y_target)  # Number of effective rows (can be 0)

    if NP > 0:
        P_columns_list = [np.ones((NP, 1), dtype=float)]  # Constant term
    else:
        P_columns_list = [np.empty((0, 1), dtype=float)]  # Constant term for 0 rows

    P_final_colnames = ['constant']
    P_columns_list.append(P0_data)
    P_final_colnames.extend(P0_colnames)
    num_P0_base_regressors = P0_data.shape[1]

    if poly_order_l >= 2 and num_P0_base_regressors > 0:
        for current_poly_order in range(2, poly_order_l + 1):
            for col_indices_tuple in combinations_with_replacement(range(num_P0_base_regressors), current_poly_order):
                term_name = "".join([P0_colnames[i] for i in col_indices_tuple])
                P_final_colnames.append(term_name)
                if NP > 0:  # Only compute values if there are rows
                    selected_P0_cols = P0_data[:, list(col_indices_tuple)]
                    new_poly_term_col = np.prod(selected_P0_cols, axis=1, keepdims=True)
                    P_columns_list.append(new_poly_term_col)

    if NP == 0:  # If no rows, return an empty matrix with the correct number of total columns
        total_cols = len(P_final_colnames)
        P_final_data = np.empty((0, total_cols), dtype=float)
    else:  # NP > 0
        P_final_data = np.concatenate(P_columns_list, axis=1)

    return P_final_data, P_final_colnames, y_target


# --- Function: frols_py ---
def frols_py(P_regressors, Y_target_in, n_components, P_colnames=None, epsilon=1e-12):
    """
    Forward Regression Orthogonal Least Squares (FROLS) for model term
    selection and parameter estimation.

    Args:
        P_regressors (np.ndarray): Candidate regressor matrix, shape (NP, M).
        Y_target_in (np.ndarray): Target vector y(k).
        n_components (int): Number of model terms to select. Capped at the
            number of available candidate regressors.
        P_colnames (list, optional): Names of the candidate regressors.
        epsilon (float): Numerical tolerance.

    Returns:
        dict with keys: 'th', 'Psel_data', 'Psel_colnames', 'g', 'W', 'A',
        'ERR_values', 'selected_indices'.
    """
    if Y_target_in.ndim == 1:
        Y_target = Y_target_in.reshape(-1, 1)
    else:
        Y_target = Y_target_in

    M = P_regressors.shape[1]
    NP = P_regressors.shape[0]
    empty_result = {
        'th': np.array([]), 'Psel_data': np.empty((NP, 0)), 'Psel_colnames': [],
        'g': np.array([]), 'W': np.empty((NP, 0)), 'A': np.empty((0, 0)),
        'ERR_values': np.array([]), 'selected_indices': []}
    if NP == 0 or M == 0:
        return empty_result

    if not isinstance(n_components, (int, np.integer)) or n_components <= 0:
        raise ValueError("n_components must be a positive integer.")
    num_terms_to_select = min(int(n_components), M)

    sig_yy_val = (Y_target.T @ Y_target).item()
    if sig_yy_val < epsilon: sig_yy_val = epsilon

    selected_terms_indices = []; err_selected_list = []; g_selected_list = []
    Q_orthogonal_bases = np.empty((NP, 0)); A_matrix = np.empty((0, 0))
    M0 = 0

    for s_term_iter in range(M):
        current_ERRs = np.full(M, -np.inf); current_gs = np.zeros(M)
        current_Qs_storage = np.zeros((NP, M))

        if s_term_iter == 0:
            for m_idx in range(M):
                p_m = P_regressors[:, m_idx:m_idx+1]; p_m_norm_sq = (p_m.T @ p_m).item()
                if p_m_norm_sq >= epsilon:
                    current_Qs_storage[:, m_idx] = p_m.flatten()
                    current_gs[m_idx] = (Y_target.T @ p_m).item() / p_m_norm_sq
                    current_ERRs[m_idx] = (current_gs[m_idx]**2 * p_m_norm_sq) / sig_yy_val
        else:
            for m_idx in range(M):
                if m_idx in selected_terms_indices: continue
                p_m = P_regressors[:, m_idx:m_idx+1]; q_m_orth = p_m.copy()
                for r_q_idx in range(M0):
                    q_r = Q_orthogonal_bases[:, r_q_idx:r_q_idx+1]; q_r_norm_sq = (q_r.T @ q_r).item()
                    alpha_mr = 0.0
                    if q_r_norm_sq >= epsilon: alpha_mr = (p_m.T @ q_r).item() / q_r_norm_sq
                    q_m_orth -= alpha_mr * q_r
                current_Qs_storage[:, m_idx] = q_m_orth.flatten()
                q_m_orth_norm_sq = (q_m_orth.T @ q_m_orth).item()
                if q_m_orth_norm_sq >= epsilon:
                    current_gs[m_idx] = (Y_target.T @ q_m_orth).item() / q_m_orth_norm_sq
                    current_ERRs[m_idx] = (current_gs[m_idx]**2 * q_m_orth_norm_sq) / sig_yy_val

        if np.all(np.isneginf(current_ERRs)): break
        newly_selected_idx = np.argmax(current_ERRs)
        selected_terms_indices.append(newly_selected_idx)
        err_selected_list.append(current_ERRs[newly_selected_idx])
        g_selected_list.append(current_gs[newly_selected_idx])
        Q_selected_term = current_Qs_storage[:, newly_selected_idx:newly_selected_idx+1]
        Q_orthogonal_bases = Q_selected_term if Q_orthogonal_bases.shape[1] == 0 else np.hstack((Q_orthogonal_bases, Q_selected_term))

        p_orig_new_sel = P_regressors[:, newly_selected_idx:newly_selected_idx+1]
        if M0 == 0:
            A_matrix = np.array([[1.0]])
        else:
            A_new_col = np.zeros((M0, 1))
            for r_A_idx in range(M0):
                q_r_for_A = Q_orthogonal_bases[:, r_A_idx:r_A_idx+1]
                q_r_for_A_norm_sq = (q_r_for_A.T @ q_r_for_A).item()
                if q_r_for_A_norm_sq >= epsilon:
                    A_new_col[r_A_idx, 0] = (p_orig_new_sel.T @ q_r_for_A).item() / q_r_for_A_norm_sq
            A_matrix = np.block([[A_matrix, A_new_col], [np.zeros((1, M0)), np.array([[1.0]])]])
        M0 += 1

        # Stopping criterion: stop once n_components terms have been selected.
        if M0 >= num_terms_to_select:
            break

    if M0 == 0:
        return empty_result
    A_final = A_matrix; g_final = np.array(g_selected_list).reshape(-1, 1)
    theta_FROLS = np.linalg.solve(A_final, g_final) if A_final.size > 0 and A_final.shape[0] == A_final.shape[1] else np.array([])
    if theta_FROLS.size == 0 and A_final.size > 0:  # If solve failed or matrix not square
        try:
            theta_FROLS = np.linalg.pinv(A_final) @ g_final
        except Exception:
            theta_FROLS = np.array([])

    P_sel_data = P_regressors[:, selected_terms_indices]
    P_sel_colnames = [P_colnames[i] for i in selected_terms_indices] if P_colnames else []
    return {'th': theta_FROLS.flatten(), 'Psel_data': P_sel_data, 'Psel_colnames': P_sel_colnames,
            'g': g_final.flatten(), 'W': Q_orthogonal_bases, 'A': A_final,
            'ERR_values': np.array(err_selected_list).flatten(), 'selected_indices': selected_terms_indices}


# --- Class: NARX ---
class NARX:
    def __init__(self, nu: int, ny: int, poly_order_l: int, n_components: int = 5):
        self.nu = nu
        self.ny = ny
        self.poly_order_l = poly_order_l
        self.n_components = n_components  # Number of model terms to select via FROLS

        self.theta_ = None
        self.selected_P_colnames_ = None
        self.selected_indices_ = None
        self.P_candidate_colnames_ = None

        self._P0_colnames_base_ = []
        if self.ny > 0: self._P0_colnames_base_.extend([f'y(k-{i})' for i in range(1, self.ny + 1)])
        if self.nu > 0: self._P0_colnames_base_.extend([f'u(k-{i})' for i in range(1, self.nu + 1)])
        self._num_P0_base_regressors_ = len(self._P0_colnames_base_)
        self._max_lag_internal_ = max(self.ny, self.nu) if self.ny > 0 or self.nu > 0 else 0
        self.fit_results_ = None

    def fit(self, u, y=None):
        """Identify the NARX model (structure selection + parameter estimation).

        Two input forms are accepted:

        * Single dataset:   ``fit(u, y)`` with array-like ``u`` and ``y``.
        * Multiple datasets: ``fit(data)`` where ``data`` is a list of
          ``(u_i, y_i)`` pairs. Each dataset's regression matrix is built
          independently (so no regressors cross dataset boundaries) and the
          rows are stacked, so FROLS selects the structure and estimates the
          parameters jointly over all datasets.
        """
        if y is not None:
            datasets = [(u, y)]
        else:
            datasets = list(u)  # list of (u_i, y_i) pairs

        P_blocks, Y_blocks = [], []
        colnames = None
        for u_i, y_i in datasets:
            u_i = np.asarray(u_i, dtype=float)
            y_i = np.asarray(y_i, dtype=float)
            P_i, colnames, y_i_target = regMatNARX(
                u_i, y_i, self.nu, self.ny, self.poly_order_l
            )
            if P_i.shape[0] == 0:
                continue  # dataset shorter than the model lags; skip it
            P_blocks.append(P_i)
            Y_blocks.append(y_i_target)

        if not P_blocks:
            raise ValueError(
                "No usable data: every dataset is shorter than the model lags."
            )

        P_cand_matrix = np.vstack(P_blocks)
        y_target_train = np.concatenate(Y_blocks)
        self.P_candidate_colnames_ = colnames

        frols_results = frols_py(
            P_cand_matrix, y_target_train, self.n_components, self.P_candidate_colnames_
        )

        self.theta_ = frols_results['th']
        self.selected_P_colnames_ = frols_results['Psel_colnames']
        self.selected_indices_ = frols_results['selected_indices']
        self.fit_results_ = frols_results

        if self.theta_ is None or len(self.theta_) == 0:
            print("Warning: FROLS did not select any terms or failed to estimate parameters.")
        return self

    def print(self):
        """Print a summary of the fitted model: selected terms, parameters (theta)
        and Error Reduction Ratio (ERR) per term."""
        if self.theta_ is None or len(self.theta_) == 0:
            print("No terms were selected by FROLS, or fitting failed.")
            return
        err = self.fit_results_['ERR_values']
        print("=" * 55)
        print("NARX model — selected terms and parameters")
        print("=" * 55)
        print(f"Max lag: {self._max_lag_internal_}  "
              f"(ny={self.ny}, nu={self.nu}, l={self.poly_order_l})")
        print(f"{'#':<4} {'Term':<30} {'theta':>10}  {'ERR (%)':>10}")
        print("-" * 55)
        for i, term in enumerate(self.selected_P_colnames_):
            err_pct = err[i] * 100 if i < err.size else float('nan')
            print(f"{i + 1:<4} {term:<30} {self.theta_[i]:>10.4f}  {err_pct:>10.6f}")
        print("-" * 55)
        print(f"{'Total ERR explained:':<35} {np.sum(err) * 100:>10.6f}%")

    def _form_single_candidate_row_values(self, current_y_lags_list, current_u_lags_list):
        current_P0_values = []
        if self.ny > 0: current_P0_values.extend(current_y_lags_list)
        if self.nu > 0: current_P0_values.extend(current_u_lags_list)

        all_terms_this_row_dict = {'constant': 1.0}
        for i in range(self._num_P0_base_regressors_):
            all_terms_this_row_dict[self._P0_colnames_base_[i]] = current_P0_values[i]

        if self.poly_order_l >= 2 and self._num_P0_base_regressors_ > 0:
            for current_order_poly in range(2, self.poly_order_l + 1):
                for p0_indices_tuple in combinations_with_replacement(range(self._num_P0_base_regressors_), current_order_poly):
                    term_name = "".join([self._P0_colnames_base_[j] for j in p0_indices_tuple])
                    term_val = np.prod([current_P0_values[j] for j in p0_indices_tuple])
                    all_terms_this_row_dict[term_name] = term_val

        full_candidate_row_ordered_list = []
        if self.P_candidate_colnames_ is None:
            raise RuntimeError("P_candidate_colnames_ not set. Model might not be fitted correctly.")

        for name in self.P_candidate_colnames_:
            val = all_terms_this_row_dict.get(name)
            if val is None:
                print(f"Warning: Term '{name}' not found in generated row dict for FR prediction. Using 0.0. This may indicate an issue.")
                full_candidate_row_ordered_list.append(0.0)
            else:
                full_candidate_row_ordered_list.append(val)
        return np.array(full_candidate_row_ordered_list)

    def predict(self, u_inputs, y_history_for_lags_or_osa=None, mode='OSA'):
        if self.theta_ is None or len(self.theta_) == 0:
            raise RuntimeError("Model has not been fitted or no terms were selected. Call fit() first.")

        u_inputs_np = np.asarray(u_inputs, dtype=float)
        if y_history_for_lags_or_osa is not None:
            y_hist_np = np.asarray(y_history_for_lags_or_osa, dtype=float)

        if mode == 'OSA':
            if y_history_for_lags_or_osa is None:
                raise ValueError("For OSA prediction, y_history_for_lags_or_osa (actual y values) must be provided.")

            P_osa_full, P_osa_full_colnames, y_target_osa = regMatNARX(
                u_inputs_np, y_hist_np, self.nu, self.ny, self.poly_order_l
            )

            if P_osa_full.shape[0] == 0:
                return np.array([]), y_target_osa

            if list(P_osa_full_colnames) != list(self.P_candidate_colnames_):
                print("Warning: OSA prediction column names differ from training. This might lead to issues if order varies subtly.")

            P_selected_osa = P_osa_full[:, self.selected_indices_]
            y_hat_osa = P_selected_osa @ self.theta_
            return y_hat_osa, y_target_osa

        elif mode == 'FR':
            if y_history_for_lags_or_osa is None:
                raise ValueError("For FR simulation, y_history_for_lags_or_osa (initial y conditions) must be provided.")

            y_initial_conditions = y_hist_np

            if len(y_initial_conditions) < self._max_lag_internal_:
                raise ValueError(f"Not enough initial y conditions for FR. Need {self._max_lag_internal_}, got {len(y_initial_conditions)}")

            num_total_timeline_points = len(u_inputs_np)
            if num_total_timeline_points < self._max_lag_internal_ and self._max_lag_internal_ > 0:
                print("Warning: u_inputs not long enough for FR simulation start. Returning empty.")
                return np.array([])

            y_hat_fr_full = np.zeros(num_total_timeline_points)

            if self._max_lag_internal_ > 0:
                y_hat_fr_full[:self._max_lag_internal_] = y_initial_conditions[:self._max_lag_internal_]

            simulation_range = range(self._max_lag_internal_, num_total_timeline_points)
            num_sim_steps = num_total_timeline_points - self._max_lag_internal_

            print(f"Starting Free-Run Simulation for {num_sim_steps} steps...")
            for k_pred_idx in tqdm(simulation_range, desc="FR Simulation", unit="step", total=num_sim_steps):
                current_y_lags = []
                if self.ny > 0:
                    current_y_lags = [y_hat_fr_full[k_pred_idx - j] for j in range(1, self.ny + 1)]

                current_u_lags = []
                if self.nu > 0:
                    current_u_lags = [u_inputs_np[k_pred_idx - j] for j in range(1, self.nu + 1)]

                full_candidate_row = self._form_single_candidate_row_values(current_y_lags, current_u_lags)
                selected_regressors_for_row = full_candidate_row[self.selected_indices_]

                y_hat_fr_full[k_pred_idx] = selected_regressors_for_row @ self.theta_

            return y_hat_fr_full[self._max_lag_internal_:]
        else:
            raise ValueError(f"Unknown prediction mode: {mode}. Choose 'OSA' or 'FR'.")
