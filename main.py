import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
from utils.folder_manager import FolderManager
from utils.transaction_manager import TransactionManager
from utils.analytics import Analytics
from utils.notification_manager import NotificationManager

# Initialize session state
if 'folder_manager' not in st.session_state:
    st.session_state.folder_manager = FolderManager()
if 'transaction_manager' not in st.session_state:
    st.session_state.transaction_manager = TransactionManager()
if 'analytics' not in st.session_state:
    st.session_state.analytics = Analytics()
if 'notification_manager' not in st.session_state:
    st.session_state.notification_manager = NotificationManager()
if 'show_folder_options' not in st.session_state:
    st.session_state.show_folder_options = False
if 'selected_folder' not in st.session_state:
    st.session_state.selected_folder = 'Default'
if 'qr_scanned' not in st.session_state:
    st.session_state.qr_scanned = False
if 'merchant_data' not in st.session_state:
    st.session_state.merchant_data = {
        'upi_id': '',
        'name': '',
        'amount': 0.0
    }
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'scanner'
    
# Function to simulate QR scan
def simulate_qr_scan():
    """Simulate scanning a QR code and extracting data"""
    # In a real app, this would parse QR code data
    import random
    merchants = [
        {"upi_id": "amazon@upi", "name": "Amazon Shopping", "amount": random.randint(500, 2000)},
        {"upi_id": "flipkart@upi", "name": "Flipkart", "amount": random.randint(200, 1500)},
        {"upi_id": "grocerystore@upi", "name": "Local Grocery Store", "amount": random.randint(100, 800)},
        {"upi_id": "restaurant@upi", "name": "Food Junction", "amount": random.randint(300, 1200)},
        {"upi_id": "utility@upi", "name": "Electric Bill Payment", "amount": random.randint(500, 3000)}
    ]
    selected = random.choice(merchants)
    return selected

