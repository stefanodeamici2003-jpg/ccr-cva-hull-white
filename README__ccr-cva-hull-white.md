# Counterparty Credit Risk and CVA under Hull-White

Risk Management lab (MSc Mathematical Engineering, Politecnico di Milano, 2025/26). Python.

## Problem

A bank holds a EUR 100M 10-year payer interest rate swap against a single counterparty. If that counterparty defaults while the swap is worth something to the bank, the bank loses it. Pricing that loss requires the whole distribution of the swap's future value, not just its value today, and the answer changes with every risk mitigant in the contract: an early termination right, a netting agreement covering a second trade, a collateral annex.

## Approach

- Short rate simulated as a Hull-White process, written as an Ornstein-Uhlenbeck component plus a deterministic shift, with 250,000 paths on a 40-date grid over ten years.
- Zero-coupon bonds rebuilt at each simulation date through the affine formula `P(t,T) = A(t,T) exp(-C(t,T) x_t)`, so the swap is repriced in closed form along every path with no nested simulation.
- Expected positive exposure and 95% potential future exposure computed at each date for five configurations: standalone swap, mandatory break clause at 3y6m, a second 5-year EUR 150M receiver swap with and without netting, and full collateralisation under a CSA with zero threshold and zero minimum transfer amount.
- Unilateral CVA on each configuration under a flat 200 bp hazard rate and 60% LGD, plus sensitivities to the hazard rate, to a parallel shift of the curve and to the Hull-White volatility, all bumped by 1 bp on the same random seed.

## Results

The uncollateralised swap carries a CVA of about EUR 252k on EUR 100M of notional. Each mitigant cuts into it: the break clause at 3y6m brings it down to EUR 106k by truncating the exposure profile, and netting the second swap into the same set brings the pair from EUR 324k to EUR 165k, roughly half. Collateralisation is the strongest by a wide margin, leaving EUR 22k, about a tenth of the base case.

The sensitivities say where the number actually comes from. A basis point on the hazard rate moves the CVA by EUR 1.2k, while a basis point on the curve moves it by EUR -32k and a basis point on the Hull-White volatility by EUR -41k. The charge is an order of magnitude more exposed to the rate environment and to the volatility used to simulate it than to the credit quality of the counterparty.

## Running it

```bash
pip install numpy pandas matplotlib jupyter
jupyter lab ex5_notebook.ipynb
```

The notebook bootstraps the curve from the market data in `data/`, then runs the simulation end to end. Seeded, so the sensitivities are reproducible.
