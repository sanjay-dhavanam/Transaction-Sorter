import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from utils.folder_manager import FolderManager
from utils.transaction_manager import TransactionManager
from utils.analytics import Analytics

# Initialize session state
if 'folder_manager' not in st.session_state:
    st.session_state.folder_manager = FolderManager()
if 'transaction_manager' not in st.session_state:
    st.session_state.transaction_manager = TransactionManager()
if 'analytics' not in st.session_state:
    st.session_state.analytics = Analytics()

def main():
    st.title("UPI Transaction Folder Manager")
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Navigation",
        ["Folders", "Scanner", "Transaction History", "Analytics"]
    )
    
    if page == "Folders":
        show_folders_page()
    elif page == "Scanner":
        show_scanner_page()
    elif page == "Transaction History":
        show_history_page()
    else:
        show_analytics_page()

def show_folders_page():
    st.header("Folder Management")
    
    # Create new folder
    with st.form("new_folder"):
        folder_name = st.text_input("New Folder Name")
        submit = st.form_submit_button("Create Folder")
        if submit and folder_name:
            st.session_state.folder_manager.create_folder(folder_name)
            st.success(f"Folder '{folder_name}' created successfully!")

    # List existing folders
    st.subheader("Your Folders")
    folders = st.session_state.folder_manager.get_folders()
    for folder in folders:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(folder)
        with col2:
            if st.button("Delete", key=f"del_{folder}"):
                st.session_state.folder_manager.delete_folder(folder)
                st.experimental_rerun()

def show_scanner_page():
    st.header("Payment Scanner")
    
    # Mock scanner interface
    with st.form("payment_form"):
        folders = st.session_state.folder_manager.get_folders()
        selected_folder = st.selectbox("Select Folder", folders)
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        merchant = st.text_input("Merchant Name")
        notes = st.text_input("Notes (optional)")
        
        if st.form_submit_button("Process Payment"):
            if selected_folder and amount > 0 and merchant:
                transaction = {
                    'folder': selected_folder,
                    'amount': amount,
                    'merchant': merchant,
                    'notes': notes,
                    'timestamp': datetime.now()
                }
                st.session_state.transaction_manager.add_transaction(transaction)
                st.success("Transaction recorded successfully!")
            else:
                st.error("Please fill in all required fields.")

def show_history_page():
    st.header("Transaction History")
    
    view_type = st.radio("View", ["All Transactions", "Folder-wise"])
    
    if view_type == "All Transactions":
        transactions = st.session_state.transaction_manager.get_all_transactions()
        if not transactions.empty:
            st.dataframe(transactions)
        else:
            st.info("No transactions recorded yet.")
    else:
        folders = st.session_state.folder_manager.get_folders()
        selected_folder = st.selectbox("Select Folder", folders)
        if selected_folder:
            transactions = st.session_state.transaction_manager.get_folder_transactions(selected_folder)
            if not transactions.empty:
                st.dataframe(transactions)
            else:
                st.info(f"No transactions in folder: {selected_folder}")

def show_analytics_page():
    st.header("Spending Analytics")
    
    # Date range selector
    date_range = st.date_input(
        "Select Date Range",
        value=(datetime.now().date(), datetime.now().date())
    )
    
    # Generate analytics
    analytics = st.session_state.analytics.generate_analytics(date_range)
    
    # Display visualizations
    if analytics['spending_by_folder'] is not None:
        st.subheader("Spending by Folder")
        fig = px.pie(analytics['spending_by_folder'], 
                    values='amount', 
                    names='folder',
                    title='Total Spending by Folder')
        st.plotly_chart(fig)
    
    if analytics['spending_trend'] is not None:
        st.subheader("Spending Trend")
        fig = px.line(analytics['spending_trend'],
                     x='date',
                     y='amount',
                     title='Daily Spending Trend')
        st.plotly_chart(fig)
    
    # Export functionality
    if st.button("Export for Power BI"):
        st.session_state.analytics.export_for_powerbi()
        st.success("Data exported successfully! Check the 'data' folder for the export file.")

if __name__ == "__main__":
    main()
