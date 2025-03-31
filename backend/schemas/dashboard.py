"""
Pydantic schemas for dashboard-related data structures.

This module defines the data models for dashboard entities, used for
response serialization and data validation.
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Transaction(BaseModel):
    """Schema for financial transaction data."""
    id: str = Field(..., description="Unique transaction identifier")
    date: datetime = Field(..., description="Transaction date and time")
    amount: float = Field(
        ...,
        description="Transaction amount (positive for income, negative for expense)"
    )
    type: str = Field(..., description="Transaction category or type")
    description: str = Field(..., description="Transaction description or memo")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "txn-123",
                "date": "2023-01-01T12:30:00Z",
                "amount": -75.50,
                "type": "Grocery",
                "description": "Grocery payment"
            }
        }
    )


class DashboardData(BaseModel):
    """Schema for dashboard overview data."""
    account_balance: float = Field(..., description="Current account balance")
    upcoming_bills: float = Field(..., description="Sum of upcoming bills")
    monthly_savings: float = Field(..., description="Monthly savings amount")
    recent_transactions: list[Transaction] = Field(
        ...,
        description="List of recent transactions"
    )
    account_name: str = Field(..., description="Account display name")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "account_balance": 1250.75,
                "upcoming_bills": 450.00,
                "monthly_savings": 300.00,
                "recent_transactions": [
                    {
                        "id": "txn-123",
                        "date": "2023-01-01T12:30:00Z",
                        "amount": -75.50,
                        "type": "Grocery",
                        "description": "Grocery payment"
                    }
                ],
                "account_name": "John's Account"
            }
        }
    )
