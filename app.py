import streamlit as st
import pandas as pd
import plotly.express as px




# --- Functions for Cost Calculation and Projection ---

def calculate_annual_cost(consumption_kwh, wholesale_price, duos, tnuos, bsuos, cfd_levy, ro_levy, ccl, standing_charge,
                          vat_rate):
    """
    Calculates the annual electricity cost based on various UK market charges.

    Args:
        consumption_kwh (float): Annual electricity consumption in kWh.
        wholesale_price (float): Wholesale price in £/MWh.
        duos (float): DUoS charge in £/MWh.
        tnuos (float): TNUoS charge in £/MWh.
        bsuos (float): BSUoS charge in £/MWh.
        cfd_levy (float): CfD Levy in £/MWh.
        ro_levy (float): RO Levy in £/MWh.
        ccl (float): CCL in £/MWh.
        standing_charge (float): Standing charge in £/day.
        vat_rate (float): VAT rate (e.g., 0.05 for 5%).

    Returns:
        dict: A dictionary containing the cost breakdown.
    """
    # Convert charges from £/MWh to £/kWh by dividing by 1000
    wholesale_price_kwh = wholesale_price / 1000
    duos_kwh = duos / 1000
    tnuos_kwh = tnuos / 1000
    bsuos_kwh = bsuos / 1000
    cfd_levy_kwh = cfd_levy / 1000
    ro_levy_kwh = ro_levy / 1000
    ccl_kwh = ccl / 1000

    # Calculate the total unit cost in £/kWh
    unit_cost_kwh = (
            wholesale_price_kwh + duos_kwh + tnuos_kwh + bsuos_kwh +
            cfd_levy_kwh + ro_levy_kwh + ccl_kwh
    )

    # Calculate individual cost components
    energy_cost = unit_cost_kwh * consumption_kwh
    annual_standing_charge = standing_charge * 365

    # Calculate total and apply VAT
    subtotal = energy_cost + annual_standing_charge
    vat_amount = subtotal * vat_rate
    total_cost = subtotal + vat_amount

    return {
        'Energy Cost (£)': energy_cost,
        'Standing Charge (£)': annual_standing_charge,
        'VAT (£)': vat_amount,
        'Total Cost (£)': total_cost,
        'Effective Unit Cost (p/kWh)': unit_cost_kwh * 100
    }


def project_costs(consumption_kwh, years, base_wholesale_price, duos, tnuos, bsuos, cfd_levy, ro_levy, ccl,
                  standing_charge, vat_rate, escalation_rate):
    """
    Projects the annual electricity costs over a specified number of years.

    Args:
        consumption_kwh (float): Annual electricity consumption in kWh.
        years (int): Number of years to project.
        base_wholesale_price (float): Starting wholesale price in £/MWh.
        ... and other cost components
        escalation_rate (float): Annual escalation rate (e.g., 0.025 for 2.5%).

    Returns:
        list: A list of dictionaries, where each dictionary contains the cost breakdown for a year.
    """
    costs_over_years = []
    # Project costs for each year based on the escalation rate
    for year in range(years):
        escalation_factor = (1 + escalation_rate) ** year
        escalated_wholesale = base_wholesale_price * escalation_factor
        escalated_duos = duos * escalation_factor
        escalated_tnuos = tnuos * escalation_factor
        escalated_bsuos = bsuos * escalation_factor
        escalated_cfd = cfd_levy * escalation_factor
        escalated_ro = ro_levy * escalation_factor
        escalated_ccl = ccl * escalation_factor
        escalated_standing = standing_charge * escalation_factor

        annual_cost = calculate_annual_cost(
            consumption_kwh, escalated_wholesale, escalated_duos, escalated_tnuos,
            escalated_bsuos, escalated_cfd, escalated_ro, escalated_ccl,
            escalated_standing, vat_rate
        )
        costs_over_years.append(annual_cost)

    return costs_over_years


# --- Streamlit Application UI ---

st.set_page_config(
    page_title="UK Electricity Cost Estimator",
    layout="wide",
    initial_sidebar_state="auto"
)

st.title("💡 UK Electricity Cost Estimator")
st.write("Enter your business's details to estimate and project electricity costs over the next 15 years.")

# --- Input Section ---
st.header("Input Parameters")

