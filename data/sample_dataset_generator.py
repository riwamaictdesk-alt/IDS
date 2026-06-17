#!/usr/bin/env python3
"""
Generate sample microfinance dataset for model training
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sample_data(n_records=1000, random_seed=42):
    """
    Generate synthetic microfinance dataset
    """
    np.random.seed(random_seed)
    
    data = {
        'customer_id': [f'CUST_{i:05d}' for i in range(n_records)],
        'age': np.random.randint(18, 70, n_records),
        'gender': np.random.choice(['Male', 'Female'], n_records),
        'income': np.random.lognormal(10, 1, n_records),
        'num_dependents': np.random.randint(0, 6, n_records),
        'employment_status': np.random.choice(['employed', 'self_employed', 'unemployed'], n_records),
        'loan_amount': np.random.lognormal(9, 1.5, n_records),
        'loan_tenure': np.random.choice([6, 12, 24, 36, 48, 60], n_records),
        'previous_defaults': np.random.choice([0, 0, 0, 0, 1, 2], n_records),  # Weighted towards 0
        'transaction_frequency': np.random.randint(1, 100, n_records),
        'average_monthly_balance': np.random.lognormal(9, 1.2, n_records),
        'loan_purpose': np.random.choice(['business', 'personal', 'education', 'agriculture'], n_records),
    }
    
    # Generate target variable (default_status) based on features
    # Higher default risk with:
    # - Lower income
    # - More dependents
    # - Previous defaults
    # - Lower balance
    
    df = pd.DataFrame(data)
    
    # Create default probability based on features
    default_prob = (
        0.1 +  # Base probability
        (np.log(df['income'].max()) - np.log(df['income'])) / 10 * 0.3 +  # Income inverse
        df['num_dependents'] * 0.05 +  # Dependents
        df['previous_defaults'] * 0.2 +  # History
        (np.log(df['average_monthly_balance'].max()) - np.log(df['average_monthly_balance'])) / 10 * 0.2  # Balance inverse
    )
    
    # Clip to valid probability range
    default_prob = np.clip(default_prob, 0, 1)
    
    # Generate binary target
    df['default_status'] = (np.random.random(n_records) < default_prob).astype(int)
    
    return df

if __name__ == "__main__":
    print("Generating sample microfinance dataset...")
    
    # Generate data
    df = generate_sample_data(n_records=1000)
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Save to CSV
    output_path = 'data/microfinance_data.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\n✅ Dataset generated successfully!")
    print(f"📁 Saved to: {output_path}")
    print(f"📊 Shape: {df.shape}")
    print(f"\nDataset Summary:")
    print(df.describe())
    print(f"\nDefault Distribution:")
    print(df['default_status'].value_counts())
    print(f"\nDefault Rate: {df['default_status'].mean():.2%}")
