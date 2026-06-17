import uuid
from datetime import datetime
from database.db_connection import MongoDBConnection
from database.models import Transaction
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TransactionService:
    """Transaction Management Service"""
    
    def __init__(self):
        self.db = MongoDBConnection()
        self.transactions_col = self.db.get_collection('transactions')
        self.customers_col = self.db.get_collection('customers')
    
    def deposit(self, customer_id: str, amount: float, description: str = "Deposit") -> dict:
        """Process deposit transaction"""
        try:
            if amount <= 0:
                return {'success': False, 'message': 'Amount must be positive'}
            
            customer = self.customers_col.find_one({'customer_id': customer_id})
            if not customer:
                return {'success': False, 'message': 'Customer not found'}
            
            new_balance = customer.get('account_balance', 0) + amount
            transaction_id = str(uuid.uuid4())
            
            transaction = Transaction(
                transaction_id=transaction_id,
                customer_id=customer_id,
                transaction_type='Deposit',
                amount=amount,
                description=description,
                status='success',
                balance_after=new_balance
            )
            
            self.transactions_col.insert_one(transaction.dict())
            self.customers_col.update_one(
                {'customer_id': customer_id},
                {'$set': {'account_balance': new_balance}}
            )
            
            logger.info(f"Deposit processed: {transaction_id}, Amount: {amount}")
            return {'success': True, 'transaction_id': transaction_id, 'new_balance': new_balance}
        except Exception as e:
            logger.error(f"Error processing deposit: {e}")
            return {'success': False, 'message': str(e)}
    
    def withdraw(self, customer_id: str, amount: float, description: str = "Withdrawal") -> dict:
        """Process withdrawal transaction"""
        try:
            if amount <= 0:
                return {'success': False, 'message': 'Amount must be positive'}
            
            customer = self.customers_col.find_one({'customer_id': customer_id})
            if not customer:
                return {'success': False, 'message': 'Customer not found'}
            
            current_balance = customer.get('account_balance', 0)
            if amount > current_balance:
                return {'success': False, 'message': 'Insufficient funds'}
            
            new_balance = current_balance - amount
            transaction_id = str(uuid.uuid4())
            
            transaction = Transaction(
                transaction_id=transaction_id,
                customer_id=customer_id,
                transaction_type='Withdrawal',
                amount=amount,
                description=description,
                status='success',
                balance_after=new_balance
            )
            
            self.transactions_col.insert_one(transaction.dict())
            self.customers_col.update_one(
                {'customer_id': customer_id},
                {'$set': {'account_balance': new_balance}}
            )
            
            logger.info(f"Withdrawal processed: {transaction_id}, Amount: {amount}")
            return {'success': True, 'transaction_id': transaction_id, 'new_balance': new_balance}
        except Exception as e:
            logger.error(f"Error processing withdrawal: {e}")
            return {'success': False, 'message': str(e)}
    
    def transfer(self, from_customer_id: str, to_customer_id: str, amount: float, description: str = "Transfer") -> dict:
        """Process transfer transaction between customers"""
        try:
            if amount <= 0:
                return {'success': False, 'message': 'Amount must be positive'}
            
            from_customer = self.customers_col.find_one({'customer_id': from_customer_id})
            to_customer = self.customers_col.find_one({'customer_id': to_customer_id})
            
            if not from_customer or not to_customer:
                return {'success': False, 'message': 'Customer not found'}
            
            from_balance = from_customer.get('account_balance', 0)
            if amount > from_balance:
                return {'success': False, 'message': 'Insufficient funds'}
            
            transaction_id = str(uuid.uuid4())
            from_new_balance = from_balance - amount
            to_new_balance = to_customer.get('account_balance', 0) + amount
            
            # Record transaction for sender
            transaction_from = Transaction(
                transaction_id=transaction_id,
                customer_id=from_customer_id,
                transaction_type='Transfer',
                amount=-amount,
                description=f"Transfer to {to_customer_id}: {description}",
                status='success',
                balance_after=from_new_balance
            )
            
            # Record transaction for receiver
            transaction_to = Transaction(
                transaction_id=str(uuid.uuid4()),
                customer_id=to_customer_id,
                transaction_type='Transfer',
                amount=amount,
                description=f"Transfer from {from_customer_id}: {description}",
                status='success',
                balance_after=to_new_balance
            )
            
            self.transactions_col.insert_one(transaction_from.dict())
            self.transactions_col.insert_one(transaction_to.dict())
            
            self.customers_col.update_one(
                {'customer_id': from_customer_id},
                {'$set': {'account_balance': from_new_balance}}
            )
            self.customers_col.update_one(
                {'customer_id': to_customer_id},
                {'$set': {'account_balance': to_new_balance}}
            )
            
            logger.info(f"Transfer processed: {transaction_id}, Amount: {amount}")
            return {'success': True, 'transaction_id': transaction_id, 'from_balance': from_new_balance, 'to_balance': to_new_balance}
        except Exception as e:
            logger.error(f"Error processing transfer: {e}")
            return {'success': False, 'message': str(e)}
    
    def phone_recharge(self, customer_id: str, amount: float, phone_number: str) -> dict:
        """Process phone recharge transaction"""
        try:
            if amount <= 0:
                return {'success': False, 'message': 'Amount must be positive'}
            
            customer = self.customers_col.find_one({'customer_id': customer_id})
            if not customer:
                return {'success': False, 'message': 'Customer not found'}
            
            current_balance = customer.get('account_balance', 0)
            if amount > current_balance:
                return {'success': False, 'message': 'Insufficient funds'}
            
            new_balance = current_balance - amount
            transaction_id = str(uuid.uuid4())
            
            transaction = Transaction(
                transaction_id=transaction_id,
                customer_id=customer_id,
                transaction_type='Phone Recharge',
                amount=amount,
                description=f"Phone recharge for {phone_number}",
                status='success',
                balance_after=new_balance
            )
            
            self.transactions_col.insert_one(transaction.dict())
            self.customers_col.update_one(
                {'customer_id': customer_id},
                {'$set': {'account_balance': new_balance}}
            )
            
            logger.info(f"Phone recharge processed: {transaction_id}, Phone: {phone_number}")
            return {'success': True, 'transaction_id': transaction_id, 'new_balance': new_balance}
        except Exception as e:
            logger.error(f"Error processing phone recharge: {e}")
            return {'success': False, 'message': str(e)}
    
    def get_transaction_history(self, customer_id: str, limit: int = 50) -> list:
        """Get transaction history for a customer"""
        try:
            transactions = list(self.transactions_col.find(
                {'customer_id': customer_id}
            ).sort('timestamp', -1).limit(limit))
            return transactions
        except Exception as e:
            logger.error(f"Error retrieving transaction history: {e}")
            return []
    
    def get_transaction_stats(self, customer_id: str) -> dict:
        """Get transaction statistics for a customer"""
        try:
            transactions = self.transactions_col.find({'customer_id': customer_id})
            stats = {
                'total_deposits': 0,
                'total_withdrawals': 0,
                'total_transfers': 0,
                'total_recharges': 0,
                'transaction_count': 0
            }
            
            for tx in transactions:
                stats['transaction_count'] += 1
                if tx['transaction_type'] == 'Deposit':
                    stats['total_deposits'] += tx['amount']
                elif tx['transaction_type'] == 'Withdrawal':
                    stats['total_withdrawals'] += tx['amount']
                elif tx['transaction_type'] == 'Transfer':
                    if tx['amount'] > 0:
                        stats['total_transfers'] += tx['amount']
                elif tx['transaction_type'] == 'Phone Recharge':
                    stats['total_recharges'] += tx['amount']
            
            return stats
        except Exception as e:
            logger.error(f"Error calculating transaction stats: {e}")
            return {}
