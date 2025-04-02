import pandas as pd
import os
from datetime import datetime
import calendar
from datetime import date

class Analytics:
    def __init__(self):
        self.transactions_file = "data/transactions.csv"
    
    def get_folder_transactions(self, folder=None):
        """Get all transactions for a specific folder or all folders"""
        try:
            transactions = pd.read_csv(self.transactions_file)
            if transactions.empty:
                return pd.DataFrame(columns=['folder', 'merchant', 'amount', 'timestamp', 'notes'])
                
            # Convert timestamp to datetime
            transactions['timestamp'] = pd.to_datetime(transactions['timestamp'])
            
            # Sort by newest first
            transactions = transactions.sort_values('timestamp', ascending=False)
            
            if folder and folder != 'All Folders':
                return transactions[transactions['folder'] == folder]
            return transactions
        except Exception as e:
            print(f"Error getting folder transactions: {str(e)}")
            return pd.DataFrame(columns=['folder', 'merchant', 'amount', 'timestamp', 'notes'])
    
    def generate_analytics(self, date_range):
        """Generate analytics for the given date range"""
        try:
            transactions = pd.read_csv(self.transactions_file)
            transactions['timestamp'] = pd.to_datetime(transactions['timestamp'])
            transactions['date'] = transactions['timestamp'].dt.date
            
            # Filter by date range
            mask = (transactions['date'] >= date_range[0]) & (transactions['date'] <= date_range[1])
            filtered_transactions = transactions[mask]
            
            # Spending by folder
            spending_by_folder = filtered_transactions.groupby('folder')['amount'].sum().reset_index()
            
            # Spending trend
            spending_trend = filtered_transactions.groupby('date')['amount'].sum().reset_index()
            
            return {
                'spending_by_folder': spending_by_folder,
                'spending_trend': spending_trend
            }
        except Exception as e:
            print(f"Error generating analytics: {str(e)}")
            return {
                'spending_by_folder': None,
                'spending_trend': None
            }
    
    def get_current_month_spending(self, folder=None):
        """Get spending for the current month for a specific folder or all folders
        
        Args:
            folder: Folder name to check (None for all folders)
            
        Returns:
            dict: Spending data with total amount and percentage of limit
        """
        try:
            # Get current month's first and last day
            today = date.today()
            _, last_day = calendar.monthrange(today.year, today.month)
            first_day = date(today.year, today.month, 1)
            last_day = date(today.year, today.month, last_day)
            
            # Get transactions
            all_transactions = self.get_folder_transactions()
            if all_transactions.empty:
                return {
                    'amount': 0.0,
                    'limit': 0.0,
                    'percentage': 0.0,
                    'over_limit': False
                }
                
            # Add date column for filtering
            all_transactions['date'] = all_transactions['timestamp'].dt.date
            
            # Filter by date range (current month)
            current_month = all_transactions[(all_transactions['date'] >= first_day) & 
                                            (all_transactions['date'] <= last_day)]
            
            # Filter by folder if specified
            if folder and folder != 'All Folders':
                current_month = current_month[current_month['folder'] == folder]
                
            # Calculate total spending
            total_spending = current_month['amount'].sum() if not current_month.empty else 0.0
            
            # Return spending data
            return {
                'amount': total_spending,
                'period': f"{today.strftime('%B %Y')}"
            }
        except Exception as e:
            print(f"Error calculating spending: {str(e)}")
            return {
                'amount': 0.0,
                'period': f"{date.today().strftime('%B %Y')}"
            }
            
    def check_folder_limit(self, folder_name, folder_manager):
        """Check if a folder has exceeded its spending limit
        
        Args:
            folder_name: Name of the folder to check
            folder_manager: FolderManager instance to get limit
            
        Returns:
            dict: Spending data with limit check results
        """
        try:
            # Get spending limit for the folder
            limit = folder_manager.get_spending_limit(folder_name)
            
            # If no limit is set (0), return no limit
            if limit <= 0:
                return {
                    'has_limit': False,
                    'limit': 0.0,
                    'current': 0.0,
                    'percentage': 0.0,
                    'over_limit': False
                }
                
            # Get current month's spending
            spending = self.get_current_month_spending(folder_name)
            current_amount = spending['amount']
            
            # Calculate percentage of limit
            percentage = (current_amount / limit) * 100 if limit > 0 else 0.0
            
            # Return limit check results
            return {
                'has_limit': True,
                'limit': limit,
                'current': current_amount,
                'percentage': percentage,
                'over_limit': current_amount > limit,
                'period': spending['period']
            }
        except Exception as e:
            print(f"Error checking limit: {str(e)}")
            return {
                'has_limit': False,
                'limit': 0.0,
                'current': 0.0,
                'percentage': 0.0,
                'over_limit': False,
                'period': f"{date.today().strftime('%B %Y')}"
            }
    
    def export_for_powerbi(self):
        """Export data in Power BI compatible format"""
        try:
            transactions = pd.read_csv(self.transactions_file)
            
            # Create separate dimension tables
            folders = transactions[['folder']].drop_duplicates()
            merchants = transactions[['merchant']].drop_duplicates()
            
            # Create fact table
            facts = transactions[['folder', 'merchant', 'amount', 'timestamp', 'notes']]
            
            # Export files
            export_path = "data/powerbi_export"
            if not os.path.exists(export_path):
                os.makedirs(export_path)
            
            folders.to_csv(f"{export_path}/folders.csv", index=False)
            merchants.to_csv(f"{export_path}/merchants.csv", index=False)
            facts.to_csv(f"{export_path}/transactions.csv", index=False)
            
            return True
        except Exception as e:
            print(f"Error exporting data: {str(e)}")
            return False
