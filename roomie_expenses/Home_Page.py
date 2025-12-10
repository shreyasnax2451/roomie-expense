import altair as alt
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from typing import Optional

from db.helpers import load_user_totals, load_expenses, get_all_users
from utils.constants import months, years
from utils.styles import CARD_CSS


# --- App ---
st.set_page_config(page_title="Expenses — Dashboard", layout="wide")
st.title("Home Page - Expenses")

# Month & Year Filters
st.markdown("## Filters")

month_options = months
year_options = years

col_month, col_year = st.columns(2)

with col_month:
    selected_month = st.selectbox("Month", ["All"] + month_options)

with col_year:
    selected_year = st.selectbox("Year", ["All"] + [str(y) for y in year_options])

user_totals = load_user_totals(selected_month, selected_year)
# format totals for display
user_totals = user_totals.sort_values("total_amount", ascending=False).reset_index(drop=True)
user_totals["total_str"] = user_totals["total_amount"].map(lambda x: f"₹{x:,.2f}")
user_totals["num_str"] = user_totals["num_expenses"].astype(str) + " expenses added"


st.markdown(CARD_CSS, unsafe_allow_html=True)

# --- Top area: bar chart + tiles ---
left, right = st.columns([2, 3])

with left:
    st.subheader("Totals by user")
    if user_totals.empty:
        st.info("No users found.")
    else:
        chart_df = user_totals[["user_id", "name", "total_amount"]].copy()
        chart = (
            alt.Chart(chart_df)
            .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
            .encode(
                x=alt.X("name:N", title="Roomie", sort=alt.EncodingSortField(field="total_amount", order="descending")),
                y=alt.Y("total_amount:Q", title="Total (₹)"),
                tooltip=[alt.Tooltip("name:N"), alt.Tooltip("total_amount:Q", format=",.2f")],
                color=alt.condition(
                    alt.datum.total_amount > chart_df["total_amount"].median(),
                    alt.value("#60a5fa"),
                    alt.value("#94a3b8")
                )
            )
            .properties(height=320, width="container")
        )
        st.altair_chart(chart, use_container_width=True)
        st.caption("Tip: Click a user's 'View' button on the right to see details.")

with right:
    st.subheader("Users")
    max_cols = 2
    rows = [user_totals.iloc[i : i + max_cols] for i in range(0, len(user_totals), max_cols)]
    for row in rows:
        cols = st.columns(len(row))
        for col, (_, r) in zip(cols, row.iterrows()):
            with col:
                # render small card
                avatar_letter = r["name"][0].upper()
                html = f"""
                <div class="user-card">
                  <div style="display:flex; gap:12px; align-items:center;">
                    <div class="user-avatar">{avatar_letter}</div>
                    <div style="flex:1;">
                      <p class="user-name">{r['name']}</p>
                      <p class="user-meta">{r['num_str']} • {r['total_str']}</p>
                    </div>
                  </div>
                </div>
                """
                st.markdown(html, unsafe_allow_html=True)

                # View button sets query param (no session_state)
                btn_key = f"view_user_{int(r['user_id'])}"
                if st.button("View", key=btn_key):
                    # set selected user in URL query params
                    st.query_params["selected_user"] = str(int(r["user_id"]))

st.markdown("---")

params = st.query_params
selected_user = params.get("selected_user", None)
selected_user_id: Optional[int] = None
if selected_user:
    try:
        selected_user_id = int(selected_user)
    except Exception:
        selected_user_id = None

if selected_user_id is None:
    st.info("Click a user's **View** button to see their expense list here.")
else:
    st.subheader(f"Expenses:")        
    filtered = load_expenses(selected_user_id, selected_month, selected_year)
    if filtered.empty:
        st.warning("No expenses found for this user.")
    else:
        filtered["created_at"] = pd.to_datetime(filtered["created_at"])
        filtered = filtered.sort_values("created_at", ascending=False)
        filtered["amount_display"] = filtered["amount"].map(lambda x: f"₹{x:,.2f}")
        display_cols = ["source_of_expense", "amount_display", "month", "year", "created_at"]

        display_df = filtered[display_cols].rename(columns={"amount_display": "amount"}).copy()
        display_df["created_at"] = pd.to_datetime(display_df["created_at"]).dt.strftime("%Y-%m-%d %H:%M:%S")

        # build grid options
        gb = GridOptionsBuilder.from_dataframe(display_df)
        gb.configure_default_column(filterable=True, sortable=True, resizable=True, wrapText=True)
        gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)
        gb.configure_side_bar()
        cell_style_amount = JsCode("""
        function(params) {
        return {
            'textAlign': 'left',
            'fontWeight': '700',
            'paddingRight': '12px'
        }
        }
        """)
        gb.configure_column("source_of_expense", header_name="Source of Expense")
        gb.configure_column("amount", header_name="Amount (₹)", cellStyle=cell_style_amount)
        gb.configure_column("created_at", header_name="Created At", width=180)
        gb.configure_column("month", header_name="Month", width=180)
        gb.configure_column("year", header_name="Year", width=100)

        grid_opts = gb.build()

        AgGrid(
            display_df,
            gridOptions=grid_opts,
            allow_unsafe_jscode=True,
            enable_enterprise_modules=False,
            fit_columns_on_grid_load=True,
            height=360,
        )

        # Download CSV Option
        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", data=csv, file_name=f"user_{selected_user_id}_{selected_month}_{selected_year}_expenses.csv", mime="text/csv")
