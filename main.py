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
if 'show_folder_options' not in st.session_state:
    st.session_state.show_folder_options = False

def main():
    # Set page config to match PhonePe style
    st.set_page_config(page_title="PhonePe Scanner", layout="wide")

    # Custom CSS to match PhonePe style
    st.markdown("""
        <style>
        .stButton button {
            background-color: #6739B7;
            color: white;
            border-radius: 20px;
        }
        .folder-icon {
            font-size: 24px;
            color: #6739B7;
        }
        </style>
    """, unsafe_allow_html=True)

    show_scanner_interface()

def show_scanner_interface():
    # Top Bar
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("Scan & Pay")

    # Scanner View
    scanner_container = st.container()
    with scanner_container:
        st.markdown("""
            <div style='background-color: #000; padding: 20px; border-radius: 10px; text-align: center;'>
                <p style='color: white;'>Camera Viewfinder</p>
                <p style='color: #6739B7;'>Position QR code in frame</p>
            </div>
        """, unsafe_allow_html=True)

        # Folder Feature Toggle (similar to PhonePe's flash toggle)
        col1, col2 = st.columns([4,1])
        with col2:
            if st.button("📁", help="Enable/Disable Folder Feature"):
                st.session_state.show_folder_options = not st.session_state.show_folder_options

    # Show folder options if enabled
    if st.session_state.show_folder_options:
        with st.container():
            st.markdown("### 📁 Select Folder")

            # Create new folder option
            if st.button("➕ Create New Folder"):
                folder_name = st.text_input("Enter folder name")
                if folder_name:
                    st.session_state.folder_manager.create_folder(folder_name)
                    st.success(f"Created folder: {folder_name}")

            # Select existing folder
            folders = st.session_state.folder_manager.get_folders()
            selected_folder = st.selectbox(
                "Choose folder for this payment",
                folders,
                help="Transaction will be saved in this folder"
            )

    # Simulate payment process
    with st.container():
        # Mock payment fields (normally these would come from QR scan)
        merchant = st.text_input("Merchant UPI ID (Simulated QR data)")
        amount = st.number_input("Amount", min_value=0.0, step=0.01)

        if st.button("Pay Now", use_container_width=True):
            if amount > 0 and merchant:
                # Create transaction
                transaction = {
                    'merchant': merchant,
                    'amount': amount,
                    'timestamp': datetime.now(),
                    'folder': selected_folder if st.session_state.show_folder_options else 'Default',
                    'notes': ''
                }

                # Save transaction
                st.session_state.transaction_manager.add_transaction(transaction)

                # Success message
                st.success("🎉 Payment Successful!")
                st.balloons()

                if st.session_state.show_folder_options:
                    st.info(f"Transaction saved in folder: {selected_folder}")
            else:
                st.error("Please enter valid payment details")

if __name__ == "__main__":
    main()