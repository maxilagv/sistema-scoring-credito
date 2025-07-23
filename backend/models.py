from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class CreditApplication(Base):
    __tablename__ = "credit_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    marital_status = Column(String, nullable=False)
    gender = Column(String)
    nationality = Column(String)
    monthly_income = Column(Float, nullable=False)
    monthly_expense = Column(Float, nullable=False)
    debt_percentage = Column(Float, nullable=False)
    active_debts = Column(Boolean, nullable=False)
    previous_loans = Column(Integer, nullable=False)
    late_payments = Column(Integer, nullable=False)
    active_credit_cards = Column(Boolean, nullable=False)
    spending_behavior = Column(String)
    payment_delay = Column(Float, default=0)
    average_balance = Column(Float, default=0)
    score = Column(Integer)
    risk_level = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
