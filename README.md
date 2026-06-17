# Microfinance Loan Default Prediction System

A comprehensive Streamlit-based application for predicting loan defaults in microfinance institutions using machine learning, integrated with full banking functionality.

## Features

### 1. Loan Default Prediction
- **Multiple ML Models**: Logistic Regression, Decision Tree, Random Forest
- **Comparative Analysis**: Compare model performance across different metrics
- **Risk Assessment**: Real-time loan default risk scoring
- **Transaction-Based Features**: Derives predictions from customer transaction history

### 2. Banking Services
- **Account Management**: View account balance and information
- **Deposit**: Add funds to account
- **Withdrawal**: Withdraw funds with balance verification
- **Transfer**: Send money between customers
- **Phone Recharge**: Mobile phone top-up service

### 3. Customer Dashboard
- **Account Overview**: Real-time balance and account status
- **Transaction History**: Complete transaction records with filtering
- **Transaction Statistics**: Aggregate statistics by transaction type
- **Prediction History**: Track previous loan risk assessments
- **Personal Information**: Manage account details

## Project Structure

```
IDS/
├── app.py                          # Main Streamlit application
├─��� config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── model_trainer_script.py         # ML model training script
│
├── database/
│   ├── db_connection.py           # MongoDB connection handler
│   └── models.py                  # Data models (Pydantic)
│
├── ml_models/
│   ├── model_trainer.py           # Model training pipeline
│   └── predictor.py               # Prediction engine
│
├── services/
│   ├── customer_service.py        # Customer management
│   ├── transaction_service.py     # Transaction processing
│   └── prediction_service.py      # Loan default predictions
│
├── utils/
│   ├── auth.py                    # Authentication utilities
│   └── helpers.py                 # Helper functions
│
└── data/
    └── microfinance_data.csv      # Training dataset
```

## Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher
- MongoDB Atlas account and connection string
- Git

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/riwamaictdesk-alt/IDS.git
cd IDS

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your MongoDB URI and settings
# MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

### 4. Prepare Dataset

Place your training dataset at `data/microfinance_data.csv` with the following columns:
- age
- income
- loan_amount
- loan_tenure
- previous_defaults
- transaction_frequency
- average_monthly_balance
- num_dependents
- employment_status
- loan_purpose
- default_status (target variable)

### 5. Train Models

```bash
python model_trainer_script.py --data data/microfinance_data.csv --output models/
```

This will:
- Train Logistic Regression, Decision Tree, and Random Forest models
- Evaluate each model using Accuracy, Precision, Recall, F1 Score, and ROC-AUC
- Save the best performing model as `best_model.pkl`
- Save individual models for comparison

### 6. Run Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Usage

### For Customers
1. Login with email and password
2. View account overview and transaction history
3. Use banking services (deposit, withdraw, transfer, phone recharge)
4. Request loan default risk assessment
5. Review prediction results and history

### For Loan Officers/Admin
1. Login with appropriate credentials
2. View customer predictions and risk assessments
3. Track loan application status
4. Generate reports on default risk trends

## Machine Learning Models

### Model Comparison

The system trains and compares three models:

#### 1. Logistic Regression
- Simple, interpretable binary classifier
- Fast training and prediction
- Baseline model for comparison

#### 2. Decision Tree
- Non-linear relationship capture
- Feature importance extraction
- Risk of overfitting managed with max_depth

#### 3. Random Forest
- Ensemble method combining multiple trees
- Reduced overfitting through averaging
- Feature importance from multiple estimators
- Generally best overall performance

### Evaluation Metrics

- **Accuracy**: Overall correct predictions ratio
- **Precision**: True positive rate among predicted positives
- **Recall**: True positive rate among actual positives
- **F1 Score**: Harmonic mean of precision and recall
- **ROC-AUC**: Area under the receiver operating characteristic curve

## Features Used for Prediction

1. **Age**: Customer age
2. **Income**: Monthly income
3. **Loan Amount**: Requested loan amount
4. **Loan Tenure**: Loan duration in months
5. **Previous Defaults**: Historical default count
6. **Transaction Frequency**: Number of recent transactions
7. **Average Monthly Balance**: Average account balance
8. **Number of Dependents**: Family size
9. **Employment Status**: Employment type (encoded)
10. **Loan Purpose**: Purpose of loan (encoded)

## Risk Levels

- **Low Risk (0-40%)**: High probability of loan repayment
- **Medium Risk (40-70%)**: Moderate risk, requires monitoring
- **High Risk (70-100%)**: High probability of default, needs intervention

## MongoDB Collections

### users
Store user authentication and profile data

### customers
Customer information and account details

### transactions
All financial transactions (deposits, withdrawals, transfers)

### loans
Loan applications and details

### predictions
Loan default predictions and assessment history

## API Endpoints (Future Enhancement)

The services can be wrapped with FastAPI for REST API:
- POST /api/customers - Create customer
- GET /api/customers/{id} - Get customer
- POST /api/transactions/deposit - Process deposit
- POST /api/transactions/withdraw - Process withdrawal
- POST /api/transactions/transfer - Transfer funds
- POST /api/predictions - Get risk assessment

## Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- MongoDB connection with URI authentication
- Environment variable protection
- Role-based access control (RBAC) ready

## Future Enhancements

1. **Advanced Analytics**
   - Customer segmentation
   - Cohort analysis
   - Trend forecasting

2. **Integration Features**
   - Email/SMS notifications
   - API integration with banks
   - Mobile app

3. **Model Improvements**
   - XGBoost, LightGBM models
   - SHAP values for model explainability
   - Automated model retraining

4. **Reporting**
   - PDF report generation
   - Custom dashboards
   - Export functionality

## Troubleshooting

### MongoDB Connection Issues
```bash
# Verify connection string
# Check network access in MongoDB Atlas
# Ensure IP is whitelisted
```

### Model Training Issues
```bash
# Check dataset format
# Verify all required columns exist
# Review data types and missing values
```

### Streamlit Issues
```bash
# Clear cache: streamlit cache clear
# Reinstall dependencies: pip install --upgrade -r requirements.txt
# Check port availability: lsof -i :8501
```

## Contributing

Contributions are welcome! Please:
1. Create a feature branch
2. Make your changes
3. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Open an issue on GitHub
- Contact: riwamaictdesk-alt@github.com

## Authors

riwamaictdesk-alt

## Acknowledgments

- Streamlit for the web framework
- scikit-learn for machine learning
- MongoDB for data storage
- Research on microfinance loan default prediction
