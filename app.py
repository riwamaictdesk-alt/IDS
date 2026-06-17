import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database.db_connection import MongoDBConnection
from services.customer_service import CustomerService
from services.transaction_service import TransactionService
from services.prediction_service import PredictionService
from utils.helpers import DataHelper
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Microfinance Loan Default Prediction",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .high-risk {
        background-color: #ff4444;
        color: white;
        padding: 10px 15px;
        border-radius: 5px;
    }
    .medium-risk {
        background-color: #ffa500;
        color: white;
        padding: 10px 15px;
        border-radius: 5px;
    }
    .low-risk {
        background-color: #4CAF50;
        color: white;
        padding: 10px 15px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

def login_page():
    """Login page"""
    st.title("🏦 Microfinance Loan Default Prediction System")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Login")
        
        login_type = st.radio("Login as:", ["Customer", "Admin", "Loan Officer"])
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", key="login_button", use_container_width=True):
            # Simple demo authentication
            if email and password:
                st.session_state.authenticated = True
                st.session_state.user_type = login_type.lower()
                st.session_state.user_id = email
                st.session_state.customer_id = "demo_customer_001"  # Demo customer ID
                st.rerun()
            else:
                st.error("Please enter email and password")

def customer_dashboard():
    """Customer Dashboard"""
    st.title("💳 Customer Dashboard")
    
    # Initialize services
    customer_service = CustomerService()
    transaction_service = TransactionService()
    prediction_service = PredictionService()
    
    customer_id = st.session_state.get('customer_id', 'demo_customer_001')
    
    # Sidebar navigation
    menu = st.sidebar.radio("Menu", [
        "Overview",
        "Account",
        "Transactions",
        "Loan Prediction",
        "Banking Services"
    ])
    
    if menu == "Overview":
        overview_page(customer_service, transaction_service, customer_id)
    elif menu == "Account":
        account_page(customer_service, customer_id)
    elif menu == "Transactions":
        transactions_page(transaction_service, customer_id)
    elif menu == "Loan Prediction":
        prediction_page(prediction_service, customer_id)
    elif menu == "Banking Services":
        banking_services_page(transaction_service, customer_id)

def overview_page(customer_service, transaction_service, customer_id):
    """Customer Overview Page"""
    st.markdown("### Account Overview")
    
    # Get customer data
    customer = customer_service.get_customer(customer_id)
    
    if customer:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Account Balance",
                value=DataHelper.format_currency(customer.get('account_balance', 0))
            )
        
        with col2:
            st.metric(
                label="Monthly Income",
                value=DataHelper.format_currency(customer.get('monthly_income', 0))
            )
        
        with col3:
            stats = transaction_service.get_transaction_stats(customer_id)
            st.metric(
                label="Total Transactions",
                value=stats.get('transaction_count', 0)
            )
        
        with col4:
            st.metric(
                label="Account Status",
                value="Active"
            )
        
        st.markdown("---")
        
        # Recent transactions
        st.markdown("### Recent Transactions")
        transactions = transaction_service.get_transaction_history(customer_id, limit=10)
        
        if transactions:
            df = pd.DataFrame(transactions)
            df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime("%Y-%m-%d %H:%M")
            df['amount'] = df['amount'].apply(DataHelper.format_currency)
            
            st.dataframe(
                df[['timestamp', 'transaction_type', 'amount', 'description', 'status']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No transactions yet")

def account_page(customer_service, customer_id):
    """Account Information Page"""
    st.markdown("### Account Information")
    
    customer = customer_service.get_customer(customer_id)
    
    if customer:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Personal Information**")
            st.write(f"**Name:** {customer.get('full_name', 'N/A')}")
            st.write(f"**Email:** {customer.get('email', 'N/A')}")
            st.write(f"**Phone:** {customer.get('phone', 'N/A')}")
            st.write(f"**Age:** {customer.get('age', 'N/A')}")
            st.write(f"**Gender:** {customer.get('gender', 'N/A')}")
        
        with col2:
            st.markdown("**Employment Information**")
            st.write(f"**Status:** {customer.get('employment_status', 'N/A')}")
            st.write(f"**Monthly Income:** {DataHelper.format_currency(customer.get('monthly_income', 0))}")
            st.write(f"**Address:** {customer.get('address', 'N/A')}")
            st.write(f"**Dependents:** {customer.get('num_dependents', 0)}")

def transactions_page(transaction_service, customer_id):
    """Transaction History Page"""
    st.markdown("### Transaction History")
    
    transactions = transaction_service.get_transaction_history(customer_id, limit=100)
    
    if transactions:
        df = pd.DataFrame(transactions)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            tx_type_filter = st.multiselect(
                "Transaction Type",
                options=df['transaction_type'].unique(),
                default=df['transaction_type'].unique()
            )
        with col2:
            date_range = st.date_input(
                "Date Range",
                value=(df['timestamp'].min().date(), df['timestamp'].max().date()),
                max_value=datetime.now().date()
            )
        
        # Filter data
        filtered_df = df[
            (df['transaction_type'].isin(tx_type_filter)) &
            (df['timestamp'].dt.date >= date_range[0]) &
            (df['timestamp'].dt.date <= date_range[1])
        ]
        
        # Display table
        display_df = filtered_df.copy()
        display_df['timestamp'] = display_df['timestamp'].dt.strftime("%Y-%m-%d %H:%M")
        display_df['amount'] = display_df['amount'].apply(DataHelper.format_currency)
        display_df['balance_after'] = display_df['balance_after'].apply(DataHelper.format_currency)
        
        st.dataframe(
            display_df[['timestamp', 'transaction_type', 'amount', 'description', 'balance_after', 'status']],
            use_container_width=True,
            hide_index=True
        )
        
        # Summary statistics
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            deposits = filtered_df[filtered_df['transaction_type'] == 'Deposit']['amount'].sum()
            st.metric("Total Deposits", DataHelper.format_currency(deposits))
        
        with col2:
            withdrawals = abs(filtered_df[filtered_df['transaction_type'] == 'Withdrawal']['amount'].sum())
            st.metric("Total Withdrawals", DataHelper.format_currency(withdrawals))
        
        with col3:
            transfers = filtered_df[filtered_df['transaction_type'] == 'Transfer']['amount'].sum()
            st.metric("Total Transfers", DataHelper.format_currency(transfers))
        
        with col4:
            recharges = filtered_df[filtered_df['transaction_type'] == 'Phone Recharge']['amount'].sum()
            st.metric("Total Recharges", DataHelper.format_currency(abs(recharges)))
    else:
        st.info("No transactions found")

def prediction_page(prediction_service, customer_id):
    """Loan Default Prediction Page"""
    st.markdown("### Loan Default Risk Assessment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Analyze Loan Default Risk", use_container_width=True):
            with st.spinner("Analyzing..."):
                result = prediction_service.predict_default_risk(customer_id)
                
                if result['success']:
                    st.success("Analysis Complete!")
                    
                    # Display results
                    prediction_score = result['prediction_score']
                    risk_level = result['risk_level']
                    confidence = result['confidence']
                    
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        st.metric(
                            label="Risk Score",
                            value=f"{prediction_score:.2%}"
                        )
                    
                    with col_b:
                        st.metric(
                            label="Risk Level",
                            value=risk_level
                        )
                    
                    with col_c:
                        st.metric(
                            label="Confidence",
                            value=f"{confidence:.2%}"
                        )
                    
                    # Risk gauge
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=prediction_score * 100,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "Default Risk Score"},
                        gauge={'axis': {'range': [0, 100]},
                               'bar': {'color': "darkblue"},
                               'steps': [
                                   {'range': [0, 40], 'color': "lightgreen"},
                                   {'range': [40, 70], 'color': "lightyellow"},
                                   {'range': [70, 100], 'color': "lightcoral"}],
                               'threshold': {'line': {'color': "red", 'width': 4},
                                           'thickness': 0.75,
                                           'value': 90}}
                    ))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error(f"Error: {result.get('message', 'Unknown error')}")
    
    with col2:
        st.markdown("**Risk Assessment Guide**")
        st.markdown("""
        - **Low Risk (0-40%)**: High probability of loan repayment
        - **Medium Risk (40-70%)**: Moderate risk, requires monitoring
        - **High Risk (70-100%)**: High probability of default, needs intervention
        """)
    
    # Prediction history
    st.markdown("---")
    st.markdown("### Prediction History")
    history = prediction_service.get_prediction_history(customer_id)
    
    if history:
        df = pd.DataFrame(history)
        df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime("%Y-%m-%d %H:%M")
        df['prediction_score'] = df['prediction_score'].apply(lambda x: f"{x:.2%}")
        df['confidence'] = df['confidence'].apply(lambda x: f"{x:.2%}")
        
        st.dataframe(
            df[['created_at', 'prediction_score', 'prediction_label', 'confidence', 'model_used']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No prediction history yet")

def banking_services_page(transaction_service, customer_id):
    """Banking Services Page"""
    st.markdown("### Banking Services")
    
    service = st.selectbox(
        "Select Service",
        ["Deposit", "Withdrawal", "Transfer", "Phone Recharge"]
    )
    
    st.markdown("---")
    
    if service == "Deposit":
        st.markdown("### Deposit Funds")
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        description = st.text_input("Description (optional)")
        
        if st.button("Deposit", use_container_width=True):
            if amount > 0:
                result = transaction_service.deposit(customer_id, amount, description or "Deposit")
                if result['success']:
                    st.success(f"✅ Deposit successful!")
                    st.info(f"New Balance: {DataHelper.format_currency(result['new_balance'])}")
                else:
                    st.error(f"❌ {result['message']}")
            else:
                st.error("Please enter a valid amount")
    
    elif service == "Withdrawal":
        st.markdown("### Withdraw Funds")
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        description = st.text_input("Description (optional)")
        
        if st.button("Withdraw", use_container_width=True):
            if amount > 0:
                result = transaction_service.withdraw(customer_id, amount, description or "Withdrawal")
                if result['success']:
                    st.success(f"✅ Withdrawal successful!")
                    st.info(f"New Balance: {DataHelper.format_currency(result['new_balance'])}")
                else:
                    st.error(f"❌ {result['message']}")
            else:
                st.error("Please enter a valid amount")
    
    elif service == "Transfer":
        st.markdown("### Transfer Funds")
        recipient_id = st.text_input("Recipient Customer ID")
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        description = st.text_input("Description (optional)")
        
        if st.button("Transfer", use_container_width=True):
            if amount > 0 and recipient_id:
                result = transaction_service.transfer(
                    customer_id, recipient_id, amount, description or "Transfer"
                )
                if result['success']:
                    st.success(f"✅ Transfer successful!")
                    st.info(f"Your New Balance: {DataHelper.format_currency(result['from_balance'])}")
                else:
                    st.error(f"❌ {result['message']}")
            else:
                st.error("Please enter valid recipient ID and amount")
    
    elif service == "Phone Recharge":
        st.markdown("### Phone Recharge")
        phone_number = st.text_input("Phone Number")
        amount = st.number_input("Recharge Amount", min_value=0.0, format="%.2f")
        
        if st.button("Recharge", use_container_width=True):
            if amount > 0 and phone_number:
                result = transaction_service.phone_recharge(customer_id, amount, phone_number)
                if result['success']:
                    st.success(f"✅ Phone recharge successful!")
                    st.info(f"Phone: {phone_number} | Amount: {DataHelper.format_currency(amount)}")
                    st.info(f"New Balance: {DataHelper.format_currency(result['new_balance'])}")
                else:
                    st.error(f"❌ {result['message']}")
            else:
                st.error("Please enter valid phone number and amount")

def main():
    """Main application"""
    if not st.session_state.authenticated:
        login_page()
    else:
        # Logout button in sidebar
        st.sidebar.markdown("---")
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
        
        st.sidebar.info(f"Logged in as: {st.session_state.user_id}")
        
        if st.session_state.user_type == "customer":
            customer_dashboard()
        elif st.session_state.user_type == "admin":
            st.title("🛠️ Admin Dashboard")
            st.info("Admin features coming soon")
        elif st.session_state.user_type == "loan officer":
            st.title("📋 Loan Officer Dashboard")
            st.info("Loan officer features coming soon")

if __name__ == "__main__":
    main()