def main():
    # Set page config to match PhonePe style
    st.set_page_config(page_title="PhonePe", page_icon="📱", layout="centered")

    # Custom CSS to match PhonePe mobile app style
    st.markdown("""
        <style>
        /* Base Styling */
        body {
            font-family: 'Roboto', sans-serif;
            max-width: 100%;
            overflow-x: hidden;
        }
        
        /* Button Styling */
        .stButton button {
            background-color: #6739B7;
            color: white;
            border-radius: 20px;
            border: none;
            padding: 10px 20px;
            font-weight: bold;
            box-shadow: 0 2px 5px rgba(103,57,183,0.3);
            transition: all 0.2s ease;
        }
        
        .stButton button:hover {
            background-color: #5c33a4;
            box-shadow: 0 4px 8px rgba(103,57,183,0.4);
        }
        
        /* Mobile Container */
        .mobile-container {
            max-width: 480px;
            margin: 0 auto;
            border: 1px solid #ddd;
            border-radius: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            overflow: hidden;
            background-color: #f9f9f9;
            position: relative;
        }
        
        /* Headers */
        .phonepe-header {
            background-color: #6739B7;
            color: white;
            padding: 15px 0;
            text-align: center;
            border-radius: 10px 10px 0 0;
            font-weight: bold;
            font-size: 18px;
            margin-bottom: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        /* Scanner UI */
        .scanner-overlay {
            position: relative;
            background-color: rgba(0, 0, 0, 0.9);
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            height: 300px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            margin-bottom: 20px;
        }
        
        /* Mobile Status Bar */
        .status-bar {
            background-color: #6739B7;
            color: white;
            padding: 5px 15px;
            font-size: 12px;
            display: flex;
            justify-content: space-between;
        }
        
        /* Icon Styling */
        .folder-icon {
            font-size: 24px;
            color: #6739B7;
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

    # Mobile Phone Status Bar (simulated)
    st.markdown("""
        <div class="status-bar">
            <span>📶 5G</span>
            <span>⚡ 85%</span>
            <span>⌚ 10:45 AM</span>
        </div>
    """, unsafe_allow_html=True)
    
    # PhonePe App Header
    st.markdown("""
        <div style="text-align: center; padding: 10px 0;">
            <h1 style="color: #6739B7; margin: 0; font-size: 28px;">Phone<span style="color: #3483FA;">Pe</span></h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Get unread notifications count
    unread_count = st.session_state.notification_manager.get_unread_count()
    
    # Navigation options
    if unread_count > 0:
        nav_options = ["Scan & Pay", "Transaction History", f"Notifications 🔔 ({unread_count})", "Spending Analytics 📊"]
    else:
        nav_options = ["Scan & Pay", "Transaction History", "Notifications 🔔", "Spending Analytics 📊"]
    
    # Mobile App Style Navigation with icons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        scan_btn = st.button("📷\nScan & Pay", key="nav_scan", use_container_width=True)
        if scan_btn:
            st.session_state.current_view = "scanner"
            st.rerun()
            
    with col2:
        history_btn = st.button("📋\nHistory", key="nav_history", use_container_width=True)
        if history_btn:
            st.session_state.current_view = "history"
            st.rerun()
            
    with col3:
        notif_label = f"🔔\n({unread_count})" if unread_count > 0 else "🔔\nNotify"
        notif_btn = st.button(notif_label, key="nav_notif", use_container_width=True)
        if notif_btn:
            st.session_state.current_view = "notifications"
            st.rerun()
            
    with col4:
        analytics_btn = st.button("📊\nAnalytics", key="nav_analytics", use_container_width=True)
        if analytics_btn:
            st.session_state.current_view = "analytics"
            st.rerun()
    
    # Divider
    st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
    
    # Keep a hidden navigation for accessibility
    selected_option = st.sidebar.radio("Navigation", nav_options, label_visibility="collapsed")
    
    # Update current view based on selection
    if selected_option == "Scan & Pay":
        st.session_state.current_view = "scanner"
    elif "Notifications" in selected_option:
        st.session_state.current_view = "notifications"
    elif "Spending Analytics" in selected_option:
        st.session_state.current_view = "analytics"
    else:
        st.session_state.current_view = "history"
    
    # Show selected interface
    if st.session_state.current_view == "scanner":
        show_scanner_interface()
    elif st.session_state.current_view == "notifications":
        show_notifications()
    elif st.session_state.current_view == "analytics":
        show_spending_analytics()
    else:
        show_transaction_history()

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
        if not st.session_state.qr_scanned:
            st.markdown("""
                <div class="scanner-overlay">
                    <div class="scanner-frame">
                        <p style='color: #6739B7;'>Position QR code in frame</p>
                    </div>
                    <p style='color: white; margin-top: 15px;'>Waiting for QR code...</p>
                    <div class="folder-toggle">📁</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Add a scan button to simulate QR scanning
            scan_col1, scan_col2, scan_col3 = st.columns([1,1,1])
            with scan_col2:
                if st.button("📷 Scan QR Code", use_container_width=True):
                    # Simulate scanning and get merchant data
                    merchant_data = simulate_qr_scan()
                    st.session_state.merchant_data = merchant_data
                    st.session_state.qr_scanned = True
                    st.rerun()
        else:
            # Show detected QR result
            st.markdown(f"""
                <div style="background-color: #e9e0ff; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
                    <h3 style="color: #6739B7; margin-bottom: 10px;">✅ QR Code Detected!</h3>
                    <p style="font-size: 18px; color: #333;">
                        <strong>Merchant:</strong> {st.session_state.merchant_data['name']}<br>
                        <strong>UPI ID:</strong> {st.session_state.merchant_data['upi_id']}<br>
                        <strong>Amount:</strong> ₹{st.session_state.merchant_data['amount']:.2f}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Add a Reset button to scan another QR
            reset_col1, reset_col2, reset_col3 = st.columns([1,1,1])
            with reset_col2:
                if st.button("🔄 Scan Another QR", use_container_width=True):
                    st.session_state.qr_scanned = False
                    st.rerun()
        
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
        
        # Auto-populate from QR code if scanned
        with col1:
            if st.session_state.qr_scanned:
                merchant_name = st.session_state.merchant_data['name']
                merchant_upi = st.session_state.merchant_data['upi_id']
                merchant = st.text_input("👤 Merchant", 
                                       value=merchant_upi,
                                       help=f"Merchant Name: {merchant_name}")
            else:
                merchant = st.text_input("👤 Merchant UPI ID", 
                                       placeholder="Scan QR code or enter manually")
        
        with col2:
            if st.session_state.qr_scanned:
                default_amount = st.session_state.merchant_data['amount']
                amount = st.number_input("💰 Amount (₹)", 
                                       value=float(default_amount),
                                       min_value=0.0, 
                                       step=10.0,
                                       format="%.2f")
            else:
                amount = st.number_input("💰 Amount (₹)", 
                                       min_value=0.0, 
                                       step=10.0,
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
                    
                    # Check if this transaction exceeds any spending limit
                    folder_name = transaction['folder']
                    if st.session_state.show_folder_options:
                        # Check folder spending limit
                        limit_info = st.session_state.analytics.check_folder_limit(
                            folder_name, 
                            st.session_state.folder_manager
                        )
                        
                        # If limit is set and exceeded, create a notification
                        if limit_info['has_limit'] and limit_info['over_limit']:
                            # Trigger notification
                            st.session_state.notification_manager.add_limit_exceeded_notification(
                                folder_name,
                                limit_info['current'],
                                limit_info['limit']
                            )
                            
                            # Show warning in UI
                            st.warning(f"""
                            ⚠️ SPENDING LIMIT EXCEEDED for folder '{folder_name}'!
                            You have spent ₹{limit_info['current']:.2f}, which is {limit_info['percentage']:.1f}% of your ₹{limit_info['limit']:.2f} limit.
                            A notification has been sent to your phone.
                            """)
                    
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

def show_transaction_history():
    """Display transaction history with folder filtering"""
    # Page title
    st.title("Transaction History")
    
    # PhonePe-like header
    st.markdown("""
        <div class="phonepe-header">
            📁 Folder Transactions
        </div>
    """, unsafe_allow_html=True)
    
    # Get all folders for filter
    folders = st.session_state.folder_manager.get_folders()
    if not folders:
        folders = ['Default']
        
    # Add "All Folders" option at the beginning
    filter_options = ["All Folders"] + folders
    
    tab1, tab2 = st.tabs(["📊 Transactions", "⚙️ Spending Limits"])
    
    with tab1:
        # Create filter dropdown
        selected_folder = st.selectbox(
            "Select a folder to view transactions:", 
            filter_options,
            index=0,  # Default to "All Folders"
        )
        
        # Show spending limit info if a specific folder is selected
        if selected_folder != "All Folders":
            limit_info = st.session_state.analytics.check_folder_limit(
                selected_folder, 
                st.session_state.folder_manager
            )
            
            # Display current spending and limit
            if limit_info['has_limit']:
                # Calculate progress color based on percentage
                progress_color = "#28a745"  # Green
                if limit_info['percentage'] > 80:
                    progress_color = "#ffc107"  # Yellow
                if limit_info['percentage'] > 100:
                    progress_color = "#dc3545"  # Red
                
                # Show progress bar and limit details
                st.markdown(f"""
                    <div style="background-color: #f8f8f8; padding: 15px; border-radius: 10px; margin: 15px 0;">
                        <h4 style="margin-top: 0; color: #6739B7;">Spending Limit: ₹{limit_info['limit']:.2f}</h4>
                        <p>Current spending: ₹{limit_info['current']:.2f} ({limit_info['period']})</p>
                        <div style="background-color: #e9e9e9; height: 20px; border-radius: 10px; margin: 10px 0;">
                            <div style="background-color: {progress_color}; width: {min(100, limit_info['percentage'])}%; height: 20px; border-radius: 10px;">
                                <p style="text-align: center; color: white; padding-top: 1px; font-size: 14px;">{limit_info['percentage']:.1f}%</p>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Show warning if over limit
                if limit_info['over_limit']:
                    st.warning(f"⚠️ You have exceeded your spending limit for {selected_folder}! Consider reducing your expenses in this category.")
            else:
                # Show current spending without limit
                spending = st.session_state.analytics.get_current_month_spending(selected_folder)
                st.markdown(f"""
                    <div style="background-color: #f8f8f8; padding: 15px; border-radius: 10px; margin: 15px 0;">
                        <p style="margin: 0;">Current spending: ₹{spending['amount']:.2f} ({spending['period']})</p>
                        <p style="margin: 5px 0 0; color: #6c757d;">No spending limit set. Set a limit in the Spending Limits tab.</p>
                    </div>
                """, unsafe_allow_html=True)
        
        # Get transactions for the selected folder
        transactions = st.session_state.analytics.get_folder_transactions(selected_folder)
        
        # Display transactions
        if not transactions.empty:
            # Format the timestamp for better display
            transactions['formatted_date'] = transactions['timestamp'].dt.strftime('%d %b %Y, %I:%M %p')
            
            # Total amount for the selected folder
            total_amount = transactions['amount'].sum()
            
            # Display the total
            st.markdown(f"""
                <div style="background-color: #e9e0ff; padding: 15px; border-radius: 10px; margin: 20px 0; text-align: center;">
                    <h3 style="color: #6739B7; margin: 0;">Total: ₹{total_amount:.2f}</h3>
                    <p style="margin: 5px 0 0 0;">From {len(transactions)} transactions</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Create a container for transactions
            st.markdown("""
                <div style="background-color: white; padding: 15px; border-radius: 10px; margin-top: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                    <h3 style="color: #6739B7; margin-bottom: 15px; text-align: center;">Transaction Details</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Display individual transactions
            for i, tx in transactions.iterrows():
                # Calculate a color based on amount (higher = darker)
                amount_color = "#6739B7" if tx['amount'] > 1000 else "#8A64C7"
                
                with st.container():
                    st.markdown(f"""
                        <div style="border-left: 4px solid {amount_color}; padding: 15px; margin: 10px 0; background-color: #f9f9f9; border-radius: 5px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <h4 style="margin: 0; color: #333;">{tx['merchant']}</h4>
                                <h3 style="margin: 0; color: {amount_color};">₹{tx['amount']:.2f}</h3>
                            </div>
                            <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                                <p style="margin: 0; color: #666; font-size: 14px;">{tx['formatted_date']}</p>
                                <p style="margin: 0; color: #6739B7; font-weight: bold; font-size: 14px;">📁 {tx['folder']}</p>
                            </div>
                            <p style="margin: 5px 0 0; color: #777; font-style: italic;">{tx['notes'] if tx['notes'] else 'No notes'}</p>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            # No transactions found
            st.markdown("""
                <div style="background-color: #f8f8f8; padding: 30px; border-radius: 10px; text-align: center; margin-top: 20px;">
                    <h3 style="color: #6739B7; margin-bottom: 10px;">No Transactions Found</h3>
                    <p>There are no transactions in this folder yet.</p>
                    <p>Create a transaction by using the Scan & Pay feature.</p>
                </div>
            """, unsafe_allow_html=True)
    
    # Spending Limits Tab
    with tab2:
        st.markdown("""
            <div style="background-color: white; padding: 15px; border-radius: 10px; margin-top: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h3 style="color: #6739B7; margin-bottom: 15px; text-align: center;">Folder Spending Limits</h3>
                <p style="text-align: center; color: #555;">Set monthly spending limits for each folder to manage your expenses</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Display folder details and allow setting limits
        folder_details = st.session_state.folder_manager.get_folder_details()
        
        # Current month info
        today = date.today()
        current_month = today.strftime('%B %Y')
        
        st.markdown(f"""
            <div style="background-color: #e9e0ff; padding: 10px; border-radius: 5px; margin: 15px 0; text-align: center;">
                <p style="margin: 0; color: #6739B7; font-weight: bold;">Current Period: {current_month}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # For each folder, show current limit and spending + input to update
        for index, folder in folder_details.iterrows():
            folder_name = folder['folder_name']
            
            # Get current limit and spending
            limit = folder['spending_limit'] if 'spending_limit' in folder else 0.0
            spending_info = st.session_state.analytics.check_folder_limit(folder_name, st.session_state.folder_manager)
            
            with st.container():
                st.markdown(f"""
                    <div style="padding: 10px; margin: 15px 0 5px 0; background-color: #f8f8f8; border-radius: 5px;">
                        <h4 style="margin: 0; color: #6739B7;">📁 {folder_name}</h4>
                    </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([3, 2])
                
                # Current spending for this folder
                current_spending = spending_info['current'] if spending_info['has_limit'] else st.session_state.analytics.get_current_month_spending(folder_name)['amount']
                
                with col1:
                    st.markdown(f"Current spending: ₹{current_spending:.2f}")
                    if spending_info['has_limit']:
                        progress_color = "#28a745"  # Green
                        if spending_info['percentage'] > 80:
                            progress_color = "#ffc107"  # Yellow
                        if spending_info['percentage'] > 100:
                            progress_color = "#dc3545"  # Red
                            
                        st.progress(min(1.0, spending_info['percentage']/100))
                        st.markdown(f"<p style='color: {progress_color}; font-size: 14px;'>{spending_info['percentage']:.1f}% of limit</p>", unsafe_allow_html=True)
                
                with col2:
                    # Set new limit
                    new_limit = st.number_input(
                        f"Set limit for {folder_name}:",
                        min_value=0.0,
                        value=float(limit),
                        step=100.0,
                        format="%.2f",
                        key=f"limit_{folder_name}"
                    )
                    
                    if st.button(f"Update Limit", key=f"update_{folder_name}"):
                        success = st.session_state.folder_manager.set_spending_limit(folder_name, new_limit)
                        if success:
                            st.success(f"Spending limit updated for {folder_name}!")
                            if new_limit > 0:
                                st.info(f"You will be notified when spending exceeds ₹{new_limit:.2f}")
                            else:
                                st.info("No spending limit set (0 = unlimited)")
                        else:
                            st.error("Failed to update spending limit!")

def show_spending_analytics():
    """Display spending analytics with pie charts and graphs showing category-wise spending"""
    # Page title
    st.title("Spending Analytics")
    
    # PhonePe-like header
    st.markdown("""
        <div class="phonepe-header">
            📊 Spending Insights
        </div>
    """, unsafe_allow_html=True)
    
    # Get all folders for filter
    folders = st.session_state.folder_manager.get_folders()
    if not folders:
        folders = ['Default']
        
    # Add "All Folders" option at the beginning
    filter_options = ["All Folders"] + folders
    
    # Date range filter
    st.markdown("""
        <div style="background-color: white; padding: 15px; border-radius: 10px; margin: 20px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h3 style="color: #6739B7; margin-bottom: 10px;">Customize Your View</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Create filter section
    col1, col2 = st.columns(2)
    
    with col1:
        # Multi-select folders
        selected_folders = st.multiselect(
            "Select folders to analyze:", 
            folders,
            default=folders[0] if folders else None,
            placeholder="Choose folders..."
        )
    
    with col2:
        # Time period filter (simplified)
        time_period = st.selectbox(
            "Select time period:", 
            ["All Time", "Current Month", "Last Month", "Last 3 Months"],
            index=0,
        )
    
    # Error message if no folders are selected
    if not selected_folders:
        st.warning("Please select at least one folder to view analytics.")
        return
    
    # Get analytics data
    analytics_data = st.session_state.analytics.generate_analytics()
    
    # Extract spending data by folder
    spending_by_folder = analytics_data['spending_by_folder']
    
    # Filter by selected folders if not "All Folders"
    if selected_folders:
        spending_by_folder = spending_by_folder[spending_by_folder['folder'].isin(selected_folders)]
        
    if spending_by_folder.empty:
        st.info("No transaction data available for the selected folders.")
        return
    
    # Display total spending info
    total_spending = spending_by_folder['amount'].sum()
    
    st.markdown(f"""
        <div style="background-color: #f0f0f0; padding: 20px; border-radius: 10px; margin: 20px 0; text-align: center;">
            <h2 style="color: #6739B7; margin-bottom: 10px;">Total Spending: ₹{total_spending:.2f}</h2>
            <p>Across {len(selected_folders)} folders</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["📈 Pie Chart", "📊 Bar Chart", "🔍 Detailed Breakdown"])
    
    with tab1:
        st.markdown("<h3 style='text-align: center; color: #6739B7;'>Spending Distribution by Folder</h3>", unsafe_allow_html=True)
        
        # Create a pie chart showing distribution of spending across folders
        spending_pie = px.pie(
            spending_by_folder, 
            values='amount', 
            names='folder',
            title='Spending Distribution by Folder',
            hover_data=['percentage'],
            labels={'amount': 'Amount (₹)', 'folder': 'Folder', 'percentage': 'Percentage (%)'},
            color_discrete_sequence=px.colors.qualitative.Bold,
        )
        
        # Customize the pie chart
        spending_pie.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Amount: ₹%{value:.2f}<br>Percentage: %{customdata[0]:.1f}%'
        )
        
        # Set the theme and layout
        spending_pie.update_layout(
            legend_title_text='Folders',
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
            margin=dict(t=60, b=120, l=40, r=40),
            height=500,
        )
        
        # Display the pie chart
        st.plotly_chart(spending_pie, use_container_width=True)
        
        # Display legend with exact amounts and percentages
        st.markdown("<h4 style='text-align: center; color: #333;'>Detailed Distribution</h4>", unsafe_allow_html=True)
        
        # Create a formatted table to show exact figures
        for _, row in spending_by_folder.iterrows():
            folder = row['folder']
            amount = row['amount']
            percentage = row['percentage']
            
            st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #eee;">
                    <div style="font-weight: bold;">📁 {folder}</div>
                    <div>₹{amount:.2f} ({percentage:.1f}%)</div>
                </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<h3 style='text-align: center; color: #6739B7;'>Spending by Folder (Bar Chart)</h3>", unsafe_allow_html=True)
        
        # Create a bar chart
        spending_bar = px.bar(
            spending_by_folder.sort_values('amount', ascending=False), 
            x='folder', 
            y='amount',
            title='Spending by Folder',
            labels={'amount': 'Amount (₹)', 'folder': 'Folder'},
            color='amount',
            color_continuous_scale='Viridis',
            text='amount'
        )
        
        # Customize the bar chart
        spending_bar.update_traces(
            texttemplate='₹%{text:.2f}',
            textposition='outside'
        )
        
        # Set the theme and layout
        spending_bar.update_layout(
            xaxis_title='Folder',
            yaxis_title='Amount (₹)',
            height=500,
            margin=dict(t=60, b=120, l=40, r=40),
        )
        
        # Display the bar chart
        st.plotly_chart(spending_bar, use_container_width=True)
    
    with tab3:
        st.markdown("<h3 style='text-align: center; color: #6739B7;'>Detailed Spending Analysis</h3>", unsafe_allow_html=True)
        
        # Get transactions for selected folders
        transactions = pd.DataFrame()
        for folder in selected_folders:
            folder_transactions = st.session_state.analytics.get_folder_transactions(folder)
            transactions = pd.concat([transactions, folder_transactions], ignore_index=True)
        
        if not transactions.empty:
            # Sort by date (newest first)
            transactions['timestamp'] = pd.to_datetime(transactions['timestamp'])
            transactions = transactions.sort_values('timestamp', ascending=False)
            
            # Format amounts
            transactions['formatted_amount'] = transactions['amount'].apply(lambda x: f"₹{x:.2f}")
            transactions['formatted_date'] = transactions['timestamp'].dt.strftime('%d %b %Y, %I:%M %p')
            
            # Group transactions by folder and merchant
            merchant_spending = transactions.groupby(['folder', 'merchant'])['amount'].sum().reset_index()
            merchant_spending = merchant_spending.sort_values(['folder', 'amount'], ascending=[True, False])
            
            # Display top merchants per folder
            for folder in selected_folders:
                folder_merchants = merchant_spending[merchant_spending['folder'] == folder]
                
                if not folder_merchants.empty:
                    st.markdown(f"""
                        <div style="background-color: #e9e0ff; padding: 15px; border-radius: 10px; margin: 15px 0;">
                            <h4 style="margin-top: 0; color: #6739B7;">📁 {folder} - Top Merchants</h4>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Create a horizontal bar chart for merchants
                    merchant_bar = px.bar(
                        folder_merchants.head(5),
                        x='amount',
                        y='merchant',
                        orientation='h',
                        labels={'amount': 'Amount (₹)', 'merchant': 'Merchant'},
                        color='amount',
                        color_continuous_scale='Viridis',
                        text='amount'
                    )
                    
                    # Customize the merchant bar chart
                    merchant_bar.update_traces(
                        texttemplate='₹%{text:.2f}',
                        textposition='outside'
                    )
                    
                    # Set the theme and layout
                    merchant_bar.update_layout(
                        height=300,
                        margin=dict(t=20, b=20, l=20, r=20),
                        yaxis=dict(autorange="reversed")
                    )
                    
                    # Display the merchant bar chart
                    st.plotly_chart(merchant_bar, use_container_width=True)
        else:
            st.info("No transaction data available for the selected folders.")

def show_notifications():
    """Display notifications page with alerts and spending limit messages"""
    # Page title
    st.title("Notifications")
    
    # PhonePe-like header
    st.markdown("""
        <div class="phonepe-header">
            🔔 Notification Center
        </div>
    """, unsafe_allow_html=True)
    
    # Get notifications
    notifications = st.session_state.notification_manager.get_notifications()
    
    # Mark all as read button
    if not notifications.empty:
        if st.button("📖 Mark all as read", key="mark_all_read"):
            st.session_state.notification_manager.mark_all_as_read()
            st.success("All notifications marked as read!")
            st.rerun()
    
    # Display notifications
    if not notifications.empty:
        # Format the timestamp
        notifications['formatted_date'] = pd.to_datetime(notifications['timestamp']).dt.strftime('%d %b %Y, %I:%M %p')
        
        # Create a container for notifications
        st.markdown("""
            <div style="background-color: white; padding: 15px; border-radius: 10px; margin-top: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h3 style="color: #6739B7; margin-bottom: 15px; text-align: center;">Your Notifications</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Display individual notifications
        for i, notification in notifications.iterrows():
            # Different styling based on notification type
            if notification['type'] == 'limit_exceeded':
                icon = "⚠️"
                color = "#dc3545"  # Red
                bg_color = "#fff5f5"
                border = "4px solid #dc3545"
            else:
                icon = "ℹ️"
                color = "#6739B7"  # PhonePe Purple
                bg_color = "#f9f9f9"
                border = "4px solid #6739B7"
            
            # Read/unread status
            read_status = "Read" if notification['read'] else "Unread"
            read_color = "#6c757d" if notification['read'] else "#28a745"
            
            with st.container():
                st.markdown(f"""
                    <div style="border-left: {border}; padding: 15px; margin: 10px 0; background-color: {bg_color}; border-radius: 5px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h4 style="margin: 0; color: {color};">{icon} {notification['type'].replace('_', ' ').title()}</h4>
                            <p style="margin: 0; color: {read_color}; font-size: 14px;">{read_status}</p>
                        </div>
                        <p style="margin: 10px 0; color: #333; font-size: 16px;">{notification['message']}</p>
                        <p style="margin: 5px 0 0; color: #666; font-size: 14px;">{notification['formatted_date']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Mark as read button for unread notifications
                if not notification['read']:
                    if st.button("Mark as read", key=f"read_{i}"):
                        st.session_state.notification_manager.mark_as_read(i)
                        st.success(f"Notification marked as read!")
                        st.rerun()
    else:
        # No notifications
        st.markdown("""
            <div style="background-color: #f8f8f8; padding: 30px; border-radius: 10px; text-align: center; margin-top: 20px;">
                <h3 style="color: #6739B7; margin-bottom: 10px;">No Notifications</h3>
                <p>You don't have any notifications at the moment.</p>
                <p>You'll receive notifications here when you exceed your spending limits.</p>
            </div>
        """, unsafe_allow_html=True)
        
    # Simulated phone notification section
    st.markdown("""
        <div style="background-color: white; padding: 15px; border-radius: 10px; margin-top: 30px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h3 style="color: #6739B7; margin-bottom: 15px; text-align: center;">Phone Notification Settings</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Phone notification settings
    st.markdown("""
        <div style="background-color: #f8f8f8; padding: 15px; border-radius: 10px; margin: 15px 0;">
            <p style="margin: 0 0 10px 0; font-weight: bold;">You'll receive push notifications on your phone when:</p>
            <ul style="margin: 0; padding-left: 20px;">
                <li>You exceed your folder spending limits</li>
                <li>A folder is nearing its spending limit (80% or higher)</li>
                <li>Your monthly spending patterns change significantly</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()