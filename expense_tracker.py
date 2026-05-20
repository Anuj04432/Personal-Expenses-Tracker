# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import csv
# import os
# from datetime import datetime
# import sqlite3

# def get_file_names(username):
#     return f"expenses_{username}.csv", f"budget_{username}.txt"

# def save_budget(username, amount):
#     _, budget_file = get_file_names(username)
#     with open(budget_file, "w") as f:
#         f.write(str(amount))
        

# def load_budget(username):
#     _, budget_file = get_file_names(username)
#     if os.path.exists(budget_file):
#         with open(budget_file, "r") as f:
#             return float(f.read().strip())
#     return None

# def init_csv(username):
#     file_name, _ = get_file_names(username)
#     if not os.path.isfile(file_name):
#         with open(file_name, mode="w", newline="") as file:
#             writer = csv.writer(file)
#             writer.writerow(["Date", "Category", "Amount", "Note"])

# def load_data(username):
#     file_name, _ = get_file_names(username)
#     if not os.path.isfile(file_name):
#         return pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])
#     return pd.read_csv(file_name)

# def add_expense(username, category, amount, note):
#     file_name, _ = get_file_names(username)
#     date = datetime.now().strftime("%Y-%m-%d")
#     with open(file_name, mode="a", newline="") as file:
#         writer = csv.writer(file)
#         writer.writerow([date, category, amount, note])

# def clear_data(username):
#     file_name, _ = get_file_names(username)
#     with open(file_name, mode="w", newline="") as file:
#         writer = csv.writer(file)
#         writer.writerow(["Date", "Category", "Amount", "Note"])

# # Streamlit App
# st.set_page_config(page_title="💰 My Personal Expenses", layout="centered")
# st.title("💰 My Personal Expenses Tracker")

# # Ask username first
# username = st.text_input("Enter your username")

# if username:
#     init_csv(username)

#     menu = ["Add Expense", "Show Summary", "Show Graph", "Clear Data", "Budget & Alerts","History"]
#     choice = st.sidebar.radio("Menu", menu)

#     if choice == "Add Expense":
#         st.subheader("Add New Expense")
#         category = st.text_input("Category")
#         amount = st.text_input("Amount")
#         note = st.text_input("Note (optional)")

#         if st.button("Add Expense"):
#             if category == "" or amount == "":
#                 st.error("Category and Amount are required!")
#             else:
#                 try:
#                     amount = float(amount)
#                     add_expense(username, category, amount, note)
#                     st.success(f"Expense Added: {category} - ₹{amount}")
#                 except ValueError:
#                     st.error("Amount must be a number!")

#     elif choice == "Show Summary":
#         st.subheader("Expense Summary")
#         df = load_data(username)
#         if df.empty:
#             st.info("No expenses yet!")
#         else:
#             st.dataframe(df)
#             total = df["Amount"].sum()
#             st.write(f"Total Spent: ₹{total}")

#     elif choice == "Show Graph":
#         types = ['Bar_graph','Line_chart','Pie_chart']
#         st.subheader("Expenses by Category")
#         graph_choice = st. radio("Graphs",types)
#         df = load_data(username)
#         if df.empty:
#             st.info("No expenses to plot!")

#         else:
#             if graph_choice == 'Bar_graph':
#                 category_summary = df.groupby("Category")["Amount"].sum()
#                 fig, ax = plt.subplots()
#                 category_summary.plot(kind="bar", color="skyblue", ax=ax)
#                 ax.set_title("Expenses by Category")
#                 ax.set_xlabel("Category")
#                 ax.set_ylabel("Amount")
#                 st.pyplot(fig)
#             elif graph_choice == 'Line_chart':
#                 fig, ax = plt.subplots()
#                 ax.plot(df["Date"],df["Amount"])
#                 st.pyplot(fig)
#             elif graph_choice == 'Pie_chart':
#                 category_summary = df.groupby("Category")["Amount"].sum()
#                 fig , ax = plt.subplots()
#                 ax.pie(category_summary,labels=category_summary.index,autopct='%1.1f%%')
#                 st.pyplot(fig)


#     elif choice == "Budget & Alerts":
#         st.subheader("Budget Limit")
#         df = load_data(username)

