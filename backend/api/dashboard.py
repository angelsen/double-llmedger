import random
from datetime import datetime, timedelta

from core.security import get_current_user, invalidate_all_user_sessions
from db.database import get_db
from fastapi import APIRouter, Depends, Request, Response
from schemas.dashboard import DashboardData, Transaction
from schemas.user import AuthResponse
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/dashboard-data", response_model=DashboardData)
async def get_dashboard_data(
    request: Request, response: Response, user: AuthResponse = Depends(get_current_user)
):
    """Return randomized dashboard data for the authenticated user"""

    # Generate random financial data (same as original implementation)
    account_balance = round(random.uniform(5000, 15000), 2)
    upcoming_bills = round(random.uniform(500, 3000), 2)
    monthly_savings = round(random.uniform(200, 1000), 2)

    # Generate fake recent transactions
    transaction_types = [
        "Grocery",
        "Rent",
        "Utilities",
        "Entertainment",
        "Income",
        "Shopping",
    ]
    recent_transactions = []

    now = datetime.now()
    for i in range(5):
        txn_date = now - timedelta(days=random.randint(0, 14))
        txn_amount = round(random.uniform(-500, 1000), 2)
        txn_type = random.choice(transaction_types)

        recent_transactions.append(
            Transaction(
                id=f"txn-{i + 1}",
                date=txn_date,
                amount=txn_amount,
                type=txn_type,
                description=f"{txn_type} {'payment' if txn_amount < 0 else 'deposit'}",
            )
        )

    return DashboardData(
        account_balance=account_balance,
        upcoming_bills=upcoming_bills,
        monthly_savings=monthly_savings,
        recent_transactions=recent_transactions,
        account_name=f"{user.username}'s Account",
    )


@router.post("/security/logout-all-devices")
async def logout_all_devices(
    request: Request,
    user: AuthResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Invalidate all sessions for the current user"""
    count = invalidate_all_user_sessions(user.user_id, db)
    return {
        "success": True,
        "message": f"Successfully invalidated {count} session(s)",
        "invalidated_count": count,
    }
