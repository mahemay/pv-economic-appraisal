# Photovoltaic (PV) Economic Appraisal Model

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

An interactive and transparent Python model for evaluating the financial performance of small-scale photovoltaic (PV) power plants. 

The model incorporates baseline parameters from **IRENA 2026 Renewable Cost Reports** and provides financial evaluation including **Simple & Discounted Payback Periods**, **Net Present Value (NPV)**, **Internal Rate of Return (IRR)**, an **Annual Cash-Flow Schedule**, and a **2D Sensitivity Matrix** comparing CAPEX against Electricity Tariff variations.

---

## Key Features

- **Interactive Shell with Validation:** Dynamic prompt input allowing custom parameter overrides while maintaining validated input boundaries.
- **Fractional Payback Calculation:** Precise time-to-recovery calculations (e.g., 4.58 years instead of rounded integers).
- **Core Financial Decision Indicators:** Automatic computation of Net Present Value (NPV) and Internal Rate of Return (IRR) with explicit decision rules.
- **Robust Sensitivity Framework:** 5×5 sensitivity matrix evaluating NPV dynamics under multi-variable trade-offs (CAPEX ±20% vs. Electricity Price ±20%).
- **Dual Visual Outputs:** Auto-generated publication-ready charts (`cumulative_cash_flow.png` and `npv_sensitivity_heatmap.png`).

---

## Model Inputs & Assumptions (IRENA 2026 Base Case)

| Parameter | Unit | Base Value | Reasonable Range | Description |
| :--- | :---: | :---: | :---: | :--- |
| **System Capacity** | kW | `10.0` | 0.1 – 100,000 | Total installed capacity |
| **Specific Yield** | kWh/kW/yr | `1,700` | 500 – 3,000 | Annual generation yield per installed kW |
| **CAPEX Rate** | USD/kW | `650` | 100 – 10,000 | Unit capital expenditure |
| **O&M Share** | % of CAPEX | `1.5%` | 0.0% – 10.0% | Annual operation & maintenance cost |
| **Electricity Price** | USD/kWh | `0.09` | 0.001 – 2.0 | Revenue tariff rate per kWh generated |
| **Degradation Rate** | % / year | `0.5%` | 0.0% – 5.0% | Annual efficiency losses of PV panels |
| **Project Lifetime** | Years | `20` | 1 – 50 | Technical operating timeline |
| **Discount Rate (WACC)**| % | `8.0%` | 0.0% – 50.0% | Discount factor for cash-flow appraisal |

---

## Output Metrics & Base-Case Results

Running the model with standard IRENA benchmark assumptions yields the following financial performance metrics:
```text
====================================================================
BASE-CASE RESULTS
====================================================================
System capacity                  : 10.00 kW
Initial investment               : $6,500.00
Annual O&M cost                  : $97.50
First-year electricity generation: 17,000 kWh
Lifetime electricity generation  : 324,324 kWh
Lifetime undiscounted revenue     : $29,189.19
Lifetime undiscounted O&M cost    : $1,950.00
Simple payback period            : 4.58 years
Discounted payback period        : 5.95 years
Net present value (NPV)           : $7,049.24
Internal rate of return (IRR)     : 21.07%
NPV decision                     : Financially acceptable
IRR decision                     : IRR exceeds WACC
====================================================================
