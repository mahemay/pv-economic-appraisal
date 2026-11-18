# PV Economic Appraisal

[![Python](https://img.shields.io/badge/python-3.1+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](#license)

A transparent screening model for the economic appraisal of grid-connected photovoltaic (PV) systems. It estimates generation and operating cash flows and reports net present value (NPV), internal rate of return (IRR), simple payback, and discounted payback, together with a 5 × 5 NPV sensitivity analysis.

> Results are illustrative and depend on the assumptions stated below. They are not investment, engineering, or tax advice.

## Repository structure

| File | Purpose |
|---|---|
| `README.md` | Documentation, assumptions, and illustrative results |
| `pv_payback.py` | PV economic appraisal model |
| `requirements.txt` | Python package dependencies |
| `cumulative_cash_flow.png` | Cumulative cash flow figure |
| `npv_sensitivity_heatmap.png` | NPV sensitivity heatmap |

## Requirements and setup

Python 3.9 or later is required. From the repository root, install the dependencies and run the model:

```bash
python -m pip install -r requirements.txt
python pv_payback.py
```

The model is designed to accept project assumptions interactively; consult its prompts for the supported inputs and defaults.

## Methodology

Let $P$ denote installed capacity, $Y$ specific annual yield, $C$ installed cost per unit capacity, $m$ the annual O&M fraction, $p$ electricity price, $d$ annual generation degradation, $N$ project life, and $r$ the annual discount rate. Initial capital expenditure and generation in year $t$ are:

$$
\mathrm{CAPEX}=PC, \qquad G_t=PY(1-d)^{t-1}, \quad t=1,\ldots,N.
$$

Annual revenue, O&M, and operating net cash flow are:

$$
\mathrm{Revenue}_t=G_t p, \qquad M_t=m\,\mathrm{CAPEX}, \qquad \mathrm{NCF}_t=\mathrm{Revenue}_t-M_t.
$$

The initial cash flow is $\mathrm{NCF}_0=-\mathrm{CAPEX}$. With end-of-year cash flows, net present value is:

$$
\mathrm{NPV}(r)=\sum_{t=0}^{N}\frac{\mathrm{NCF}_t}{(1+r)^t}.
$$

The internal rate of return $r^*$ satisfies:

$$
0=\sum_{t=0}^{N}\frac{\mathrm{NCF}_t}{(1+r^*)^t}.
$$

Simple payback is the time at which cumulative undiscounted operating net cash flows recover initial CAPEX. Discounted payback applies the discount factor $(1+r)^{-t}$ to each annual operating net cash flow before accumulation. When recovery occurs between annual periods, payback is linearly interpolated within the crossing year. If recovery does not occur within the modeled life, payback is not achieved during the analysis period.

## Illustrative base case

| Metric | Illustrative value |
|---|---:|
| Installed capacity | 10 kW |
| Initial CAPEX | $6,500.00 |
| First-year generation | 17,000 kWh |
| Annual O&M | $97.50 |
| Simple payback | 4.58 years |
| Discounted payback | 5.95 years |
| NPV | $7,049.24 |
| IRR | 21.07% |

These values are an illustrative reference case. NPV and discounted payback use an 8% annual discount rate. Use the model with project-specific, documented inputs for decision-making.

## NPV sensitivity analysis

The matrix varies CAPEX and electricity price by multipliers from 0.80 to 1.20 in 0.10 increments. Rows are CAPEX multipliers and columns are price multipliers. All other assumptions are held constant; scenario O&M is calculated as 1.5% of scenario CAPEX. Values are NPV in USD.

| CAPEX multiplier / Price multiplier | 0.80 | 0.90 | 1.00 | 1.10 | 1.20 |
|---:|---:|---:|---:|---:|---:|
| **0.80** | $5,639.40 | $7,090.05 | $8,540.70 | $9,991.35 | $11,442.00 |
| **0.90** | $4,893.67 | $6,344.32 | $7,794.97 | $9,245.62 | $10,696.27 |
| **1.00** | $4,147.94 | $5,598.59 | **$7,049.24** | $8,499.90 | $9,950.55 |
| **1.10** | $3,402.21 | $4,852.87 | $6,303.52 | $7,754.17 | $9,204.82 |
| **1.20** | $2,656.49 | $4,107.14 | $5,557.79 | $7,008.44 | $8,459.09 |

## Figures

![Cumulative cash flow](cumulative_cash_flow.png)

*Figure 1. Cumulative cash flow over the modeled project life.*

![NPV sensitivity heatmap](npv_sensitivity_heatmap.png)

*Figure 2. NPV sensitivity to installed CAPEX and electricity price.*

## Assumptions and limitations

- Annual generation declines at a constant compounded degradation rate.
- O&M is modeled as a fixed nominal annual amount derived from a fraction of initial CAPEX; no inflation escalation is applied.
- Cash flows are annual and assumed to occur at year-end.
- Taxes, inflation, subsidies, financing structure, replacement costs, and residual value are excluded.
- The sensitivity analysis varies only CAPEX and electricity price. It does not quantify uncertainty in yield, degradation, operating costs, or other inputs.
- IRR may be ambiguous or unavailable for some cash-flow profiles; interpret it together with NPV and the underlying assumptions.

The analysis is a simplified appraisal, not a full project-finance model. Input provenance, units, currency, and reference date should be documented for any applied study.

## Author

**Mohammad Akbarzadeh**  
Ph.D. Candidate in Resource Economics  
Ferdowsi University of Mashhad

## License

This project is released under the MIT License. See the repository's `LICENSE` file for the complete terms.
