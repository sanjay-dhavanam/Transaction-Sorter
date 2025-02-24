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
if 'scan_state' not in st.session_state:
    st.session_state.scan_state = 'initial'  # States: initial, folder_selection, processing
if 'current_transaction' not in st.session_state:
    st.session_state.current_transaction = {}

def main():
    st.title("PhonePe Scanner Simulation")

    # Simplified navigation - focusing on scanner experience
    show_scanner_page()

def show_scanner_page():
    if st.session_state.scan_state == 'initial':
        show_initial_scan()
    elif st.session_state.scan_state == 'folder_selection':
        show_folder_selection()
    elif st.session_state.scan_state == 'processing':
        process_transaction()

def show_initial_scan():
    st.header("UPI Scanner")

    # Simulate QR code scanning
    col1, col2 = st.columns([3, 1])
    with col1:
        merchant = st.text_input("Merchant UPI ID")
        amount = st.number_input("Amount", min_value=0.0, step=0.01)

    # Proceed button
    if st.button("Scan QR Code"):
        if merchant and amount > 0:
            st.session_state.current_transaction = {
                'merchant': merchant,
                'amount': amount,
                'timestamp': datetime.now()
            }
            st.session_state.scan_state = 'folder_selection'
            st.experimental_rerun()
        else:
            st.error("Please enter merchant details and amount")

def show_folder_selection():
    st.header("Select Folder")

    # Display transaction details
    st.info(f"Payment to: {st.session_state.current_transaction['merchant']}")
    st.info(f"Amount: ₹{st.session_state.current_transaction['amount']:.2f}")

    # Create new folder option
    with st.expander("➕ Create New Folder"):
        with st.form("new_folder"):
            new_folder = st.text_input("Folder Name")
            if st.form_submit_button("Create"):
                if new_folder:
                    st.session_state.folder_manager.create_folder(new_folder)
                    st.success(f"Created folder: {new_folder}")
                    st.experimental_rerun()

    # Select folder
    folders = st.session_state.folder_manager.get_folders()
    selected_folder = st.selectbox("Select Folder", folders, help="Choose a folder to categorize this transaction")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back"):
            st.session_state.scan_state = 'initial'
            st.experimental_rerun()
    with col2:
        if st.button("Pay") and selected_folder:
            st.session_state.current_transaction['folder'] = selected_folder
            st.session_state.scan_state = 'processing'
            st.experimental_rerun()

def process_transaction():
    st.header("Processing Payment")

    # Add notes if needed
    notes = st.text_input("Add notes (optional)")
    st.session_state.current_transaction['notes'] = notes

    # Process the payment
    if st.button("Confirm Payment"):
        # Save transaction
        st.session_state.transaction_manager.add_transaction(st.session_state.current_transaction)

        # Show success message
        st.success("Payment Successful!")
        st.balloons()

        # Show folder details
        st.info(f"Transaction recorded in folder: {st.session_state.current_transaction['folder']}")

        # Option to view transaction history
        if st.button("View Transactions"):
            show_history_page()
        else:
            # Reset for next transaction
            st.session_state.scan_state = 'initial'
            st.session_state.current_transaction = {}
            st.experimental_rerun()

def show_history_page():
    st.header("Transaction History")

    # Filter by folder
    folders = st.session_state.folder_manager.get_folders()
    selected_folder = st.selectbox("Select Folder to View", folders)

    if selected_folder:
        transactions = st.session_state.transaction_manager.get_folder_transactions(selected_folder)
        if not transactions.empty:
            st.dataframe(transactions)
        else:
            st.info(f"No transactions in folder: {selected_folder}")

if __name__ == "__main__":
    main()