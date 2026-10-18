# Counterparty Credit Risk and CVA under Hull-White

Risk Management lab (MSc Mathematical Engineering, Politecnico di Milano, 2025/26).

## Problem

A bank holds a EUR 100M 10-year payer swap against a single counterparty. A default while the swap is in the money means a loss, and pricing it requires the whole distribution of the swap's future value. The answer shifts with every mitigant in the contract: an early termination right, a netting agreement, a collateral annex.

## Approach

- Short rate simulated as a Hull-White process (Ornstein-Uhlenbeck component plus a deterministic shift), with 250,000 paths on a 40-date grid over ten years.
- Zero-coupon bonds rebuilt at each simulation date through the affine formula `P(t,T) = A(t,T) exp(-C(t,T) x_t)`, so the swap is repriced in closed form along every path.
- Expected positive exposure and 95% potential future exposure computed at each date for six configurations: standalone swap, break clause at 3y6m, a 5-year EUR 150M receiver swap (standalone, no netting, netting), and full collateralisation under a zero-threshold, zero-MTA CSA.
- Unilateral CVA on each configuration under a flat 200 bp hazard rate and 60% LGD, plus sensitivities to hazard rate, curve and Hull-White volatility, all at +1 bp on the same seed.

## Results

The uncollateralised swap carries a CVA of about EUR 252k on EUR 100M of notional. Each mitigant cuts into it: the break clause at 3y6m brings it down to EUR 106k by truncating the exposure profile; netting the second swap in brings the pair from EUR 324k to EUR 165k, roughly half; collateralisation is the strongest, leaving EUR 22k, about a tenth of the base case.

The sensitivities say where the number actually comes from. A basis point on the hazard rate moves the CVA by EUR 1.2k, on the curve by EUR 1.9k, on the Hull-White volatility by EUR 2.8k. All three are positive: the CVA is a positive-weighted sum of expected positive exposures, each a call option on the swap's mark-to-market with zero strike, so a higher rate level, a wider simulated distribution and a higher default probability all push it up. The charge is about twice as sensitive to the rate environment and to the simulated volatility as to the credit quality of the counterparty.

## Running it

```bash
pip install numpy pandas matplotlib scipy jupyter
jupyter lab ex5_notebook.ipynb
