import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Project assumptions
# -----------------------------
capacity_kw = 10
specific_yield = 1700          # kWh per kW per year
investment_cost = 8500         # currency units per kW
annual_om_cost = 0.02          # share of initial investment
electricity_price = 0.12      # currency units per kWh
degradation = 0.005            # annual generation degradation
project_life = 20

discount_rate = 0.10

# -----------------------------
# Annual calculations
# -----------------------------
initial_investment = capacity_kw * investment_cost
annual_generation = capacity_kw * specific_yield
annual_om = initial_investment * annual_om_cost

cash_flows = [-initial_investment]
discounted_cash_flows = [-initial_investment]

for year in range(1, project_life + 1):
    generation = annual_generation * ((1 - degradation) ** (year - 1))
    revenue = generation * electricity_price
    net_cash_flow = revenue - annual_om
    discounted_cash_flow = net_cash_flow / ((1 + discount_rate) ** year)

    cash_flows.append(net_cash_flow)
    discounted_cash_flows.append(discounted_cash_flow)

# -----------------------------
# Payback calculations
# -----------------------------
cumulative_cash_flow = np.cumsum(cash_flows)
cumulative_discounted_cash_flow = np.cumsum(discounted_cash_flows)

def calculate_payback(cumulative_values):
    for year, value in enumerate(cumulative_values):
        if value >= 0:
            return year
    return None

simple_payback = calculate_payback(cumulative_cash_flow)
discounted_payback = calculate_payback(cumulative_discounted_cash_flow)

print(f"Initial investment: {initial_investment:,.0f}")
print(f"Annual generation: {annual_generation:,.0f} kWh")
print(f"Simple payback period: {simple_payback} years")
print(f"Discounted payback period: {discounted_payback} years")

# -----------------------------
# Visualization
# -----------------------------
years = np.arange(0, project_life + 1)

plt.figure(figsize=(10, 6))
plt.plot(years, cumulative_cash_flow, marker="o", label="Simple cash flow")
plt.plot(years, cumulative_discounted_cash_flow, marker="s", label="Discounted cash flow")
plt.axhline(0, color="black", linewidth=1)
plt.xlabel("Year")
plt.ylabel("Cumulative cash flow")
plt.title("Cumulative Cash Flow of a Small-Scale PV Project")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("cumulative_cash_flow.png", dpi=300)
plt.show()
