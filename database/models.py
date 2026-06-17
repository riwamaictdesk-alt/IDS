from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field

class User(BaseModel):
    """User Model"""
    user_id: str
    email: str
    password_hash: str
    full_name: str
    role: str  # admin, loan_officer, customer
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

class Customer(BaseModel):
    """Customer Model"""
    customer_id: str
    user_id: str
    age: int
    gender: str
    email: str
    phone: str
    address: str
    employment_status: str  # employed, self_employed, unemployed
    monthly_income: float
    num_dependents: int
    loan_purpose: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    account_balance: float = 0.0

class Transaction(BaseModel):
    """Transaction Model"""
    transaction_id: str
    customer_id: str
    transaction_type: str  # Deposit, Withdrawal, Transfer, Phone Recharge
    amount: float
    description: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str  # success, pending, failed
    balance_after: float

class Loan(BaseModel):
    """Loan Model"""
    loan_id: str
    customer_id: str
    loan_amount: float
    loan_tenure_months: int
    interest_rate: float
    monthly_payment: float
    issue_date: datetime
    maturity_date: datetime
    status: str  # active, completed, defaulted
    remaining_balance: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Prediction(BaseModel):
    """Prediction Model"""
    prediction_id: str
    customer_id: str
    loan_id: Optional[str]
    prediction_score: float  # 0-1, probability of default
    prediction_label: str  # High Risk, Medium Risk, Low Risk
    model_used: str  # logistic_regression, decision_tree, random_forest
    features_used: Dict
    created_at: datetime = Field(default_factory=datetime.utcnow)
    confidence: float
