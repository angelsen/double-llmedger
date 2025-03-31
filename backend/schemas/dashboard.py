from datetime import datetime

from pydantic import BaseModel


# Dashboard response schema
class Transaction(BaseModel):
    id: str
    date: datetime
    amount: float
    type: str
    description: str


class DashboardData(BaseModel):
    account_balance: float
    upcoming_bills: float
    monthly_savings: float
    recent_transactions: list[Transaction]
    account_name: str
