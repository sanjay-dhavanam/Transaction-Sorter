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
            pd.DataFrame(columns=['folder_name']).to_csv(self.folders_file, index=False)
    
    def create_folder(self, folder_name):
        """Create a new folder"""
        folders = pd.read_csv(self.folders_file)
        if folder_name not in folders['folder_name'].values:
            folders = folders.append({'folder_name': folder_name}, ignore_index=True)
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
