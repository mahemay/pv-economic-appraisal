# Solar PV Project Economics: NPV, IRR, and Payback

An interactive Python model for evaluating the annual cash flows of a grid-connected solar photovoltaic project. It collects project assumptions, calculates discounted investment metrics, and produces cash-flow and NPV-sensitivity plots. The model is intended for transparent screening and educational analysis; it is not a substitute for a project-specific engineering or financial assessment.

## Repository contents

The repository version described for this README lists these files:

- `pv_payback.py` — interactive model and plotting code.
- `requirements.txt` — Python package requirements.
- `cumulative_cash_flow.png` — existing cumulative cash-flow plot.

The generated sensitivity plot is named `npv_sensitivity_heatmap.png` by the program context, but it is not confirmed in the current repository tree. It is therefore not linked as an existing image below. Generated plots only exist after the script has run; commit or upload them to the repository if they should render on the repository page.

![Cumulative cash flow](cumulative_cash_flow.png)

## Features

The interactive program requests system capacity, specific annual yield, installed investment cost, annual O&M rate, electricity price, annual generation degradation, project life, and discount rate. It builds annual generation, revenue, O&M, and net cash-flow series and reports NPV, IRR, and fractional simple and discounted payback. It also evaluates NPV over a 5 × 5 sensitivity grid for CAPEX and electricity price and plots the results.

The source visibly imports `numpy` and `matplotlib`. The current `requirements.txt` additionally lists `six` and `python-dateutil`; these are not direct imports visible in the source description and may be transitive/environment-compatibility requirements. Audit the dependency tree and remove unnecessary entries only as a separate, deliberate change to that file.

## Setup and run

Use a supported Python 3 installation. From the repository directory:

```bash
python -m pip install -r requirements.txt
python pv_payback.py
```

The program is interactive and prompts for inputs; no command-line argument interface is documented here. The source has visible defaults and validation bounds, but browser extraction of the source was incomplete. Confirm exact runtime prompts, defaults, upper bounds, and validation behavior directly in `pv_payback.py` before relying on them. Clearly visible inputs include capacity default 10 kW (minimum 0.1), specific yield 1,700 kWh/kW/year (minimum 500), installed cost 650 USD/kW (minimum 100), O&M default 1.5% (range 0–10%), electricity price 0.09 USD/kWh (minimum 0.001), degradation default 0.5% (range 0–5%), project life 20 years (minimum 1), and discount rate 8% (maximum 50%). Other upper/lower bounds should be checked against the source.

## Model conventions and equations

Let `P` denote capacity in kW, `Y` specific yield in kWh/kW/year, `C` installed cost in USD/kW, `m` annual O&M rate, `p` electricity price in USD/kWh, `d` annual degradation, `r` discount rate, and `N` project life in years. Generation degradation is compounded annually. O&M is fixed in nominal terms and based on initial CAPEX. The cash flow at time zero is the negative initial investment; annual operating cash flows occur at each year end.

```text
CAPEX = P × C
G_t = P × Y × (1 − d)^(t − 1),                         t = 1,...,N
Revenue_t = G_t × p
O&M_t = CAPEX × m
NCF_0 = −CAPEX
NCF_t = Revenue_t − O&M_t
NPV(r) = Σ[t=0..N] NCF_t / (1 + r)^t
IRR = r* such that Σ[t=0..N] NCF_t / (1 + r*)^t = 0
```

IRR is found numerically by bisection in the described program. A valid bracket/root depends on the cash-flow pattern; always assess the result in context.

Fractional payback interpolates linearly within the year in which cumulative cash flow crosses the initial investment. For undiscounted payback, let `S_(t−1) = Σ[k=1..t−1] NCF_k`; if `S_(t−1) < CAPEX` and `S_(t−1) + NCF_t ≥ CAPEX`, then:

```text
Simple payback = (t − 1) + (CAPEX − S_(t−1)) / NCF_t
```

