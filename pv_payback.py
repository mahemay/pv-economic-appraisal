import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# Input validation
# ============================================================

def get_float_input(prompt, default, minimum, maximum):
    """
    Receives a floating-point number from the user.

    Pressing Enter returns the default value.
    Values outside the specified range are rejected.
    """
    while True:
        user_input = input(f"{prompt} ({default}): ").strip()

        if user_input == "":
            return float(default)

        # Allow both decimal point and decimal comma
        user_input = user_input.replace(",", ".")

        try:
            value = float(user_input)

            if minimum <= value <= maximum:
                return value

            print(
                f"Error: Enter a value between "
                f"{minimum} and {maximum}."
            )

        except ValueError:
            print("Error: Please enter a valid numeric value.")


def get_integer_input(prompt, default, minimum, maximum):
    """
    Receives an integer from the user.

    Pressing Enter returns the default value.
    Decimal and non-numeric values are rejected.
    """
    while True:
        user_input = input(f"{prompt} ({default}): ").strip()

        if user_input == "":
            return int(default)

        try:
            value = int(user_input)

            if minimum <= value <= maximum:
                return value

            print(
                f"Error: Enter an integer between "
                f"{minimum} and {maximum}."
            )

        except ValueError:
            print("Error: Please enter a valid integer.")


def get_rate_input(prompt, default_percent, minimum_percent, maximum_percent):
    """
    Receives percentage rates in percent format.

    Example:
        Enter 8 for 8 percent.
        Enter 0.5 for 0.5 percent.

    The returned value is converted to decimal format.
    """
    value_percent = get_float_input(
        prompt=prompt,
        default=default_percent,
        minimum=minimum_percent,
        maximum=maximum_percent
    )

    return value_percent / 100


# ============================================================
# Financial functions
# ============================================================

def calculate_npv(rate, cash_flows):
    """
    Calculates net present value, including the year-zero
    investment.
    """
    return sum(
        cash_flow / ((1 + rate) ** year)
        for year, cash_flow in enumerate(cash_flows)
    )


def calculate_irr(cash_flows, lower_bound=-0.9999,
                  upper_bound=10.0, tolerance=1e-8,
                  max_iterations=1000):
    """
    Calculates IRR using the bisection method.

    This avoids dependency on numpy-financial.
    Returns None when no valid IRR can be identified.
    """

    def npv_at_rate(rate):
        return calculate_npv(rate, cash_flows)

    npv_lower = npv_at_rate(lower_bound)
    npv_upper = npv_at_rate(upper_bound)

    # The bisection method requires opposite signs.
    if npv_lower * npv_upper > 0:
        return None

    for _ in range(max_iterations):
        midpoint = (lower_bound + upper_bound) / 2
        npv_midpoint = npv_at_rate(midpoint)

        if abs(npv_midpoint) < tolerance:
            return midpoint

        if npv_lower * npv_midpoint < 0:
            upper_bound = midpoint
            npv_upper = npv_midpoint
        else:
            lower_bound = midpoint
            npv_lower = npv_midpoint

    return (lower_bound + upper_bound) / 2


def calculate_fractional_payback(cash_flows):
    """
    Calculates a fractional payback period.

    Example:
        4.35 years instead of only reporting year 5.
    """
    cumulative_cash_flow = cash_flows[0]

    if cumulative_cash_flow >= 0:
        return 0.0

    for year in range(1, len(cash_flows)):
        previous_cumulative = cumulative_cash_flow
        cumulative_cash_flow += cash_flows[year]

        if cumulative_cash_flow >= 0:
            unrecovered_amount = abs(previous_cumulative)
            current_year_cash_flow = cash_flows[year]

            if current_year_cash_flow <= 0:
                return float(year)

            fraction = unrecovered_amount / current_year_cash_flow
            return (year - 1) + fraction

    return None