#         budget = load_budget(username)
#         if budget is None:
#             new_budget = st.number_input("Enter your monthly budget", min_value=0.0, step=100.0)
#             if st.button("Save Budget"):
#                 save_budget(username, new_budget)
#                 st.success(f"The budget has been set: ₹{new_budget}")
#                 budget = new_budget
#         else:
#             st.info(f"Your monthly budget is: ₹{budget}")

#             total_spent = df["Amount"].sum()
#             st.write(f"Total amount spent: ₹{total_spent}")

#             if total_spent > budget:
#                 st.error("You have crossed your budget!")
#             else:
#                 st.success(f"You are within your budget. Remaining balance: ₹{budget - total_spent}")

#             if st.button("Reset Budget"):
#                 _, budget_file = get_file_names(username)
#                 os.remove(budget_file)
#                 st.warning("!! Budget has been reset !!")

#     elif choice == "Clear Data":
#         st.subheader("🗑 Clear All Expenses")
#         if st.button("Clear All Data"):
#             clear_data(username)
#             st.success("All expenses cleared!")

#     elif choice == "History":
#         st.subheader("📜 Expense History")

#         df = load_data(username)

#         if df.empty:
#             st.info("No history available!")
#         else:
#             # Convert Date column to datetime
#             df["Date"] = pd.to_datetime(df["Date"])

#             # Filters
#             st.markdown("### 🔍 Filter Options")

#             # Date filter
#             start_date = st.date_input("Start Date", df["Date"].min())
#             end_date = st.date_input("End Date", df["Date"].max())

#             # Category filter
#             categories = df["Category"].unique().tolist()
#             selected_category = st.selectbox("Select Category", ["All"] + categories)

#             # Apply filters
#             filtered_df = df[
#                 (df["Date"] >= pd.to_datetime(start_date)) &
#                 (df["Date"] <= pd.to_datetime(end_date))
#             ]

#             if selected_category != "All":
#                 filtered_df = filtered_df[filtered_df["Category"] == selected_category]

#             # Show data
#             st.dataframe(filtered_df)

#             # Total of filtered data
#             total = filtered_df["Amount"].sum()
#             st.write(f"### 💰 Filtered Total: ₹{total}")
# else:
#     st.warning("Please enter your username to continue.")


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os
from datetime import datetime

DB_PATH = "expenses.db"

