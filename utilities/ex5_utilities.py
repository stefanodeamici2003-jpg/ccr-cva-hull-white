"""
Mathematical Engineering - Financial Engineering, FY 2025-2026
Risk Management - Exercise 5: Utilities for HW Monte Carlo CCR
"""

import numpy as np
import pandas as pd
import datetime as dt
from typing import Tuple, List
from scipy.integrate import quad

from utilities.ex0_utilities import (
    get_discount_factor_by_zero_rates_linear_interp,
    year_frac_act_x,
    year_frac_30e_360,
)

from utilities.ex1_utilities import swap_par_rate


# ---------------------------------------------------------------------------
# OU (Hull-White) simulation of the state variable x_t
# ---------------------------------------------------------------------------

def simulate_ou_process(
    simulation_grid,
    today,
    mean_reversion: float,
    sigma: float,
    n_sim: int,
    x0: float = 0.0,
) -> np.ndarray:
    """Simulate x_t under the OU dynamics (Hull-White extended Vasicek)."""
    n_steps = len(simulation_grid)
    Z = np.random.standard_normal((n_sim, n_steps))

    x_paths = np.zeros((n_sim, n_steps))
    x_prev = np.full(n_sim, x0)

    for i, sim_date in enumerate(simulation_grid):
        prev_date = today if i == 0 else simulation_grid[i - 1]
        dt = year_frac_act_x(prev_date, sim_date, 360)

        mean = x_prev * np.exp(-mean_reversion * dt)
        var = (sigma ** 2 / (2 * mean_reversion)) * (1 - np.exp(-2 * mean_reversion * dt))
        x_current = mean + np.sqrt(var) * Z[:, i]

        x_paths[:, i] = x_current
        x_prev = x_current

    return x_paths


# ---------------------------------------------------------------------------
# Affine trick: B(t,T) = A(t,T) * exp(-C(t,T) * x_t)
# ---------------------------------------------------------------------------

def affine_trick(
    valuation_date,
    pricing_grid: List,
    mean_reversion: float,
    sigma: float,
    discount_factors: pd.Series,
) -> Tuple[pd.Series, pd.Series]:
    """
    Compute A(t, T) and C(t, T) such that:
        B(t, T) = A(t, T) * exp(-C(t, T) * x_t)
    with (Hull-White / extended Vasicek):
        A(t, T) = [B(0,T) / B(0,t)] * exp(-0.5 * ∫_0^t [σ(u,T)^2 - σ(u,t)^2] du)
        C(t, T) = (1 - exp(-a(T-t))) / a
    """
    reference_date = discount_factors.index[0].to_pydatetime()

    A = pd.Series(index=pricing_grid, dtype=float)
    C = pd.Series(index=pricing_grid, dtype=float)

    # Ensure the curve covers the whole pricing grid
    needed_dates = pd.DatetimeIndex(list(pricing_grid) + [valuation_date]).unique()
    missing_dates = [d for d in needed_dates if d not in discount_factors.index]
    if missing_dates:
        interp_vals = [
            get_discount_factor_by_zero_rates_linear_interp(
                reference_date, d, discount_factors.index, discount_factors.values
            )
            for d in missing_dates
        ]
        interpolated_dfs = pd.Series(index=missing_dates, data=interp_vals)
        discount_factors = (
            pd.concat([discount_factors, interpolated_dfs]).sort_index()
        )

    sigma_func = lambda u, T: (sigma / mean_reversion) * (
        1 - np.exp(-mean_reversion * (T - u))
    )

    for T in pricing_grid:
        if T <= valuation_date:
            A[T] = 1.0
            C[T] = 0.0
            continue

        tau_t_T = year_frac_act_x(valuation_date, T, 360)
        tau_0_T = year_frac_act_x(reference_date, T, 360)
        tau_0_t = year_frac_act_x(reference_date, valuation_date, 360)

        integral, _ = quad(
            lambda u: sigma_func(u, tau_0_T) ** 2 - sigma_func(u, tau_0_t) ** 2,
            0,
            tau_0_t,
        )
        A[T] = (
            discount_factors.loc[T] / discount_factors.loc[valuation_date]
        ) * np.exp(-0.5 * integral)
        C[T] = (1 - np.exp(-mean_reversion * tau_t_T)) / mean_reversion

    return A, C


# ---------------------------------------------------------------------------
# Collateral (CSA) update under simplified assumptions
# ---------------------------------------------------------------------------

