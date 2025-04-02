import pandas as pd
import os

class FolderManager:
    def __init__(self):
        self.folders_file = "data/folders.csv"
        self._initialize_storage()

    def _initialize_storage(self):
        """Initialize the folders storage file if it doesn't exist"""
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists(self.folders_file):
            pd.DataFrame(columns=['folder_name', 'spending_limit']).to_csv(self.folders_file, index=False)

    def create_folder(self, folder_name, spending_limit=0.0):
        """Create a new folder with optional spending limit
        
        Args:
            folder_name: Name of the folder
            spending_limit: Spending limit for this folder (0 = no limit)
        """
        folders = pd.read_csv(self.folders_file)
        if folder_name not in folders['folder_name'].values:
            # Using concat instead of the deprecated append method
            new_folder = pd.DataFrame({
                'folder_name': [folder_name],
                'spending_limit': [float(spending_limit)]
            })
            folders = pd.concat([folders, new_folder], ignore_index=True)
            folders.to_csv(self.folders_file, index=False)
            return True
        return False

    def delete_folder(self, folder_name):
        """Delete an existing folder"""
        folders = pd.read_csv(self.folders_file)
        folders = folders[folders['folder_name'] != folder_name]
        folders.to_csv(self.folders_file, index=False)

    def get_folders(self):
        """Get list of all folders"""
        folders = pd.read_csv(self.folders_file)
        return folders['folder_name'].tolist()
        
    def get_folder_details(self):
        """Get all folder details including spending limits"""
        folders = pd.read_csv(self.folders_file)
        # Ensure spending_limit column exists (for backward compatibility)
        if 'spending_limit' not in folders.columns:
            folders['spending_limit'] = 0.0
            folders.to_csv(self.folders_file, index=False)
        return folders
        
    def get_spending_limit(self, folder_name):
        """Get spending limit for a folder
        
        Returns:
            float: Spending limit (0 means no limit set)
        """
        folders = pd.read_csv(self.folders_file)
        # Ensure spending_limit column exists
        if 'spending_limit' not in folders.columns:
            folders['spending_limit'] = 0.0
            folders.to_csv(self.folders_file, index=False)
            
        if folder_name in folders['folder_name'].values:
            folder = folders[folders['folder_name'] == folder_name]
            return float(folder['spending_limit'].values[0])
        return 0.0
    
    def set_spending_limit(self, folder_name, limit):
        """Set spending limit for a folder
        
        Args:
            folder_name: Name of the folder
            limit: Spending limit (0 = no limit)
            
        Returns:
            bool: True if successful, False if folder not found
        """
        folders = pd.read_csv(self.folders_file)
        # Ensure spending_limit column exists
        if 'spending_limit' not in folders.columns:
            folders['spending_limit'] = 0.0
            
        if folder_name in folders['folder_name'].values:
            folders.loc[folders['folder_name'] == folder_name, 'spending_limit'] = float(limit)
            folders.to_csv(self.folders_file, index=False)
            return True
        return False