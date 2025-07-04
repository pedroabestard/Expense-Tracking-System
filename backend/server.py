from fastapi import FastAPI, HTTPException
from datetime import date
import db_helper
from typing import List, Dict
from pydantic import BaseModel

app = FastAPI()

# schemes of data when consulting:
class Expense(BaseModel):
    amount: float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date: date
    end_date: date

class MonthBreakdown(BaseModel):
    total: float
    percentage: float

@app.get("/expenses/{expense_date}", response_model = List)
def get_expenses(expense_date: date):
    expenses = db_helper.fetch_expenses_for_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from the database")
    return expenses

@app.post("/expenses/{expense_date}", response_model = List)
def add_or_update_expense(expense_date: date, expenses: List[Expense]):
    db_helper.delete_expense_for_date(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)
    return expenses#{"message": "Expenses updated successfully"}

@app.post("/analytics")
def get_analytics(date_range: DateRange):
    data = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from the database")

    total = sum([row['total'] for row in data])

    breakdown = {}
    for row in data:
        percentage = (row['total'] / total) * 100 if total != 0 else 0
        breakdown[row['category']] = {
            "total": row['total'],
            "percentage": percentage
        }
    return breakdown

@app.get("/analyticsbymonths", response_model=Dict[str, MonthBreakdown])
def get_analytics_by_months():
    data = db_helper.fetch_expense_summary_by_months()
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from the database")
    total = sum([row['total'] for row in data])

    breakdown = {}
    for row in data:
        percentage = (row['total'] / total) * 100 if total != 0 else 0
        breakdown[row['month']] = {
            "total": row['total'],
            "percentage": percentage
        }
    return breakdown

@app.post("/analyticsbypayment")
def get_analytics(date_range: DateRange):
    data = db_helper.fetch_expense_summary_by_method_of_payment(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from the database")

    total = sum([row['total'] for row in data])

    breakdown = {}
    for row in data:
        percentage = (row['total'] / total) * 100 if total != 0 else 0
        breakdown[row['method_of_payment']] = {
            "total": row['total'],
            "percentage": percentage
        }
    return breakdown