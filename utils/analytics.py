import pandas as pd
import os
from datetime import datetime

class Analytics:
    def __init__(self):
        self.transactions_file = "data/transactions.csv"
    
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
