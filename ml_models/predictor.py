import pickle
import numpy as np
import logging
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoanDefaultPredictor:
    """Loan Default Prediction Engine"""
    
    def __init__(self, model_path):
        self.model = None
        self.scaler = StandardScaler()
        self.load_model(model_path)
    
    def load_model(self, model_path):
        """Load pre-trained model from pickle file"""
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            logger.info(f"Model loaded successfully from {model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def predict(self, features):
        """Make prediction on new data
        
        Args:
            features: numpy array or list of feature values
        
        Returns:
            dict with prediction, probability, and risk level
        """
        try:
            features_array = np.array(features).reshape(1, -1)
            
            # Make prediction
            prediction = self.model.predict(features_array)[0]
            
            # Get probability
            if hasattr(self.model, 'predict_proba'):
                probability = self.model.predict_proba(features_array)[0][1]
            else:
                probability = float(prediction)
            
            # Determine risk level
            if probability >= 0.7:
                risk_level = 'High Risk'
            elif probability >= 0.4:
                risk_level = 'Medium Risk'
            else:
                risk_level = 'Low Risk'
            
            return {
                'prediction': int(prediction),
                'probability': float(probability),
                'risk_level': risk_level,
                'confidence': max(self.model.predict_proba(features_array)[0]) if hasattr(self.model, 'predict_proba') else probability
            }
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            return None
    
    def batch_predict(self, features_list):
        """Make predictions for multiple records
        
        Args:
            features_list: list of feature arrays
        
        Returns:
            list of predictions
        """
        try:
            predictions = []
            for features in features_list:
                pred = self.predict(features)
                if pred:
                    predictions.append(pred)
            return predictions
        except Exception as e:
            logger.error(f"Error in batch prediction: {e}")
            return None