def create_project_cash_flows(
    capacity_kw,
    specific_yield,
    investment_cost_per_kw,
    annual_om_rate,
    electricity_price,
    degradation_rate,
    project_life
):
    """
    Creates annual project cash flows.

    O&M is assumed to remain constant in nominal terms.
    No taxes, inflation, subsidies, or residual value are
    included in this basic version.
    """
    initial_investment = capacity_kw * investment_cost_per_kw
    first_year_generation = capacity_kw * specific_yield
    annual_om_cost = initial_investment * annual_om_rate

    cash_flows = [-initial_investment]
    generations = [0.0]
    revenues = [0.0]
    om_costs = [0.0]

    for year in range(1, project_life + 1):
        generation = (
            first_year_generation
            * ((1 - degradation_rate) ** (year - 1))
        )

        revenue = generation * electricity_price
        net_cash_flow = revenue - annual_om_cost

        generations.append(generation)
        revenues.append(revenue)
        om_costs.append(annual_om_cost)
        cash_flows.append(net_cash_flow)

    return {
        "initial_investment": initial_investment,
        "first_year_generation": first_year_generation,
        "annual_om_cost": annual_om_cost,
        "generations": generations,
        "revenues": revenues,
        "om_costs": om_costs,
        "cash_flows": cash_flows
    }


# ============================================================
# User inputs
# ============================================================

print("=" * 68)
print("        PV SYSTEM ECONOMIC APPRAISAL MODEL")
print("              IRENA-BASED DEFAULT VALUES")
print("=" * 68)

print("\nPress Enter to use the default value shown in parentheses.")
print("Enter percentage rates as percentages, not decimals.")
print("Example: enter 8 for 8%, and 0.5 for 0.5%.\n")

capacity_kw = get_float_input(
    "System capacity in kW",
    default=10.0,
    minimum=0.1,
    maximum=100000.0
)

specific_yield = get_float_input(
    "Specific yield in kWh/kW/year",
    default=1700.0,
    minimum=500.0,
    maximum=3000.0
)

investment_cost_per_kw = get_float_input(
    "Investment cost in USD/kW",
    default=650.0,
    minimum=100.0,
    maximum=10000.0
)

annual_om_rate = get_rate_input(
    "Annual O&M cost as percent of initial investment",
    default_percent=1.5,
    minimum_percent=0.0,
    maximum_percent=10.0
)

electricity_price = get_float_input(
    "Electricity price in USD/kWh",
    default=0.09,
    minimum=0.001,
    maximum=2.0
)

degradation_rate = get_rate_input(
    "Annual PV degradation rate (%)",
    default_percent=0.5,
    minimum_percent=0.0,
    maximum_percent=5.0
)

project_life = get_integer_input(
    "Project lifetime in years",
    default=20,
    minimum=1,
    maximum=50
)

discount_rate = get_rate_input(
    "Discount rate / WACC (%)",
    default_percent=8.0,
    minimum_percent=0.0,
    maximum_percent=50.0
)


# ============================================================
# Base-case calculations
# ============================================================

project = create_project_cash_flows(
    capacity_kw=capacity_kw,
    specific_yield=specific_yield,
    investment_cost_per_kw=investment_cost_per_kw,
    annual_om_rate=annual_om_rate,
    electricity_price=electricity_price,
    degradation_rate=degradation_rate,
    project_life=project_life
)

initial_investment = project["initial_investment"]
first_year_generation = project["first_year_generation"]
annual_om_cost = project["annual_om_cost"]
cash_flows = project["cash_flows"]

years = np.arange(0, project_life + 1)

discounted_cash_flows = [
    cash_flow / ((1 + discount_rate) ** year)
    for year, cash_flow in enumerate(cash_flows)
]

cumulative_cash_flows = np.cumsum(cash_flows)
cumulative_discounted_cash_flows = np.cumsum(
    discounted_cash_flows
)

simple_payback = calculate_fractional_payback(cash_flows)

discounted_payback = calculate_fractional_payback(
    discounted_cash_flows
)

npv = calculate_npv(discount_rate, cash_flows)
irr = calculate_irr(cash_flows)

