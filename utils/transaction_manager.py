import pandas as pd
import os
from datetime import datetime

class TransactionManager:
    def __init__(self):
        self.transactions_file = "data/transactions.csv"
        self._initialize_storage()
    
    def _initialize_storage(self):
        """Initialize the transactions storage file if it doesn't exist"""
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists(self.transactions_file):
            pd.DataFrame(columns=[
                'folder', 'amount', 'merchant', 'notes', 'timestamp'
            ]).to_csv(self.transactions_file, index=False)
    
    def add_transaction(self, transaction):
        """Add a new transaction"""
        transactions = pd.read_csv(self.transactions_file)
        transactions = transactions.append(transaction, ignore_index=True)
        transactions.to_csv(self.transactions_file, index=False)
    
    def get_all_transactions(self):
        """Get all transactions"""
        return pd.read_csv(self.transactions_file)
    
    def get_folder_transactions(self, folder):
        """Get transactions for a specific folder"""
        transactions = pd.read_csv(self.transactions_file)
        return transactions[transactions['folder'] == folder]
