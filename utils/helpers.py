import pandas as pd
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataHelper:
    """Data Helper Functions"""
    
    @staticmethod
    def format_currency(amount: float) -> str:
        """Format amount as currency"""
        return f"${amount:,.2f}"
    
    @staticmethod
    def format_datetime(dt: datetime) -> str:
        """Format datetime to readable string"""
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def get_risk_color(risk_level: str) -> str:
        """Get color for risk level"""
        colors = {
            'High Risk': '#FF4444',
            'Medium Risk': '#FFA500',
            'Low Risk': '#4CAF50'
        }
        return colors.get(risk_level, '#808080')
    
    @staticmethod
    def get_transaction_icon(transaction_type: str) -> str:
        """Get icon emoji for transaction type"""
        icons = {
            'Deposit': '📥',
            'Withdrawal': '📤',
            'Transfer': '🔄',
            'Phone Recharge': '📱',
            'Loan Repayment': '💳'
        }
        return icons.get(transaction_type, '💰')
    
    @staticmethod
    def create_transactions_dataframe(transactions: list) -> pd.DataFrame:
        """Create DataFrame from transactions list"""
        try:
            df = pd.DataFrame(transactions)
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception as e:
            logger.error(f"Error creating DataFrame: {e}")
            return pd.DataFrame()