For discounted payback, let `D_k = NCF_k / (1 + r)^k` and `Q_(t−1) = Σ[k=1..t−1] D_k`; at the first crossing of the discounted cumulative operating cash flows:

```text
Discounted payback = (t − 1) + (CAPEX − Q_(t−1)) / D_t
```

These interpolations assume a positive crossing-year cash flow and do not represent subannual production timing. If a crossing does not occur within the modeled project life, payback is not achieved during the modeled period.

## Illustrative base case

The following figures are independently calculated from the stated conventions, not asserted to be a captured run of the repository script. Inputs are 10 kW, 1,700 kWh/kW/year, 650 USD/kW, 1.5% O&M, 0.09 USD/kWh, 0.5% annual degradation, 20 years, and 8% discount rate. O&M remains fixed at 1.5% of initial CAPEX each year.

| Metric | Result |
|---|---:|
| Initial CAPEX | $6,500.00 |
| Year 1 generation | 17,000 kWh |
| Annual O&M | $97.50 |
| Year 1 net cash flow | $1,432.50 |
| NPV at 8% | $7,049.24 |
| IRR | 21.0715% |
| Simple payback (fractional) | 5.5818 years |
| Discounted payback at 8% (fractional) | 6.9519 years |

## NPV sensitivity

The grid varies CAPEX and electricity price independently by factors 0.8, 0.9, 1.0, 1.1, and 1.2 relative to the base case. Rows are CAPEX factors; columns are electricity-price factors. Generation, degradation, project life, and discount rate remain fixed. O&M is recalculated as 1.5% of scenario CAPEX, consistent with the base-case convention. Values below are NPV in USD, computed using the equations above; they are not represented as a numeric table extracted from a script run.

| CAPEX factor \ Price factor | 0.80 | 0.90 | 1.00 | 1.10 | 1.20 |
|---:|---:|---:|---:|---:|---:|
| 0.80 | 5,639.40 | 7,090.05 | 8,540.70 | 9,991.35 | 11,442.00 |
| 0.90 | 4,893.67 | 6,344.32 | 7,794.97 | 9,245.62 | 10,696.27 |
| 1.00 | 4,147.94 | 5,598.59 | 7,049.24 | 8,499.90 | 9,950.55 |
| 1.10 | 3,402.21 | 4,852.87 | 6,303.52 | 7,754.17 | 9,204.82 |
| 1.20 | 2,656.49 | 4,107.14 | 5,557.79 | 7,008.44 | 8,459.09 |

If generated and committed at the repository root, the heatmap can be displayed with `![NPV sensitivity heatmap](npv_sensitivity_heatmap.png)`. That image is not linked as a current repository asset because its presence is unconfirmed.

## Assumptions and limitations

The model uses user-supplied assumptions and illustrative defaults; no external benchmark or institutional affiliation is implied. In particular, this README makes no IRENA benchmark claim. The described source treats O&M as fixed in nominal terms and compounds annual generation degradation. Taxes, inflation, subsidies, residual value, financing structure, and time-varying electricity prices are excluded unless the implementation is separately extended. Results are sensitive to resource yield, system performance, tariff treatment, and cost assumptions; document the data source and units for each real project input.

For reproducibility, record the exact input values, Python version, package versions, and source revision alongside any reported outputs. Verify that plot generation, printed metric conventions, and edge cases (including failure to reach payback or bracket an IRR) match the actual script before publishing results.

## Implementation note

The live source text available during preparation was malformed/truncated in browser extraction and did not expose the complete validation logic or final calculation section. This README aligns with the repository details and behavior described above but does not claim that undocumented runtime behavior has been tested. Inspect `pv_payback.py` directly to confirm exact bounds, formulas, report formatting, and output paths before treating this documentation as a source-level audit.

## Author

Mohammad Akbarzadeh, PhD candidate in Resource Economics, Ferdowsi University of Mashhad. See the author's GitHub profile/repository for current contact and project information.
