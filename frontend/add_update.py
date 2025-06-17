import streamlit as st
from datetime import datetime
import requests

API_URL = "http://localhost:8000"

def add_update_tab():
    selected_date = st.date_input("Enter Date", datetime(2024,8,1), label_visibility='collapsed')
    response = requests.get(f"{API_URL}/expenses/{selected_date}")
    if response.status_code == 200:
        existing_expenses = response.json()
        # st.write(existing_expenses)
    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []

    categories = ["Rent","Food","Shopping","Entertainment","Other","Gas","Bills","Car","Transportation"]
    methods_of_payment = ["Amex Blue","Amex Hilton","Cash","Chase Unlimited", "Chase Rise","Debit Card"]

    with st.form(key = "expense_form"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.subheader("Amount")
        with col2:
            st.subheader("Category")
        with col3:
            st.subheader("Paid With")
        with col4:
            st.subheader("Notes")

        expenses = []
        for i in range(5):

            if i < len(existing_expenses):
                amount = existing_expenses[i]["amount"]
                category = existing_expenses[i]["category"]
                method_of_payment = existing_expenses[i]["method_of_payment"]
                notes = existing_expenses[i]["notes"]
            else:
                amount = 0.0
                category = "Shopping"
                method_of_payment = "Cash"
                notes = ""

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                amount_input = st.number_input(label = "Amount", min_value=0.0, step = 1.0, value = amount, key = f"amount_{i}",
                                               label_visibility='collapsed')
            with col2:
                category_input = st.selectbox(label = "Category", options = categories, index = categories.index(category),
                                              key = f"category_{i}", label_visibility='collapsed')
            with col3:
                method_of_payment_input = st.selectbox(label = "Payment", options = methods_of_payment, index = methods_of_payment.index(method_of_payment),
                                              key = f"method_of_payment_{i}", label_visibility='collapsed')
            with col4:
                notes_input = st.text_input(label = "Notes", value = notes, key = f"notes_{i}", label_visibility='collapsed')

            expenses.append({
                "amount": amount_input,
                "category": category_input,
                "method_of_payment": method_of_payment_input,
                "notes": notes_input
            })
        submit_button = st.form_submit_button()
        if submit_button:
            filtered_expenses = [expense for expense in expenses if expense["amount"] > 0]

            response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)
            if response.status_code == 200:
                print("satus_code: ", response.status_code)
                st.success("Expenses updated successfully!")
            else:
                print("satus_code: ", response.status_code)
                st.error("Failed to update expenses.")