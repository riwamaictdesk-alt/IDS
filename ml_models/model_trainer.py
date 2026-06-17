import pandas as pd
import numpy as np
import pickle
import logging
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelTrainer:
    """Machine Learning Model Trainer"""
    
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()
        self.models = {}
        self.results = {}
    
    def load_data(self):
        """Load and explore dataset"""
        try:
            self.df = pd.read_csv(self.dataset_path)
            logger.info(f"Dataset loaded: {self.df.shape}")
            logger.info(f"Columns: {self.df.columns.tolist()}")
            logger.info(f"Missing values:\n{self.df.isnull().sum()}")
            return True
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            return False
    
    def preprocess_data(self):
        """Preprocess and prepare data"""
        try:
            # Handle missing values
            self.df = self.df.fillna(self.df.mean())
            
            # Separate features and target
            X = self.df[Config.FEATURE_COLUMNS]
            y = self.df['default_status'] if 'default_status' in self.df.columns else self.df.iloc[:, -1]
            
            # Split data
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Scale features
            self.X_train = self.scaler.fit_transform(self.X_train)
            self.X_test = self.scaler.transform(self.X_test)
            
            logger.info(f"Data preprocessing completed. Train: {self.X_train.shape}, Test: {self.X_test.shape}")
            return True
        except Exception as e:
            logger.error(f"Error in preprocessing: {e}")
            return False
    
    def train_logistic_regression(self):
        """Train Logistic Regression Model"""
        try:
            model = LogisticRegression(max_iter=1000, random_state=42)
            model.fit(self.X_train, self.y_train)
            self.models['Logistic Regression'] = model
            logger.info("Logistic Regression model trained successfully")
            return model
        except Exception as e:
            logger.error(f"Error training Logistic Regression: {e}")
            return None
    
    def train_decision_tree(self):
        """Train Decision Tree Model"""
        try:
            model = DecisionTreeClassifier(max_depth=10, random_state=42)
            model.fit(self.X_train, self.y_train)
            self.models['Decision Tree'] = model
            logger.info("Decision Tree model trained successfully")
            return model
        except Exception as e:
            logger.error(f"Error training Decision Tree: {e}")
            return None
    
    def train_random_forest(self):
        """Train Random Forest Model"""
        try:
            model = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42)
            model.fit(self.X_train, self.y_train)
            self.models['Random Forest'] = model
            logger.info("Random Forest model trained successfully")
            return model
        except Exception as e:
            logger.error(f"Error training Random Forest: {e}")
            return None
    
    def evaluate_model(self, model_name, model):
        """Evaluate model performance"""
        try:
            y_pred = model.predict(self.X_test)
            y_pred_proba = model.predict_proba(self.X_test)[:, 1] if hasattr(model, 'predict_proba') else y_pred
            
            metrics = {
                'Accuracy': accuracy_score(self.y_test, y_pred),
                'Precision': precision_score(self.y_test, y_pred, zero_division=0),
                'Recall': recall_score(self.y_test, y_pred, zero_division=0),
                'F1 Score': f1_score(self.y_test, y_pred, zero_division=0),
                'ROC-AUC': roc_auc_score(self.y_test, y_pred_proba) if hasattr(model, 'predict_proba') else 0
            }
            
            self.results[model_name] = metrics
            logger.info(f"{model_name} Evaluation - {metrics}")
            return metrics
        except Exception as e:
            logger.error(f"Error evaluating {model_name}: {e}")
            return None
    
    def train_all_models(self):
        """Train all three models"""
        self.train_logistic_regression()
        self.train_decision_tree()
        self.train_random_forest()
    
    def evaluate_all_models(self):
        """Evaluate all models"""
        for model_name, model in self.models.items():
            self.evaluate_model(model_name, model)
    
    def get_best_model(self):
        """Get the best performing model based on F1 Score"""
        if not self.results:
            return None
        
        best_model_name = max(self.results.keys(), key=lambda x: self.results[x]['F1 Score'])
        return best_model_name, self.models[best_model_name]
    
    def save_model(self, model_name, output_path):
        """Save model to pickle file"""
        try:
            model = self.models[model_name]
            with open(output_path, 'wb') as f:
                pickle.dump(model, f)
            logger.info(f"{model_name} saved to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            return False
    
    def get_results_summary(self):
        """Get comprehensive results summary"""
        return self.results
