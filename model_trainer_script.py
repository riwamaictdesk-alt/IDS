#!/usr/bin/env python3
"""
Standalone script to train and evaluate ML models
Usage: python model_trainer_script.py --data <dataset_path> --output <output_directory>
"""

import sys
import argparse
import os
from ml_models.model_trainer import ModelTrainer
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    parser = argparse.ArgumentParser(description="Train and evaluate loan default prediction models")
    parser.add_argument('--data', required=True, help='Path to the dataset CSV file')
    parser.add_argument('--output', default='./models', help='Output directory for models')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    print("\n" + "="*60)
    print("Microfinance Loan Default Prediction Model Training")
    print("="*60 + "\n")
    
    # Initialize trainer
    trainer = ModelTrainer(args.data)
    
    # Load data
    print("[1/5] Loading dataset...")
    if not trainer.load_data():
        print("Failed to load dataset")
        sys.exit(1)
    
    # Preprocess data
    print("[2/5] Preprocessing data...")
    if not trainer.preprocess_data():
        print("Failed to preprocess data")
        sys.exit(1)
    
    # Train models
    print("[3/5] Training models...")
    print("  - Training Logistic Regression...")
    trainer.train_logistic_regression()
    print("  - Training Decision Tree...")
    trainer.train_decision_tree()
    print("  - Training Random Forest...")
    trainer.train_random_forest()
    
    # Evaluate models
    print("[4/5] Evaluating models...")
    trainer.evaluate_all_models()
    
    # Display results
    print("[5/5] Results Summary")
    print("\n" + "-"*60)
    print("MODEL PERFORMANCE COMPARISON")
    print("-"*60 + "\n")
    
    results = trainer.get_results_summary()
    results_df = pd.DataFrame(results).T
    print(results_df.to_string())
    
    # Find and save best model
    best_model_name, best_model = trainer.get_best_model()
    print(f"\n\n✅ BEST MODEL: {best_model_name}")
    print("-"*60)
    print(f"Accuracy:  {results[best_model_name]['Accuracy']:.4f}")
    print(f"Precision: {results[best_model_name]['Precision']:.4f}")
    print(f"Recall:    {results[best_model_name]['Recall']:.4f}")
    print(f"F1 Score:  {results[best_model_name]['F1 Score']:.4f}")
    print(f"ROC-AUC:   {results[best_model_name]['ROC-AUC']:.4f}")
    
    # Save best model
    output_path = os.path.join(args.output, 'best_model.pkl')
    trainer.save_model(best_model_name, output_path)
    print(f"\n📁 Model saved to: {output_path}")
    
    # Save all models
    for model_name in trainer.models.keys():
        model_path = os.path.join(args.output, f"{model_name.lower().replace(' ', '_')}.pkl")
        trainer.save_model(model_name, model_path)
    
    print("\n" + "="*60)
    print("Training completed successfully!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
