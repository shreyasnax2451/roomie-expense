import pandas as pd
import plotly.express as px
import streamlit as st

st.info("Coming Soon...")

# st.markdown("---")
# st.header("Expenses and Analysis")

# # Load data
# df = load_expenses_df()

# if df.empty:
#     st.info("No expenses recorded yet. Add one above to get started.")
# else:
#     # Filters
#     st.sidebar.header("Filter")
#     unique_years = sorted(df["year"].unique(), reverse=True)
#     sel_year = st.sidebar.selectbox("Year", options=["All"] + [str(y) for y in unique_years], index=0)
#     unique_months = ["All"] + months
#     sel_month = st.sidebar.selectbox("Month", options=unique_months, index=0)
#     sel_added_by = st.sidebar.selectbox("Added by", options=["All"] + ROOMMATES, index=0)

#     filtered = df.copy()
#     if sel_year != "All":
#         filtered = filtered[filtered["year"] == int(sel_year)]
#     if sel_month != "All":
#         filtered = filtered[filtered["month_name"] == sel_month]
#     if sel_added_by != "All":
#         filtered = filtered[filtered["added_by"] == sel_added_by]

#     # Table & totals
#     display_df = filtered[["id", "source", "amount", "added_by", "month_name", "year", "created_at"]].rename(
#         columns={"month_name": "month"}
#     )
#     display_df = display_df.reset_index(drop=True)
#     st.subheader("Recorded expenses")
#     st.dataframe(display_df.style.format({"amount": "₹{:.2f}"}), height=300)

#     total = filtered["amount"].sum()
#     st.metric("Total (filtered)", f"₹{total:.2f}")

#     # Charts: category (source) totals and split by roommate
#     with st.expander("Charts"):
#         # Group by source (sum amounts for identical sources)
#         by_source = filtered.groupby("source", as_index=False)["amount"].sum().sort_values("amount", ascending=False)
#         if not by_source.empty:
#             st.subheader("Expenses by source (top categories)")
#             st.plotly_chart(px.bar(by_source, x="source", y="amount", title="Amount by source", labels={"amount": "Amount (₹)"}), use_container_width=True)

#             st.subheader("Expense distribution (pie)")
#             st.plotly_chart(px.pie(by_source, values="amount", names="source", title="Expense distribution"), use_container_width=True)

#         by_person = filtered.groupby("added_by", as_index=False)["amount"].sum()
#         if not by_person.empty:
#             st.subheader("Added by (per person)")
#             st.plotly_chart(px.bar(by_person, x="added_by", y="amount", title="Amount added by person", labels={"amount": "Amount (₹)"}), use_container_width=True)

#     # CSV export
#     csv = display_df.to_csv(index=False)
#     st.download_button("Download filtered CSV", data=csv, file_name="expenses.csv", mime="text/csv")

# # small footer
# st.markdown("---")
# st.caption("This stores expenses in a local SQLite file (expenses.db). Replace ROOMMATES list with your roommates' names.")