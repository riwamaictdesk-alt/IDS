import uuid
from datetime import datetime
from database.db_connection import MongoDBConnection
from database.models import Customer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomerService:
    """Customer Management Service"""
    
    def __init__(self):
        self.db = MongoDBConnection()
        self.customers_col = self.db.get_collection('customers')
    
    def create_customer(self, customer_data: dict) -> dict:
        """Create new customer"""
        try:
            customer_id = str(uuid.uuid4())
            customer = Customer(
                customer_id=customer_id,
                **customer_data,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            result = self.customers_col.insert_one(customer.dict())
            logger.info(f"Customer created: {customer_id}")
            return customer.dict()
        except Exception as e:
            logger.error(f"Error creating customer: {e}")
            return None
    
    def get_customer(self, customer_id: str) -> dict:
        """Retrieve customer by ID"""
        try:
            customer = self.customers_col.find_one({'customer_id': customer_id})
            return customer
        except Exception as e:
            logger.error(f"Error retrieving customer: {e}")
            return None
    
    def get_all_customers(self) -> list:
        """Retrieve all customers"""
        try:
            customers = list(self.customers_col.find({}))
            return customers
        except Exception as e:
            logger.error(f"Error retrieving customers: {e}")
            return []
    
    def update_customer(self, customer_id: str, update_data: dict) -> bool:
        """Update customer information"""
        try:
            update_data['updated_at'] = datetime.utcnow()
            result = self.customers_col.update_one(
                {'customer_id': customer_id},
                {'$set': update_data}
            )
            logger.info(f"Customer updated: {customer_id}")
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating customer: {e}")
            return False
    
    def get_customer_transactions(self, customer_id: str) -> list:
        """Get all transactions for a customer"""
        try:
            transactions_col = self.db.get_collection('transactions')
            transactions = list(transactions_col.find({'customer_id': customer_id}).sort('timestamp', -1))
            return transactions
        except Exception as e:
            logger.error(f"Error retrieving transactions: {e}")
            return []
    
    def get_customer_loans(self, customer_id: str) -> list:
        """Get all loans for a customer"""
        try:
            loans_col = self.db.get_collection('loans')
            loans = list(loans_col.find({'customer_id': customer_id}))
            return loans
        except Exception as e:
            logger.error(f"Error retrieving loans: {e}")
            return []