total_generation = sum(project["generations"])
total_revenue = sum(project["revenues"])
total_om_cost = sum(project["om_costs"])


# ============================================================
# Display base-case results
# ============================================================

print("\n" + "=" * 68)
print("                    BASE-CASE RESULTS")
print("=" * 68)

print(f"System capacity                  : {capacity_kw:,.2f} kW")
print(
    f"Initial investment               : "
    f"${initial_investment:,.2f}"
)
print(
    f"Annual O&M cost                  : "
    f"${annual_om_cost:,.2f}"
)
print(
    f"First-year electricity generation: "
    f"{first_year_generation:,.0f} kWh"
)
print(
    f"Lifetime electricity generation  : "
    f"{total_generation:,.0f} kWh"
)
print(
    f"Lifetime undiscounted revenue     : "
    f"${total_revenue:,.2f}"
)
print(
    f"Lifetime undiscounted O&M cost    : "
    f"${total_om_cost:,.2f}"
)

if simple_payback is None:
    print(
        "Simple payback period           : "
        "Not achieved during project life"
    )
else:
    print(
        f"Simple payback period            : "
        f"{simple_payback:.2f} years"
    )

if discounted_payback is None:
    print(
        "Discounted payback period       : "
        "Not achieved during project life"
    )
else:
    print(
        f"Discounted payback period        : "
        f"{discounted_payback:.2f} years"
    )

print(f"Net present value (NPV)           : ${npv:,.2f}")

if irr is None:
    print("Internal rate of return (IRR)     : Not available")
else:
    print(f"Internal rate of return (IRR)     : {irr * 100:.2f}%")

if npv > 0:
    print("NPV decision                     : Financially acceptable")
elif npv < 0:
    print("NPV decision                     : Financially unacceptable")
else:
    print("NPV decision                     : Break-even")

if irr is not None:
    if irr > discount_rate:
        print("IRR decision                     : IRR exceeds WACC")
    elif irr < discount_rate:
        print("IRR decision                     : IRR is below WACC")
    else:
        print("IRR decision                     : IRR equals WACC")

print("=" * 68)


# ============================================================
# Annual cash-flow table
# ============================================================

print("\n" + "=" * 98)
print("                            ANNUAL CASH-FLOW TABLE")
print("=" * 98)

print(
    f"{'Year':>5}"
    f"{'Generation':>16}"
    f"{'Revenue':>15}"
    f"{'O&M Cost':>15}"
    f"{'Net Cash Flow':>18}"
    f"{'Discounted CF':>18}"
)

print(
    f"{'':>5}"
    f"{'(kWh)':>16}"
    f"{'(USD)':>15}"
    f"{'(USD)':>15}"
    f"{'(USD)':>18}"
    f"{'(USD)':>18}"
)

print("-" * 98)

for year in range(project_life + 1):
    print(
        f"{year:>5}"
        f"{project['generations'][year]:>16,.0f}"
        f"{project['revenues'][year]:>15,.2f}"
        f"{project['om_costs'][year]:>15,.2f}"
        f"{cash_flows[year]:>18,.2f}"
        f"{discounted_cash_flows[year]:>18,.2f}"
    )


# ============================================================
# Sensitivity analysis
# ============================================================

sensitivity_factors = np.array([
    0.80,
    0.90,
    1.00,
    1.10,
    1.20
])

sensitivity_matrix = np.zeros((
    len(sensitivity_factors),
    len(sensitivity_factors)
))

for capex_index, capex_factor in enumerate(sensitivity_factors):
    for price_index, price_factor in enumerate(
        sensitivity_factors
    ):
        sensitivity_project = create_project_cash_flows(
            capacity_kw=capacity_kw,
            specific_yield=specific_yield,
            investment_cost_per_kw=(
                investment_cost_per_kw * capex_factor
            ),
            annual_om_rate=annual_om_rate,
            electricity_price=(
                electricity_price * price_factor
            ),
            degradation_rate=degradation_rate,
            project_life=project_life
        )

        sensitivity_npv = calculate_npv(
            discount_rate,
            sensitivity_project["cash_flows"]
        )

        sensitivity_matrix[
            capex_index,
            price_index
        ] = sensitivity_npv