# ─── Database Setup ───────────────────────────────────────────────────────────

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT    NOT NULL,
                date     TEXT    NOT NULL,
                category TEXT    NOT NULL,
                amount   REAL    NOT NULL,
                note     TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                username TEXT PRIMARY KEY,
                amount   REAL NOT NULL
            )
        """)

# ─── Expense Operations ───────────────────────────────────────────────────────

def add_expense(username, category, amount, note):
    date = datetime.now().strftime("%Y-%m-%d")
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO expenses (username, date, category, amount, note) VALUES (?,?,?,?,?)",
            (username, date, category, amount, note)
        )

def load_data(username):
    with get_conn() as conn:
        df = pd.read_sql_query(
            "SELECT date AS Date, category AS Category, amount AS Amount, note AS Note "
            "FROM expenses WHERE username = ? ORDER BY date",
            conn, params=(username,)
        )
    return df

def clear_data(username):
    with get_conn() as conn:
        conn.execute("DELETE FROM expenses WHERE username = ?", (username,))

# ─── Budget Operations ────────────────────────────────────────────────────────

def save_budget(username, amount):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO budgets (username, amount) VALUES (?,?) "
            "ON CONFLICT(username) DO UPDATE SET amount = excluded.amount",
            (username, amount)
        )

def load_budget(username):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT amount FROM budgets WHERE username = ?", (username,)
        ).fetchone()
    return row["amount"] if row else None

def delete_budget(username):
    with get_conn() as conn:
        conn.execute("DELETE FROM budgets WHERE username = ?", (username,))

# ─── App ──────────────────────────────────────────────────────────────────────

init_db()

st.set_page_config(page_title="💰 My Personal Expenses", layout="centered")
st.title("💰 My Personal Expenses Tracker")

username = st.text_input("Enter your username")

if username:
    menu = ["Add Expense", "Show Summary", "Show Graph", "Clear Data", "Budget & Alerts", "History"]
    choice = st.sidebar.radio("Menu", menu)

    # ── Add Expense ──────────────────────────────────────────────────────────
    if choice == "Add Expense":
        st.subheader("Add New Expense")
        category = st.text_input("Category")
        amount   = st.text_input("Amount")
        note     = st.text_input("Note (optional)")

        if st.button("Add Expense"):
            if not category or not amount:
                st.error("Category and Amount are required!")
            else:
                try:
                    add_expense(username, category, float(amount), note)
                    st.success(f"Expense Added: {category} - ₹{float(amount)}")
                except ValueError:
                    st.error("Amount must be a number!")

    # ── Show Summary ─────────────────────────────────────────────────────────
    elif choice == "Show Summary":
        st.subheader("Expense Summary")
        df = load_data(username)
        if df.empty:
            st.info("No expenses yet!")
        else:
            st.dataframe(df)
            st.write(f"**Total Spent: ₹{df['Amount'].sum():,.2f}**")

    # ── Show Graph ───────────────────────────────────────────────────────────
    elif choice == "Show Graph":
        st.subheader("Expenses by Category")
        graph_choice = st.radio("Graph type", ["Bar Graph", "Line Chart", "Pie Chart"])
        df = load_data(username)

        if df.empty:
            st.info("No expenses to plot!")
        else:
            fig, ax = plt.subplots()

            if graph_choice == "Bar Graph":
                df.groupby("Category")["Amount"].sum().plot(kind="bar", color="skyblue", ax=ax)
                ax.set_title("Expenses by Category")
                ax.set_xlabel("Category")
                ax.set_ylabel("Amount (₹)")

            elif graph_choice == "Line Chart":
                ax.plot(df["Date"], df["Amount"], marker="o")
                ax.set_title("Expenses Over Time")
                ax.set_xlabel("Date")
                ax.set_ylabel("Amount (₹)")
                plt.xticks(rotation=45)

            elif graph_choice == "Pie Chart":
                summary = df.groupby("Category")["Amount"].sum()
                ax.pie(summary, labels=summary.index, autopct="%1.1f%%")
                ax.set_title("Expense Distribution")

            st.pyplot(fig)

    # ── Budget & Alerts ──────────────────────────────────────────────────────
    elif choice == "Budget & Alerts":
        st.subheader("Budget Limit")
        df     = load_data(username)
        budget = load_budget(username)

        if budget is None:
            new_budget = st.number_input("Enter your monthly budget", min_value=0.0, step=100.0)
            if st.button("Save Budget"):
                save_budget(username, new_budget)
                st.success(f"Budget set: ₹{new_budget:,.2f}")
                st.rerun()
        else:
            st.info(f"Your monthly budget: ₹{budget:,.2f}")
            total_spent = df["Amount"].sum()
            st.write(f"Total amount spent: ₹{total_spent:,.2f}")

            if total_spent > budget:
                st.error("⚠️ You have crossed your budget!")
            else:
                st.success(f"✅ Within budget. Remaining: ₹{budget - total_spent:,.2f}")

            if st.button("Reset Budget"):
                delete_budget(username)
                st.warning("Budget has been reset!")
                st.rerun()

    # ── Clear Data ───────────────────────────────────────────────────────────
    elif choice == "Clear Data":
        st.subheader("🗑 Clear All Expenses")
        if st.button("Clear All Data"):
            clear_data(username)
            st.success("All expenses cleared!")

    # ── History ──────────────────────────────────────────────────────────────
    elif choice == "History":
        st.subheader("📜 Expense History")
        df = load_data(username)

        if df.empty:
            st.info("No history available!")
        else:
            df["Date"] = pd.to_datetime(df["Date"])

            st.markdown("### 🔍 Filter Options")
            start_date       = st.date_input("Start Date", df["Date"].min())
            end_date         = st.date_input("End Date",   df["Date"].max())
            categories       = df["Category"].unique().tolist()
            selected_category = st.selectbox("Select Category", ["All"] + categories)

            filtered_df = df[
                (df["Date"] >= pd.to_datetime(start_date)) &
                (df["Date"] <= pd.to_datetime(end_date))
            ]
            if selected_category != "All":
                filtered_df = filtered_df[filtered_df["Category"] == selected_category]

            st.dataframe(filtered_df)
            st.write(f"### 💰 Filtered Total: ₹{filtered_df['Amount'].sum():,.2f}")

else:
    st.warning("Please enter your username to continue.")