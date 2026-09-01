---PAGE 1---
Risk Management
Assignment 5
Exposures in Counterparty Credit Risk
Politecnico di Milano — Financial Engineering
FY 2025/2026
---PAGE 2---
01
Counterparty Credit Risk
The risk isn’t the market only, it’ s your counterparty too.
Counterparty Credit Risk (CCR) is the risk that a counterparty fails to meet its contractual obligations 
before the final settlement, causing a financial loss.
---PAGE 3---
Key features of OTC markets
OTC derivatives differ from exchange traded derivatives and CCP derivatives in several aspects.
Over-the-counter derivatives   vs Exchange traded derivatives
• The trading venue is private, subject to bilateral 
negotiation.
• Highly customized contracts
• High bilateral counterparty credit risk 
• Low trade and price transparency, private deals
• Liquidity generally lower and instrument-specific
• Very high flexibility (tailored maturities and payoffs)
• Regulation traditionally lighter,increased post-crisis
• The trading venue is centralized, in the regulated 
exchange 
• Fully standardized contracts
• Very low counterparty credit risk 
• High trade and price transparency, fully public
• High liquidity for standardized instrument
• Flexibility limited 
• Strong regulatory oversight
OTC gives you freedom, at the price of the risk. Exchange gives you safety, at the price of standardization.
---PAGE 4---
Counterparty and Credit
Counterparty credit risk and credit risk are slightly different concepts
"Traditional" Credit risk - CR
It is the risk that a borrower fails to repay principal and/or interest, therefore it is typical of loans, bonds, and credit facilities.
For such products, the exposure and the potential losses, are known in advance (e.g. nominal of the loan).
Another feature is that risk is unilateral, there is a clear distinction between creditor and debtor.
The loss affects only the creditor and arises at debtor's default.
Finally, exposure usually declines over time as principal is repaid.
Credit risk is about not getting paid. CCR is about when and how much you lose.
Counterparty Credit Risk - CCR
It is the risk that a counterparty in a financial contract defaults before maturity. Given their nature, it is typical of OTC derivatives.
For those financial contracts, exposure is stochastic and time -varying.
Given the time -varying MtM of these contracts, risk is bilateral and both parties can be exposed at different times.
The loss that affect one party depends on market value at default of the other party.
Exposure can increase over time.
---PAGE 5---
02
Exposure
The core element to compute all the relevant CCR metrics
Exposure measures what is at risk when default occurs. 
It is the bridge between market value and counterparty credit risk.
---PAGE 6---
What can happen during a default
MtM is the value of the position between party B and counterparty C. MtM seen from B perspective.
1a MtM positive, C defaults
B might suffer a credit loss equal to MtM
(net of collateral).
B may then file a bankruptcy claim for 
that amount. 
1b MtM negative, C defaults
B is still required by the ISDA 
agreement to fully pay | MtM| to C.
B incurs no credit losses.
Positive MtM means exposure — B is at risk of credit losses. Negative MtM means obligation — no credit loss for B.
2a MtM positive, B defaults
C is still required by ISDA agreement 
to fully pay MtM to B.
C incurs no credit losses.
2b MtM negative, B defaults
C might suffer a credit loss equal to 
|MtM| (net of collateral).
C may then file a bankruptcy claim for 
that amount.
---PAGE 7---
The cornerstone of CCR: Exposures
Let define for now Exposure_t = MtM_t, later we will improve this
1 Positive Exposure (PE)
Exposure that represent what B may lose if counterparty C defaults at time t, in a specific scenario. 
PE(t,ω)=Max(Exposure_t(ω),0)
It is a random process.
2 Negative Exposure (NE)
Exposure that represent what C may lose if counterparty B defaults at time t, in a specific scenario. 
NE(t,ω)=Min(Exposure_t(ω),0)
It is a random process.
These are the most common definitions used in the industry. Original definitions provided in Basel are different.
---PAGE 8---
The cornerstone of CCR: Expected Exposures
We want to get rid of the stochasticity
1 Expected Positive Exposure (EPE)
Average amount that B may lose if counterparty C defaults at time t. 
EPE(t)=E[PE(t)]
It is a profile, deterministic function of time.
2 Expected Negative Exposure (ENE)
Average amount that C may lose if counterparty B defaults at time t. 
ENE(t)=E[NE(t)]
It is profile, deterministic function of time.
These are the most common definitions used in the industry. Original definitions provided in Basel are different.
---PAGE 9---
Simplified CVA and DVA
Here we are making very strong assumption to present two easy-to-read, fast-to-explain formulas
1 Credit Valuation Adjustment
The expected discounted loss due to the possible default of the counterparty, during the life of the 
deal. It reduces the risk -free MtM.
2 Debit Valuation Adjustment
The expected discounted gain due to not fully paying in case of own default, during the life of the 
deal. It increases the risk -free MtM.
CVA is the costof counterparty default risk.DVA is the benefit ofown default risk.

