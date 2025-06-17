from add_update import add_update_tab
from analytics_by_category import analytics_category_tab
from analytics_by_months import analytics_months_tab
from analytics_by_method_of_payment import analytics_method_of_payment_tab
import streamlit as st

st.title("Expense Management System")

tab1, tab2, tab3, tab4 = st.tabs(["Add/Update","Analytics By Category","Analytics By Month","Analytics By Method of Payment"])

with tab1:
    add_update_tab()

with tab2:
    analytics_category_tab()

with tab3:
    analytics_months_tab()

with tab4:
    analytics_method_of_payment_tab()

