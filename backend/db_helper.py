# CRUD stands for Create, Retrieve, Update, Delete
import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

logger = setup_logger('db_helper')


@contextmanager
def get_db_cursor(commit = False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()

def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with date: {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date=%s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses

def delete_expense_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with date: {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))

def insert_expense(expense_date, amount,category,notes):
    logger.info(f"insert_expense called with date: {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date,amount,category,notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )

def fetch_expense_summary(start_date,end_date):
    logger.info(f"fetch_expense_summary called with start: {start_date} end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
        '''SELECT category, SUM(amount) as total
           FROM expenses
           WHERE expense_date
           BETWEEN %s AND %s
           GROUP BY category;''',
    (start_date,end_date)
        )
        data = cursor.fetchall()
        return data

def fetch_expense_summary_by_months():
    logger.info(f"fetch_expense_summary_by_months called")
    with get_db_cursor() as cursor:
        cursor.execute(
        '''SELECT DATE_FORMAT(expense_date, '%Y-%m') AS month, SUM(amount) as total
           FROM expenses
           GROUP BY month
           ORDER BY month;
        '''
        )
        data = cursor.fetchall()
        return data

def fetch_expense_summary_by_method_of_payment(start_date,end_date):
    logger.info(f"fetch_expense_summary_by_method_of_payment called with start: {start_date} end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
        '''SELECT method_of_payment, SUM(amount) as total
           FROM expenses
           WHERE expense_date
           BETWEEN %s AND %s
           GROUP BY method_of_payment;''',
    (start_date,end_date)
        )
        data = cursor.fetchall()
        return data

if __name__ == '__main__':
    # expenses = fetch_expenses_for_date("2024-09-30")
    # print(expenses)
    #insert_expense("2025-06-15",48,"food","fathers day")
    #delete_expense_for_date('2025-06-15')
    summary = fetch_expense_summary("2024-08-01", "2024-08-05")
    for record in summary:
        print(record)