def update_collateral(
    mtm: np.ndarray,
    VM: np.ndarray,
    THR_B: float = 0.0,
    THR_C: float = 0.0,
    MTA_B: float = 0.0,
    MTA_C: float = 0.0,
    Cap_B: float = np.inf,
    Cap_C: float = np.inf,
) -> np.ndarray:
    """
    Update the variation margin at a single time step under a bilateral CSA.
    Target VM*:
        max(MtM - THR_C, 0)   if MtM >= 0
        min(MtM + THR_B, 0)   if MtM <  0
    """
    VM_star = np.where(
        mtm >= 0,
        np.maximum(mtm - THR_C, 0.0),
        np.minimum(mtm + THR_B, 0.0),
    )

    delta_VM = VM_star - VM

    margin_call = np.where(
        delta_VM >= 0,
        np.where(delta_VM >= MTA_C, delta_VM, 0.0),
        np.where(np.abs(delta_VM) >= MTA_B, delta_VM, 0.0),
    )

    VM_no_cap = VM + margin_call

    VM_updated = np.where(
        VM_no_cap >= 0,
        np.minimum(VM_no_cap, Cap_C),
        np.maximum(VM_no_cap, -Cap_B),
    )

    return VM_updated


# ---------------------------------------------------------------------------
# EPE for the base 10y payer swap — corrected for sensitivity analysis
# ---------------------------------------------------------------------------

def compute_epe_base(
    discount_factors_input,
    sigma_input,
    simulation_grid,
    x_paths,
    fixed_leg_payment_dates,
    notional,
    mean_reversion,
    swap_rate_fixed,
):
    """
    Recompute the EPE profile for the base 10y payer swap using a possibly
    bumped discount curve and/or sigma.  `x_paths` is passed explicitly so
    the caller controls the random scenario set (same seed → same increments).

    Fixes applied vs. previous version
    ----------------------------------
    1) MtM at date t_i must include only FUTURE cash flows (strictly after t_i),
       i.e. cf[i+1:]  (bug-fix: was cf[i:], which double-counted the coupon
       paid at t_i and systematically collapsed EPE on payment dates).
    2) At the very last simulation date, MtM is set to 0 (no future cash flows).
    3) The fixed contractual rate does NOT change under curve/σ bumps: only
       the discounting changes.
    """
    n_dates = len(simulation_grid)
    epe = np.zeros(n_dates)

    # Fixed-leg cash flows (fixed coupon + notional at maturity)
    cf = pd.Series(
        data=[
            swap_rate_fixed
            * year_frac_30e_360(
                fixed_leg_payment_dates[k - 1], fixed_leg_payment_dates[k]
            )
            for k in range(1, len(fixed_leg_payment_dates))
        ],
        index=fixed_leg_payment_dates[1:],
    )
    cf.iloc[-1] += 1.0  # notional reimbursement at maturity
    cf_ext = cf.reindex(simulation_grid, fill_value=0.0)

    for i, sim_date in enumerate(simulation_grid):
        x_t = x_paths[:, i]

        A, C = affine_trick(
            sim_date,
            simulation_grid,
            mean_reversion,
            sigma_input,
            discount_factors_input,
        )

        # B(sim_date, T_j) for all j
        df_hw = A.values[np.newaxis, :] * np.exp(-np.outer(x_t, C.values))

        if i == n_dates - 1:
            mtf = np.zeros(len(x_t))
        else:
            dcf = df_hw[:, i + 1:] @ cf_ext.values[i + 1:]
            mtf = notional * (1.0 - dcf)

        epe[i] = np.mean(np.maximum(mtf, 0.0))

    return epe


# ---------------------------------------------------------------------------
# CVA via discrete integral
# ---------------------------------------------------------------------------

def compute_cva(
    epe_array,
    lambda_input,
    discount_factors_input,
    simulation_grid,
    settlement_date,
    lgd,
):
    """
    Discrete CVA integral (independence between exposure and default):

        CVA = Σ_i  LGD · EPE_i · B(0, t_i) · [S(t_{i-1}) - S(t_i)]
        S(t) = exp(-λ t)
    """
    cva = 0.0
    for i, sim_date in enumerate(simulation_grid):
        prev_date = settlement_date if i == 0 else simulation_grid[i - 1]

        t_prev = year_frac_act_x(settlement_date, prev_date, 360)
        t_curr = year_frac_act_x(settlement_date, sim_date, 360)

        marginal_pd = np.exp(-lambda_input * t_prev) - np.exp(-lambda_input * t_curr)

        df_t = get_discount_factor_by_zero_rates_linear_interp(
            settlement_date,
            sim_date,
            discount_factors_input.index,
            discount_factors_input.values,
        )

        cva += lgd * epe_array[i] * df_t * marginal_pd

    return cva