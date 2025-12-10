from contextlib import contextmanager
import os
import pandas as pd

from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from db.models import engine, User, Expense


base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, "roomie_expenses.db")

Session = sessionmaker(bind=engine)
session = Session()


@contextmanager
def get_db_session():
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def bulk_add_expense_to_db(expenses_data: list) -> int:
    try:
        objs = [Expense(**rec) for rec in expenses_data]
        session.add_all(objs)
        session.commit()

        return len(objs)

    except SQLAlchemyError:
        session.rollback()

    finally:
        session.close()
    return 0


def add_expense_to_db(source: str, amount: float, added_by: int, month: str, year: int):
    new_expense = Expense(
        source_of_expense = source,
        amount = amount,
        added_by_id = added_by,
        month = month,
        year = year,
        created_at = datetime.utcnow(),
        updated_at = datetime.utcnow()
    )

    session.add(new_expense)
    session.commit()
    expense_id = new_expense.id
    session.close()
    return expense_id


def load_user_totals(selected_month: str = None, selected_year: int = None) -> pd.DataFrame:
    """
    Returns DataFrame with: user_id, name, total_amount, num_expenses
    """

    expenses_data = []
    expenses_query = (
        session.query(
            Expense.added_by_id.label("added_by_id"),
            User.name.label("name"),
            func.sum(Expense.amount).label("total_amount"),
            func.count(Expense.id).label("num_expenses")
        )
        .join(User, User.id == Expense.added_by_id)
    )

    if selected_month and selected_month != "All":
        expenses_query = expenses_query.filter(Expense.month == selected_month)

    if selected_year and selected_year != "All":
        expenses_query = expenses_query.filter(Expense.year == int(selected_year))

    expenses_query = (
        expenses_query
        .group_by(Expense.added_by_id, User.name)
        .all()
    )

    expenses = expenses_query
    for expense in expenses:
        expenses_data.append(
            {
                "user_id": expense.added_by_id, 
                "name": expense.name, 
                "total_amount": float(expense.total_amount), 
                "num_expenses": expense.num_expenses
            }
        )
    
    if not expenses_data:
        _, users_dict = get_all_users()
        for name, id in users_dict.items():
            expenses_data.append(
                {
                    "user_id": id,
                    "name": name,
                    "total_amount": 0, 
                    "num_expenses": 0,
                }
            )

    return pd.DataFrame(expenses_data)


def load_expenses(user_id: int, month: str = None, year: int = None) -> pd.DataFrame:
    """Return all expenses as DataFrame. Replace demo with DB query."""
    user_expenses = []
    if user_id and user_id != 'All':
        expenses_query = (
            session.query(Expense)
        ).filter(Expense.added_by_id == int(user_id))
    else:
        expenses_query = (
            session.query(Expense)
        )

    expenses_query = expenses_query.filter(Expense.month == month) if month and month != "All" else expenses_query
    expenses_query = expenses_query.filter(Expense.year == year) if year and year != "All" else expenses_query
    expenses_query = expenses_query.all()

    for user_expense in expenses_query:
        user_expenses.append(
            {
                "id": user_expense.id, 
                "source_of_expense": user_expense.source_of_expense,
                "amount": user_expense.amount, 
                "month": user_expense.month, 
                "year": user_expense.year, 
                "created_at": user_expense.created_at
            }
        )

    return pd.DataFrame(user_expenses)

def update_expense_in_db(expense_id: int, payload: dict):
    """Edit the timings, priority, status or invitees of a Task"""
    expense = (
        session.query(Expense)
        .filter_by(id=expense_id)
        .first()
    )

    if expense:
        expense.source_of_expense = payload["source_of_expense"]
        expense.amount = payload["amount"]
        session.commit()
        session.close()
        return expense_id


# ---------- User Helper Functions ----------
def get_all_users():
    with get_db_session() as db:
        user_query = (
            db.query(User).all()
        )

        users_list = []
        users_dict = {}
        for user in user_query:
            users_list.append(user.name)
            users_dict[user.name] = user.id 

        return users_list, users_dict