# Use a container for a clean layout
with st.container(border=True):
    consumption_kwh = st.number_input(
        "Annual Electricity Consumption (kWh)",
        min_value=0.0,
        value=1000000.0,
        step=1000.0,
        format="%.0f",
        help="The total amount of electricity your business consumes in a year."
    )

    use_defaults = st.checkbox("Use default charge values", value=True)

    # Define default values for a cleaner look
    default_values = {
        "Wholesale Price": 90.0,  # £/MWh
        "DUoS Charge": 20.0,  # £/MWh
        "TNUoS Charge": 10.0,  # £/MWh
        "BSUoS Charge": 5.0,  # £/MWh
        "CfD Levy": 15.0,  # £/MWh
        "RO Levy": 5.0,  # £/MWh
        "CCL": 5.85,  # £/MWh
        "Standing Charge": 0.5137,  # £/day
        "VAT Rate": 0.05,  # 5%
        "Annual Escalation Rate": 0.025  # 2.5%
    }

    # Use columns to align the input fields
    col1, col2 = st.columns(2)

    if use_defaults:
        # Display current default values for transparency
        st.info("Using default values. Uncheck the box to enter custom values.")
        with st.expander("Show Default Values"):
            for key, value in default_values.items():
                st.write(f"**{key}**: {value} (as of July 2025)")

        wholesale_price = default_values["Wholesale Price"]
        duos = default_values["DUoS Charge"]
        tnuos = default_values["TNUoS Charge"]
        bsuos = default_values["BSUoS Charge"]
        cfd_levy = default_values["CfD Levy"]
        ro_levy = default_values["RO Levy"]
        ccl = default_values["CCL"]
        standing_charge = default_values["Standing Charge"]
        vat_rate = default_values["VAT Rate"]
        escalation_rate = default_values["Annual Escalation Rate"]

    else:
        # User input fields for custom values
        with col1:
            wholesale_price = st.number_input("Wholesale Price (£/MWh)", min_value=0.0,
                                              value=default_values["Wholesale Price"], step=1.0, format="%.2f")
            duos = st.number_input("DUoS Charge (£/MWh)", min_value=0.0, value=default_values["DUoS Charge"], step=1.0,
                                   format="%.2f")
            tnuos = st.number_input("TNUoS Charge (£/MWh)", min_value=0.0, value=default_values["TNUoS Charge"],
                                    step=1.0, format="%.2f")
            bsuos = st.number_input("BSUoS Charge (£/MWh)", min_value=0.0, value=default_values["BSUoS Charge"],
                                    step=1.0, format="%.2f")
            cfd_levy = st.number_input("CfD Levy (£/MWh)", min_value=0.0, value=default_values["CfD Levy"], step=1.0,
                                       format="%.2f")

        with col2:
            ro_levy = st.number_input("RO Levy (£/MWh)", min_value=0.0, value=default_values["RO Levy"], step=1.0,
                                      format="%.2f")
            ccl = st.number_input("CCL (£/MWh)", min_value=0.0, value=default_values["CCL"], step=0.1, format="%.2f")
            standing_charge = st.number_input("Standing Charge (£/day)", min_value=0.0,
                                              value=default_values["Standing Charge"], step=0.01, format="%.4f")
            vat_rate = st.number_input("VAT Rate (e.g., 0.05 for 5%)", min_value=0.0, value=default_values["VAT Rate"],
                                       step=0.01, format="%.3f")
            escalation_rate = st.number_input("Annual Escalation Rate (e.g., 0.025 for 2.5%)", min_value=0.0,
                                              value=default_values["Annual Escalation Rate"], step=0.005, format="%.3f")

# --- Calculation and Output ---
years_to_project = 15
costs = project_costs(
    consumption_kwh, years_to_project, wholesale_price, duos, tnuos, bsuos,
    cfd_levy, ro_levy, ccl, standing_charge, vat_rate, escalation_rate
)

# Year 1 (Current Year)
current_year = 2025
st.header(f"Cost Breakdown for {current_year}")
st.write(f"This is an estimation of your annual electricity costs for the current year.")
st.markdown(f"""
- **Energy Cost**: £{costs[0]['Energy Cost (£)']:,.2f}
- **Standing Charge**: £{costs[0]['Standing Charge (£)']:,.2f}
- **VAT**: £{costs[0]['VAT (£)']:,.2f}
- **Total Annual Cost**: £{costs[0]['Total Cost (£)']:,.2f}
- **Effective Unit Cost**: {costs[0]['Effective Unit Cost (p/kWh)']:.2f} p/kWh
""")

# --- Projection Section ---
st.header("15-Year Cost Projection")
st.write(
    f"The table below shows the projected costs for each year based on a {escalation_rate * 100:.1f}% annual escalation rate.")

df_costs = pd.DataFrame(costs)
df_costs['Year'] = range(current_year, current_year + years_to_project)
df_costs = df_costs.round(2)  # Round to 2 decimal places for cleaner display
df_costs['Energy Cost (£)'] = df_costs['Energy Cost (£)'].map('{:,.2f}'.format)
df_costs['Standing Charge (£)'] = df_costs['Standing Charge (£)'].map('{:,.2f}'.format)
df_costs['VAT (£)'] = df_costs['VAT (£)'].map('{:,.2f}'.format)
df_costs['Total Cost (£)'] = df_costs['Total Cost (£)'].map('{:,.2f}'.format)

st.dataframe(df_costs, use_container_width=True)

# --- Interactive Plotly Graph ---
st.header("Interactive Cost Trends Over 15 Years")
st.write("Hover over the lines to see exact values for each year. You can also zoom and pan the graph.")

# Create a 'melted' DataFrame for Plotly Express
df_plot = pd.DataFrame(costs)
df_plot['Year'] = range(current_year, current_year + years_to_project)

# Plotly Express is great for this kind of data. We'll plot the total cost and individual components.
fig = px.line(
    df_plot,
    x='Year',
    y=['Total Cost (£)', 'Energy Cost (£)', 'Standing Charge (£)', 'VAT (£)'],
    title='Projected Electricity Cost Breakdown',
    labels={'value': 'Annual Cost (£)', 'variable': 'Cost Component'},
    template='plotly_white'
)

# Enhance the layout
fig.update_layout(
    legend_title_text='Cost Components',
    xaxis_title='Year',
    yaxis_title='Annual Cost (£)',
    hovermode='x unified'
)

# Display the plot in Streamlit
st.plotly_chart(fig, use_container_width=True)

