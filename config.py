import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application Configuration"""
    
    # MongoDB Configuration
    MONGODB_URI = os.getenv('MONGODB_URI')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'microfinance_db')
    
    # Collections
    USERS_COLLECTION = 'users'
    CUSTOMERS_COLLECTION = 'customers'
    TRANSACTIONS_COLLECTION = 'transactions'
    LOANS_COLLECTION = 'loans'
    PREDICTIONS_COLLECTION = 'predictions'
    
    # Application Settings
    APP_NAME = os.getenv('APP_NAME', 'Microfinance Loan Default Prediction System')
    APP_SECRET = os.getenv('APP_SECRET')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    
    # Model Configuration
    MODEL_PATH = './models/best_model.pkl'
    DATASET_PATH = './data/microfinance_data.csv'
    
    # Feature Names for Model
    FEATURE_COLUMNS = [
        'age', 'income', 'loan_amount', 'loan_tenure',
        'previous_defaults', 'transaction_frequency',
        'average_monthly_balance', 'num_dependents',
        'employment_status', 'loan_purpose'
    ]
    
    # Transaction Types
    TRANSACTION_TYPES = ['Deposit', 'Withdrawal', 'Transfer', 'Phone Recharge', 'Loan Repayment']
