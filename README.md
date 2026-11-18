# PV Economic Appraisal

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

A robust, transparent, and reproducible Python model designed to evaluate the economic and financial performance of small-scale photovoltaic (PV) power plants. 

Developed as part of research in **Energy Economics and Renewable Energy Systems**, this repository demonstrates practical techno-economic modeling—bridging engineering yields with financial appraisal metrics.

---

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Key Economic & Technical Metrics](#key-economic--technical-metrics)
- [Model Assumptions (IRENA Benchmarks)](#model-assumptions-irena-benchmarks)
- [Methodology & Key Features](#methodology--key-features)
- [Project Structure](#project-structure)
- [Installation & Usage](#installation--usage)
- [Results & Visualization](#results--visualization)
- [Author](#author)

---

## 💡 Project Overview
Investing in renewable energy requires rigorous financial appraisal under uncertainty. This tool models the complete cash flow lifecycle of a grid-connected photovoltaic system over a 20-year horizon. It explicitly accounts for panel degradation, operation and maintenance (O&M) expenses, and the time value of money via discounted cash flow (DCF) analysis.

---

## 📊 Key Economic & Technical Metrics
For a standard **10 kW** rooftop/small-scale commercial PV installation, the model computes:
- **Initial Investment:** $6,500
- **Annual Generation (Year 1):** 17,000 kWh
- **Simple Payback Period:** 5 Years
- **Discounted Payback Period:** 6 Years

---

## ⚙️ Model Assumptions (IRENA Benchmarks)
The baseline parameters reflect recent global cost trends for solar PV (aligned with IRENA reports):

| Parameter | Value | Unit | Description |
| :--- | :---: | :---: | :--- |
| **System Capacity** | 10 | kW | Installed peak capacity |
| **Specific Yield** | 1,700 | kWh/kW/year | Annual energy output per kW |
| **Investment Cost** | 650 | USD/kW | Total installed capital cost |
| **Annual O&M Cost** | 1.5% | % of CAPEX | Operation and maintenance share |
| **Electricity Price** | 0.09 | USD/kWh | Tariff / Feed-in rate |
| **Degradation Rate** | 0.5% | %/year | Annual efficiency loss |
| **Project Lifetime** | 20 | Years | Operational horizon |
| **Discount Rate** | 8.0% | % | Weighted Average Cost of Capital (WACC) |

---

## 🛠️ Methodology & Key Features
- **Degradation Modeling:** Applies compounding annual efficiency loss: $Y_t = Y_1 \times (1 - d)^{t-1}$
- **Cash Flow Generation:** Computes annual net revenues (Gross Revenue minus O&M).
- **Time Value of Money:** Evaluates both nominal (simple) and present-value (discounted) cumulative cash flows.
- **Payback Identification:** Programmatically determines exact cost-recovery milestones.

---

## 📂 Project Structure
```text
pv-economic-appraisal/
│
├── pv_payback.py               # Main economic model and plotting script
├── requirements.txt            # Required Python libraries
├── cumulative_cash_flow.png    # Generated cash flow trajectory chart
└── README.md                   # Project documentation