---PAGE 10---
Potential Future Exposure
A VaR-like measure of counterparty credit risk
PFE
It measures a severe but plausible future exposure at a given confidence level and time horizon.
• Forward-looking measure of credit exposure
• Depends on market volatility and time
• Analogous to Value at Risk ( VaR), but for exposures: it captures tail risk
This measure is used in credit limit setting, stress testing and scenario analysis. 
It is one of Basel building blocks for EAD.
PFE is how bad exposure can be.

---PAGE 11---
Peak Potential Future Exposure
A conservative scalar that summarize worst -case potential exposure
Peak-PFE
For a given confidence level, it is a scalar representing the maximum PFE over the life of the contract.
• Single scalar measure of worst -case exposure
• Used for credit limit setting and monitoring
• Conservative by construction
Given that it is a simple scalar number, this measure isused in high level reporting and for comparison across 
portfolios. It is also adopted to estimate capital requirements in stressed scenarios.
Peak-PFE is how bad the worst exposure can get.

---PAGE 12---
03
Mitigation of CCR
Regulators promote mechanisms that enhance the stability and efficiency of financial markets.
Counterparty Credit Risk can be reduced but never fully eliminated through a combination of 
contractual, operational, and market mechanisms.
---PAGE 13---
Break clauses
The first mechanism that allows to mitigate CCR: exposure and maturity cuts
Exposure_t can be truncated and assumed 0 for all t>break date
Break Clauses
A break clause is a contractual provision that grants one or both parties the right (optional) or the 
obligation (mandatory) to terminate contracts early at specified dates or upon predefined events, 
such as credit rating downgrades.
• It can be trade or counterpart specific
• It limits the time horizon over which counterparty exposure can accumulate
• Reduces PFE and peak -PFE by allowing early termination
• Prevents exposure from growing in adverse market or credit conditions
• In case it is triggered, the termination of the transaction is carried out at the prevailing MtM
Risk is transferred into different forms
CCR is mitigated, but new risks arise: moral hazard, cliff edge effect, model risk
Break clauses shorten the time horizon of exposure, thereby reducing counterparty credit risk.
---PAGE 14---
Netting Agreement
The second mechanism that allows to mitigate CCR: subadditivity. 
Exposure_t becomes the sum of all MtM_i,t of all i assets exchanged between B and C. 
Close-out Netting Agreement
A netting agreement is a legal arrangement (typically under an ISDA Master Agreement) that allows 
all outstanding transactions between two counterparties to be offset and collapsed into a single net 
amount, in the event of default.
• It applies across multiple trades and maturities
• Only the net exposure is payable or claimable at default
• Significantly reduces counterparty credit risk
• Lowers collateral requirements and regulatory capital
• Is effective only if legally enforceable
Risk is transferred into different forms
CCR is mitigated, but new risks arise: legal, systemic, concentration risks.
Netting turns many exposures into one — and credit risk drops accordingly.
---PAGE 15---
CSA Agreement
The third mechanism that allows to mitigate CCR: assets kept in a safe.
Exposures_t now becomes MtM_t – collateral_t
CSA Agreement
A Credit Support Annex (CSA) is a legal agreement that supplements the ISDA Master Agreement and 
governs the exchange of collateral between counterparties in derivative transactions in order to 
mitigate counterparty credit risk.
Its purpose is to:
• Reduce unsecured exposure arising from mark -to-market (MtM) fluctuations
• Limit losses in the event of counterparty default
• Support regulatory and risk -management requirements
Risk is transferred into different forms
CCR is mitigated, but new risks arise: liquidity, market, operational
Collateral turns promises into protection: the liquidity of todayprevents the losses of tomorrow
---PAGE 16---
CSA Key Components
Risk Management goes Legal (as it wasn't complex enough)
• Eligible assets: types of financial instruments accepted as collateral (cash, government bonds, etc...)
• Haircuts: discounts applied to non -cash or foreign-currency collateral 
• Independent Amount : a fixed amount always posted, as extra buffer and to cover closeout costs after 
default
• Variation Margin: a dynamically adjusted amount that follows MtM and reflects existing credit exposure
• Remuneration: cash collateral is remunerated at an agreed reference rate to compensate the posting party 
for funding costs
• Rating triggers:  provisions specifying adjustments to collateral requirements following a counterparty credit 
rating downgrade
• Valuation agent: the party responsible for determining the MtM used for collateral calculations, at specified 
dates and times, to ensure consistency and avoid litigation (even if disputes still happen)
---PAGE 17---
VM elements
A perfect replica of MtM can be really time and resources consuming.
Variation Margin model
To limit the operational complexity of a perfect replica of the MtM, some rules are agreed in advance 
between the parties involved.
• Margin calls are "discretized" and allowed only on certain time, e.g. daily, weekly, monthly
• Thresholds and cap, below and above which no VM is posted
• MTA, to avoid margin calls for trivial amounts
• Rounding rules, to prevent the requests of complex transfers (11 334.73 EUR vs 10 000.00 EUR)
• Margin calls are subject to cut -off time and settlement period
Everything is negotiated
All the above parameters are mutually negotiated by the two parties, and asymmetric rules may apply to each 
counterparty. How would you set up these parameters, for yourself and your counterpart, to benefit the most?
In an ideal world, VM would track MtM continuously. In the real world this is not feasible.
---PAGE 18---
04
Extended Vasicek Model
The extended V asicek model (Hull-White) is a mean-reverting short-rate model with a 
time-dependent drift that perfectly fits the initial yield curve.
You will implement a code that will simulate the dynamics of your short term rates. 
This will allow you to compute MtM_t in several scenarios and compute the relevant exposures.
---PAGE 19---
The dynamics
Ornstein–Uhlenbeck process brings back the values towards the center .
OU process
Mean reverting stochastic process, defined by the following SDE:
- a>0 is the speed of mean reversion
- sigma>0 is the volatility
- W_t is a standard Brownian motion
a and sigma are calibrated from the market
Typically from caps/floors and swaptions.
Rates wander, but always come back.

---PAGE 20---
The solution
Ornstein–Uhlenbeck solution, affine trick, boundary conditions.
Reconstruct the discount factors
Recalling the link between r_t and B(t_0,T), it can be proven that the discount factors have an affine 
form:
Forcing the boundary conditions in t_0, A and C are:

---PAGE 21---
05
Today assignment
Polimi Bank enters into a 10Y vanilla payer IRS, on 15/02/2008
Polimi Bank ask you to study the counterparty exposure embedded in this position, under different 
possible mitigation scenario.
---PAGE 22---
Task 1 - 2
Write the code to perform the MC simulation of the discount factors and derive swap MtM_t
1 Write the code to simulate r_t and the discount factors
Use the data from Lab0 and bootstrap functions.
Exploit the affine trick.
2 Compute the swap MtM at each point in the future required
At each future point in time t, in each simulation, you will have new discount factors to use to 
compute the MtM_t of the swap.
---PAGE 23---
Task 3 – 4 – 5
Evaluate the relevant exposures metrics and compare them
3 From the simulated MtM, compute the EPE profile
4 From the simulated MtM, compute the PFE profile, alpha=0.95
5 From the computed PFE, compute the Peak-PFE 
---PAGE 24---
Task 6a – 6b – 6c
Evaluate the relevant exposures metrics, under mitigation of exposures and compare with the baseline
6a Consider a 3.5y mandatory Break Clause
6b Consider the netting with a 5y vanilla receiver IRS 
6c Consider a CSA agreement, in which only the ctp posts collateral
---PAGE 25---
Task 7 - optional
CVA approximated formula
7a Compute the CVA for all the scenario (base, a, b, c)
7b For the base scenario CVA, compute 3 different sensitivities
- Comment the results
---PAGE 26---
Deliverables & Practical Notes
1 Deliver by Friday 15 May, 18:00 
to financial.engineering.polimi@gmail.com with subject "RM: Assignment5, Group #"
2 Submit a PDF with results
Include your considerations, analysis and list any errors found in the code
3 Submit the Python code
One single notebook. Comment in detail and use descriptive variable names.
4 Use bootstrap data from Lab0 – Lab1 – Lab2
Reuse your functions. If you have time, try to revise them given what you have learned!
5 Fill the gaps and correct errors
in case of incoherences between the assignment PDF and the code, follow the assignment document.
