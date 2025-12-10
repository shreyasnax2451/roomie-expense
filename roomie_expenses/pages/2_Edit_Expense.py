from datetime import datetime
import pandas as pd
import streamlit as st

from db.helpers import get_all_users, load_expenses, update_expense_in_db
from utils.constants import months, years
from utils.styles import UPDATE_CARD_STYLE

# ---------- UI ----------
st.title("🏠 Roommates — Edit Expense")

month_options = months
year_options = years
users, users_dict = get_all_users()

col_month, col_year, col_user = st.columns(3)

with col_month:
    selected_month = st.selectbox("Month", ["All"] + month_options)

with col_year:
    selected_year = st.selectbox("Year", ["All"] + [str(y) for y in year_options])

with col_user:
    selected_user = st.selectbox("Added By", ["All"] + users)
    selected_user_id = users_dict.get(selected_user) or "All"

# ---- Styling for cards + edit form ----
st.markdown(UPDATE_CARD_STYLE, unsafe_allow_html=True)

# Read edit selection from URL (new API)
params = st.query_params
editing = params.get("edit_expense", None)
editing_id = None
if editing:
    try:
        editing_id = int(editing)
    except Exception:
        editing_id = None

filtered = load_expenses(user_id=selected_user_id, month=selected_month, year=selected_year)
if filtered.empty:
    st.info("No expenses to show for the selected filters.")
else:
    # Render each expense as a card
    for _, row in filtered.sort_values("created_at", ascending=False).iterrows():
        exp_id = int(row["id"])
        user_id = row.get("added_by_id")
        name = row.get("source_of_expense", "—")
        amount = row.get("amount", 0)
        month = row.get("month", "")
        year = row.get("year", "")
        created = row.get("created_at", "")
        try:
            created_str = pd.to_datetime(created).strftime("%Y-%m-%d %H:%M")
        except Exception:
            created_str = str(created)

        avatar_letter = str(name or "?")[0].upper()

        # Card HTML header
        card_html = f"""
        <div class="exp-card">
          <div class="exp-row">
            <div class="exp-left">
              <div class="avatar">{avatar_letter}</div>
              <div>
                <div style="font-weight:700; font-size:15px;">{name}</div>
                <div class="exp-meta">{month} • {year} · <span class="small-muted">Added: {created_str}</span></div>
              </div>
            </div>
            <div style="display:flex;flex-direction:column;align-items:flex-end;">
              <div class="exp-amount">₹{amount:,.2f}</div>
            </div>
          </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

        cols = st.columns([1, 4])
        with cols[0]:
            # Edit button sets query param
            if st.button("Edit", key=f"edit_{exp_id}"):
                st.query_params["edit_expense"] = str(exp_id)
        with cols[1]:
            st.write("")

        if editing_id == exp_id:
            with st.form(key=f"form_{exp_id}", clear_on_submit=False):
                st.markdown("<div class='form-row'>", unsafe_allow_html=True)
                c1, c2 = st.columns([3,1])
                with c1:
                    src = st.text_input("Source / Description", value=str(row.get("source_of_expense", "")), key=f"src_{exp_id}")
                with c2:
                    amt = st.number_input("Amount (₹)", value=float(row.get("amount", 0)), min_value=0.0, format="%.2f", key=f"amt_{exp_id}")
                st.markdown("</div>", unsafe_allow_html=True)

                c4, c5 = st.columns([1,1])
                with c4:
                    save = st.form_submit_button("Save", use_container_width=True)
                with c5:
                    cancel = st.form_submit_button("Cancel", use_container_width=True)

                # Handle form actions
                if save:
                    payload = {
                        "source_of_expense": src,
                        "amount": float(amt),
                        "updated_at": datetime.utcnow()
                    }
                    is_expense_updated = update_expense_in_db(exp_id, payload)
                    if is_expense_updated:
                        st.success("Expense updated.")
                        st.experimental_rerun()
                    else:
                        st.error("Failed to update expense (check server logs).")

                if cancel:
                    st.query_params.pop("edit_expense", None)
                    st.experimental_rerun()

        # close card div
        st.markdown("</div>", unsafe_allow_html=True)
