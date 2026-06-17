import uuid
from datetime import datetime
from database.db_connection import MongoDBConnection
from database.models import Prediction
from ml_models.predictor import LoanDefaultPredictor
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PredictionService:
    """Loan Default Prediction Service"""
    
    def __init__(self):
        self.db = MongoDBConnection()
        self.predictions_col = self.db.get_collection('predictions')
        self.customers_col = self.db.get_collection('customers')
        self.transactions_col = self.db.get_collection('transactions')
        self.predictor = LoanDefaultPredictor(Config.MODEL_PATH)
    
    def extract_features_from_customer(self, customer_id: str) -> list:
        """Extract features from customer data and transaction history"""
        try:
            customer = self.customers_col.find_one({'customer_id': customer_id})
            if not customer:
                logger.error(f"Customer not found: {customer_id}")
                return None
            
            # Get transaction history
            transactions = list(self.transactions_col.find({'customer_id': customer_id}))
            
            # Calculate features
            features = []
            
            # 1. Age
            features.append(customer.get('age', 30))
            
            # 2. Income
            features.append(customer.get('monthly_income', 0))
            
            # 3. Loan Amount (placeholder - would come from loan application)
            features.append(customer.get('account_balance', 0) * 2)  # Assume can borrow 2x balance
            
            # 4. Loan Tenure (months) - placeholder
            features.append(12)
            
            # 5. Previous Defaults - placeholder
            features.append(0)
            
            # 6. Transaction Frequency
            tx_count = len(transactions)
            features.append(tx_count)
            
            # 7. Average Monthly Balance
            if tx_count > 0:
                avg_balance = sum([t.get('balance_after', 0) for t in transactions]) / tx_count
            else:
                avg_balance = customer.get('account_balance', 0)
            features.append(avg_balance)
            
            # 8. Number of Dependents
            features.append(customer.get('num_dependents', 0))
            
            # 9. Employment Status (convert to numeric)
            employment_status = customer.get('employment_status', 'employed')
            employment_map = {'employed': 1, 'self_employed': 2, 'unemployed': 0}
            features.append(employment_map.get(employment_status, 1))
            
            # 10. Loan Purpose (convert to numeric)
            loan_purpose = customer.get('loan_purpose', 'business')
            purpose_map = {'business': 1, 'personal': 2, 'education': 3, 'agriculture': 4}
            features.append(purpose_map.get(loan_purpose, 1))
            
            logger.info(f"Features extracted for customer {customer_id}: {features}")
            return features
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            return None
    
    def predict_default_risk(self, customer_id: str, loan_id: str = None) -> dict:
        """Predict loan default risk for a customer"""
        try:
            features = self.extract_features_from_customer(customer_id)
            if features is None:
                return {'success': False, 'message': 'Could not extract features'}
            
            # Make prediction
            prediction_result = self.predictor.predict(features)
            
            if prediction_result is None:
                return {'success': False, 'message': 'Prediction failed'}
            
            # Save prediction to database
            prediction_id = str(uuid.uuid4())
            prediction = Prediction(
                prediction_id=prediction_id,
                customer_id=customer_id,
                loan_id=loan_id,
                prediction_score=prediction_result['probability'],
                prediction_label=prediction_result['risk_level'],
                model_used='best_model',
                features_used={
                    'age': features[0],
                    'income': features[1],
                    'loan_amount': features[2],
                    'transaction_frequency': features[5],
                    'average_balance': features[6]
                },
                confidence=prediction_result['confidence']
            )
            
            self.predictions_col.insert_one(prediction.dict())
            logger.info(f"Prediction saved: {prediction_id}")
            
            return {
                'success': True,
                'prediction_id': prediction_id,
                'customer_id': customer_id,
                'prediction_score': prediction_result['probability'],
                'risk_level': prediction_result['risk_level'],
                'confidence': prediction_result['confidence']
            }
        except Exception as e:
            logger.error(f"Error in default risk prediction: {e}")
            return {'success': False, 'message': str(e)}
    
    def get_prediction_history(self, customer_id: str, limit: int = 10) -> list:
        """Get prediction history for a customer"""
        try:
            predictions = list(self.predictions_col.find(
                {'customer_id': customer_id}
            ).sort('created_at', -1).limit(limit))
            return predictions
        except Exception as e:
            logger.error(f"Error retrieving prediction history: {e}")
            return []