# ============================================================
# Display sensitivity table
# ============================================================

print("\n" + "=" * 78)
print("             NPV SENSITIVITY ANALYSIS — CAPEX VS PRICE")
print("=" * 78)
print("Rows represent CAPEX changes; columns represent price changes.")
print("All values are NPV in USD.\n")

header = f"{'CAPEX / Price':>15}"

for price_factor in sensitivity_factors:
    header += f"{price_factor:>12.0%}"

print(header)
print("-" * 78)

for row_index, capex_factor in enumerate(sensitivity_factors):
    row = f"{capex_factor:>15.0%}"

    for column_index in range(len(sensitivity_factors)):
        row += (
            f"{sensitivity_matrix[row_index, column_index]:>12,.0f}"
        )

    print(row)

print("=" * 78)


# ============================================================
# Cash-flow chart
# ============================================================

plt.figure(figsize=(11, 6.5))

plt.plot(
    years,
    cumulative_cash_flows,
    marker="o",
    markersize=4,
    linewidth=2,
    color="#00796B",
    label="Cumulative cash flow"
)

plt.plot(
    years,
    cumulative_discounted_cash_flows,
    marker="s",
    markersize=4,
    linewidth=2,
    color="#EF6C00",
    label="Cumulative discounted cash flow"
)

plt.axhline(
    y=0,
    color="black",
    linestyle="--",
    linewidth=1
)

plt.title(
    "PV Project Cumulative Cash Flow",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel("Project year")
plt.ylabel("Cumulative cash flow (USD)")
plt.grid(alpha=0.25)
plt.legend()
plt.tight_layout()

cash_flow_chart_name = "cumulative_cash_flow.png"

plt.savefig(
    cash_flow_chart_name,
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# ============================================================
# Sensitivity heatmap
# ============================================================

fig, ax = plt.subplots(figsize=(9, 6.5))

image = ax.imshow(
    sensitivity_matrix,
    cmap="RdYlGn",
    aspect="auto"
)

ax.set_xticks(np.arange(len(sensitivity_factors)))
ax.set_yticks(np.arange(len(sensitivity_factors)))

ax.set_xticklabels([
    f"{factor:.0%}"
    for factor in sensitivity_factors
])

ax.set_yticklabels([
    f"{factor:.0%}"
    for factor in sensitivity_factors
])

ax.set_xlabel("Electricity price relative to base case")
ax.set_ylabel("CAPEX relative to base case")

ax.set_title(
    "NPV Sensitivity Analysis (USD)",
    fontsize=14,
    fontweight="bold"
)

maximum_absolute_npv = np.max(np.abs(sensitivity_matrix))

for row_index in range(len(sensitivity_factors)):
    for column_index in range(len(sensitivity_factors)):
        cell_value = sensitivity_matrix[
            row_index,
            column_index
        ]

        # Improve text visibility according to cell intensity
        if maximum_absolute_npv == 0:
            text_color = "black"
        elif abs(cell_value) > 0.65 * maximum_absolute_npv:
            text_color = "white"
        else:
            text_color = "black"

        ax.text(
            column_index,
            row_index,
            f"{cell_value:,.0f}",
            ha="center",
            va="center",
            color=text_color,
            fontsize=9,
            fontweight="bold"
        )

color_bar = fig.colorbar(image, ax=ax)
color_bar.set_label("NPV (USD)")

plt.tight_layout()

sensitivity_chart_name = "npv_sensitivity_heatmap.png"

plt.savefig(
    sensitivity_chart_name,
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# ============================================================
# Final message
# ============================================================

print("\nAnalysis completed successfully.")

print(
    f"Cash-flow chart saved as: "
    f"{cash_flow_chart_name}"
)

print(
    f"Sensitivity chart saved as: "
    f"{sensitivity_chart_name}"
)
