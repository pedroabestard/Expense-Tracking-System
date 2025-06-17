import streamlit as st
import requests
import pandas as pd
import altair as alt

API_URL = "http://localhost:8000"

def analytics_months_tab():
    response = requests.get(f"{API_URL}/analyticsbymonths/")
    response = response.json()

    data = {
        "Month": list(response.keys()),
        "Total": [response[month]["total"] for month in response],
        "Percentage": [response[month]["percentage"] for month in response]
    }

    df = pd.DataFrame(data)

    # Create datetime and formatted columns
    df["Month_dt"] = pd.to_datetime(df["Month"])
    df["MonthCode"] = df["Month_dt"].dt.strftime('%Y%m')           # For x-axis
    df["MonthName"] = df["Month_dt"].dt.strftime('%B %Y')          # For table
    df = df.sort_values("Month_dt")

    # Altair chart: discrete x-axis using MonthCode
    line_chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('MonthCode:N', sort=df["MonthCode"].tolist(), title = "Month",axis=alt.Axis(labelAngle=45)),
        y=alt.Y('Total:Q', title='Total Expense',),
        tooltip=['MonthName', 'Total', 'Percentage']
    ).properties(
        title='Monthly Expense Trend',
        width='container'
    )

    st.altair_chart(line_chart, use_container_width=True)

    # Format numbers in table
    df['Total'] = df['Total'].map("{:.2f}".format)
    df['Percentage'] = df['Percentage'].map("{:.2f}".format)

    # Display formatted table with MonthName
    st.table(df[["MonthName", "Total", "Percentage"]].rename(columns={"MonthName": "Month"}))