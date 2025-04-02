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
if 'selected_folder' not in st.session_state:
    st.session_state.selected_folder = 'Default'

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
            border: none;
            padding: 10px 20px;
            font-weight: bold;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }
        .folder-icon {
            font-size: 24px;
            color: #6739B7;
        }
        .phonepe-header {
            background-color: #6739B7;
            color: white;
            padding: 10px 0;
            text-align: center;
            border-radius: 10px 10px 0 0;
            font-weight: bold;
            font-size: 20px;
        }
        .scanner-overlay {
            position: relative;
            background-color: #000;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            height: 300px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .scanner-frame {
            border: 2px solid #6739B7;
            border-radius: 10px;
            padding: 5px;
            width: 80%;
            height: 60%;
            margin: 0 auto;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .folder-toggle {
            position: absolute;
            bottom: 20px;
            right: 20px;
            background-color: rgba(103, 57, 183, 0.8);
            color: white;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            font-size: 18px;
        }
        .folder-panel {
            background-color: #f8f8f8;
            border-radius: 10px;
            padding: 15px;
            margin-top: 10px;
            border: 1px solid #ddd;
        }
        .folder-item {
            display: flex;
            align-items: center;
            padding: 8px;
            border-radius: 5px;
            margin-bottom: 5px;
            cursor: pointer;
        }
        .folder-item:hover {
            background-color: #e9e0ff;
        }
        .folder-item-selected {
            background-color: #e9e0ff;
            border-left: 3px solid #6739B7;
        }
        div[data-testid="stSelectbox"] {
            background-color: white;
            border-radius: 5px;
            padding: 5px;
            border: 1px solid #ddd;
        }
        </style>
    """, unsafe_allow_html=True)

    show_scanner_interface()

def show_scanner_interface():
    # Top Bar
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("Scan & Pay")

    # Scanner View - PhonePe-like Scanner Interface
    scanner_container = st.container()
    with scanner_container:
        # PhonePe-like header
        st.markdown("""
            <div class="phonepe-header">
                Scan & Pay
            </div>
        """, unsafe_allow_html=True)
        
        # Camera viewfinder with QR frame
        st.markdown("""
            <div class="scanner-overlay">
                <div class="scanner-frame">
                    <p style='color: #6739B7;'>Position QR code in frame</p>
                </div>
                <p style='color: white; margin-top: 15px;'>Waiting for QR code...</p>
                <div class="folder-toggle">📁</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Folder Feature Toggle - Making it more visible
        col1, col2, col3 = st.columns([3,1,1])
        with col2:
            if st.button("📁 Folders", help="Enable/Disable Folder Feature"):
                st.session_state.show_folder_options = not st.session_state.show_folder_options
                
        # Show enabled/disabled status        
        with col3:
            status = "ON" if st.session_state.show_folder_options else "OFF"
            st.markdown(f"<p style='color: {'green' if st.session_state.show_folder_options else 'red'};'>{status}</p>", unsafe_allow_html=True)

    # Show folder options if enabled
    if st.session_state.show_folder_options:
        with st.container():
            st.markdown("""
                <div class="folder-panel">
                    <h3 style="color: #6739B7; margin-bottom: 15px;">📁 Select Folder</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Create new folder functionality
            col1, col2 = st.columns([1, 3])
            with col1:
                create_folder = st.button("➕ New Folder", use_container_width=True)
            
            # Initialize the input state
            if 'new_folder_name' not in st.session_state:
                st.session_state.new_folder_name = ""
            if 'show_folder_input' not in st.session_state:
                st.session_state.show_folder_input = False
                
            # Toggle the folder input form when button is clicked
            if create_folder:
                st.session_state.show_folder_input = True
            
            # Show the folder creation form when needed
            if st.session_state.show_folder_input:
                with st.container():
                    st.markdown("<div style='background-color: #e9e0ff; padding: 15px; border-radius: 10px; margin-top: 10px;'>", unsafe_allow_html=True)
                    
                    new_folder_name = st.text_input("Enter new folder name:", key="folder_name_input")
                    
                    col1, col2, col3 = st.columns([1,1,1])
                    with col1:
                        if st.button("Create Folder"):
                            if new_folder_name:
                                success = st.session_state.folder_manager.create_folder(new_folder_name)
                                if success:
                                    st.success(f"Folder '{new_folder_name}' created successfully!")
                                    # Update selected folder to the newly created one
                                    st.session_state.selected_folder = new_folder_name
                                    st.session_state.show_folder_input = False
                                else:
                                    st.warning(f"Folder '{new_folder_name}' already exists!")
                            else:
                                st.error("Please enter a folder name!")
                                
                    with col3:
                        if st.button("Cancel"):
                            st.session_state.show_folder_input = False
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            
            # Get existing folders
            folders = st.session_state.folder_manager.get_folders()
            if not folders:  # If no folders exist, add a Default folder
                st.session_state.folder_manager.create_folder('Default')
                folders = ['Default']
            
            # Custom folder selection with icons
            st.markdown("<p style='margin-top: 15px; font-weight: bold;'>Choose a folder:</p>", unsafe_allow_html=True)
            
            # Display folders in a grid
            cols = st.columns(3)
            for i, folder in enumerate(folders):
                with cols[i % 3]:
                    if st.button(f"📁 {folder}", key=f"folder_{i}", use_container_width=True):
                        st.session_state.selected_folder = folder
            
            # Show currently selected folder
            st.markdown(f"""
                <div style='margin-top: 15px; padding: 10px; background-color: #e9e0ff; border-radius: 5px;'>
                    <p style='margin: 0; color: #6739B7;'>Selected: 📁 {st.session_state.selected_folder}</p>
                </div>
            """, unsafe_allow_html=True)

    # Simulate payment process - PhonePe style payment interface
    with st.container():
        st.markdown("""
            <div style="background-color: white; padding: 15px; border-radius: 10px; margin-top: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h3 style="color: #6739B7; margin-bottom: 15px; text-align: center;">Payment Details</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Payment columns for a cleaner look
        col1, col2 = st.columns(2)
        
        with col1:
            merchant = st.text_input("👤 Merchant UPI ID", 
                                    placeholder="merchant@upi")
        
        with col2:
            amount = st.number_input("💰 Amount (₹)", 
                                    min_value=0.0, step=10.0,
                                    format="%.2f")
        
        # Optional note
        note = st.text_input("✏️ Add a note (optional)", 
                           placeholder="What's this payment for?")
        
        # Payment button styled like PhonePe
        st.markdown("<br>", unsafe_allow_html=True)
        
        pay_col1, pay_col2, pay_col3 = st.columns([1,2,1])
        with pay_col2:
            if st.button("💸 Pay Now", use_container_width=True):
                if amount > 0 and merchant:
                    # Create transaction
                    transaction = {
                        'merchant': merchant,
                        'amount': amount,
                        'timestamp': datetime.now(),
                        'folder': st.session_state.selected_folder if st.session_state.show_folder_options else 'Default',
                        'notes': note if note else ''
                    }
                    
                    # Save transaction
                    st.session_state.transaction_manager.add_transaction(transaction)
                    
                    # Success message with PhonePe style
                    st.markdown("""
                        <div style="background-color: #eefff5; padding: 20px; border-radius: 10px; margin-top: 20px; text-align: center; border-left: 4px solid #28a745;">
                            <h2 style="color: #28a745; margin-bottom: 10px;">🎉 Payment Successful!</h2>
                            <p style="font-size: 18px;">Your transaction has been completed.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                    
                    if st.session_state.show_folder_options:
                        st.markdown(f"""
                            <div style="background-color: #e9e0ff; padding: 10px; border-radius: 5px; margin-top: 10px; text-align: center;">
                                <p style="color: #6739B7; margin: 0;">
                                    <span style="font-size: 20px;">📁</span> 
                                    Transaction saved in folder: <strong>{st.session_state.selected_folder}</strong>
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error("Please enter a valid merchant ID and amount")

if __name__ == "__main__":
    main()