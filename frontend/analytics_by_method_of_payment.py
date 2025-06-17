import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "http://localhost:8000"

def analytics_method_of_payment_tab():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024,8,1), key="payment_start")
    with col2:
        end_date = st.date_input("End Date", datetime(2024,11,30), key="payment_end")
    if st.button("Get Analytics", key="payment_button"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }
        response = requests.post(f"{API_URL}/analyticsbypayment/", json = payload)
        response = response.json()

        data = {
            "Payment": list(response.keys()),
            "Total": [response[method_of_payment]["total"] for method_of_payment in response],
            "Percentage": [response[method_of_payment]["percentage"] for method_of_payment in response]
        }
        df = pd.DataFrame(data)
        df_sorted = df.sort_values("Total", ascending=False)

        st.title("Expense Breakdown By Payment Method")
        st.bar_chart(data=df_sorted.set_index("Payment")["Percentage"], width = 0,height = 0, use_container_width = True)

        df_sorted['Total'] = df_sorted['Total'].map("{:.2f}".format)
        df_sorted['Percentage'] = df_sorted['Percentage'].map("{:.2f}".format)

        st.table(df_sorted)