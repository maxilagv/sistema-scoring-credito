from pydantic import BaseModel, Field
from typing import Optional

class CreditInput(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., gt=0, le=120)
    marital_status: str = Field(..., min_length=1)
    gender: Optional[str] = None
    nationality: str = Field(..., min_length=1)
    monthly_income: float = Field(..., gt=0)
    monthly_expense: float = Field(..., gt=0)
    debt_percentage: float = Field(..., ge=0, le=100)
    active_debts: bool
    previous_loans: int = Field(..., ge=0)
    late_payments: int = Field(..., ge=0)
    active_credit_cards: bool
    spending_behavior: str = Field(..., min_length=1)
    payment_delay: Optional[float] = Field(default=0, ge=0)
    average_balance: Optional[float] = Field(default=0, ge=0)

class CreditScoreResponse(BaseModel):
    name: str
    risk_level: str
    score: int
    explanation: str
    factors: dict

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
