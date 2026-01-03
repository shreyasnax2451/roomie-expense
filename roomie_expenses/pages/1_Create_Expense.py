import os
import streamlit as st
import time

from datetime import datetime
from db.helpers import add_expense_to_db, bulk_add_expense_to_db, get_all_users, get_db_session

from utils.constants import months, years, base_dir
from utils.enums import ExpenseSource
from utils.expense_helpers import parse_expense_from_image

# ---------- CONFIG ----------
@st.cache_data
def load_users():
    return get_all_users()

ROOMMATES, users_dict = load_users()
# ROOMMATES, users_dict = get_all_users()

path = os.path.join(base_dir, "sample_image.png")

# ---------- UI ----------
st.title("🏠 Roommates — Add Expense")

expense_parser = st.selectbox("Option for Expense", [ExpenseSource.MANUAL_EXPENSE.value, ExpenseSource.IMAGE_UPLOAD.value])

expenses = []

if expense_parser == ExpenseSource.MANUAL_EXPENSE.value:
    # Manual Expense Form
    with st.form("manual_expense_form", clear_on_submit=True):
        col1, col2 = st.columns([3, 2])
        with col1:
            source = st.text_input("Expense source (e.g., Chicken, Instamart, Maid)", placeholder="e.g. Instamart")
        with col2:
            amount = st.text_input("Amount (₹)", placeholder="e.g. 260.5")
        col3, col4 = st.columns([2, 2])
        with col3:
            added_by = st.selectbox("Added by", options=ROOMMATES)

        month = st.selectbox("Month", options=months, index=datetime.now().month - 1)
        year = st.selectbox("Year", options=years, index=0)
        submitted = st.form_submit_button("Add expense")

    if submitted:
        if not source:
            st.error("Please enter an expense source.")
        elif not amount:
            st.error("Please enter amount")
        elif not added_by:
            st.error("Please enter User info")
        else:
            try:
                amt = float(amount)
                message = f"✅ Added: {source.strip()} — ₹{amt:.2f} ({month} {year})"
                st.toast(message)
                time.sleep(1.4)
                with get_db_session() as session:
                    add_expense_to_db(source.strip(), amt, users_dict.get(added_by), month, int(year))
            except ValueError as e:
                st.toast(str(e))

elif expense_parser == ExpenseSource.IMAGE_UPLOAD.value:
    # Image Uploader Form
    st.image(path, caption="Sample Format")

    image_uploaded = st.file_uploader("Upload expense screenshot", type=["jpg", "jpeg", "png"])
    with st.form("image_expense_form", clear_on_submit=True):
        col3, col4 = st.columns([2, 2])
        with col3:
            added_by = st.selectbox("Added by", options=ROOMMATES)

        month = st.selectbox("Month", options=months, index=datetime.now().month - 1)
        year = st.selectbox("Year", options=years, index=0)
        submitted = st.form_submit_button("Add expense")
    
    if submitted:
        try:
            expenses_data = parse_expense_from_image(image_uploaded)
            for expense in expenses_data:
                expense["month"] = month
                expense["year"] = year
                expense["added_by_id"] = users_dict.get(added_by)
                expense["created_at"] = datetime.utcnow()
                expense["updated_at"] = datetime.utcnow()
            expenses_count = bulk_add_expense_to_db(expenses_data)
            time.sleep(1.8)
        except ValueError:
            st.error("Expenses Addition via Image Failed")

