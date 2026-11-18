# PV Economic Appraisal

A transparent Python model for evaluating the economic performance of a small-scale photovoltaic power plant.

## Objective

This project estimates the annual generation, revenues, operating costs, cash flows, and payback period of a small-scale PV project.

The model also compares simple cash flow with discounted cash flow in order to demonstrate the effect of the discount rate on investment recovery.

## Main Features

- Annual photovoltaic electricity generation
- Panel degradation assumption
- Operating and maintenance costs
- Simple payback period
- Discounted payback period
- Cumulative cash-flow visualization

## Model Assumptions

The assumptions are defined directly in `pv_payback.py` and can be modified for different project scenarios.

Important parameters include:

- Installed capacity
- Specific annual yield
- Investment cost
- Electricity price
- Annual operating cost
- Degradation rate
- Project lifetime
- Discount rate

## Installation
```bash
pip install -r requirements.txt
