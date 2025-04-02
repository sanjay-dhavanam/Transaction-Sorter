import pandas as pd
import os
from datetime import datetime

class NotificationManager:
    def __init__(self):
        self.notifications_file = "data/notifications.csv"
        self._initialize_storage()
    
    def _initialize_storage(self):
        """Initialize the notifications storage file if it doesn't exist"""
        if not os.path.exists(os.path.dirname(self.notifications_file)):
            os.makedirs(os.path.dirname(self.notifications_file))
            
        if not os.path.exists(self.notifications_file):
            # Create empty file with headers
            df = pd.DataFrame(columns=['timestamp', 'type', 'message', 'read'])
            df.to_csv(self.notifications_file, index=False)
    
    def add_limit_exceeded_notification(self, folder_name, current_amount, limit):
        """Add a notification when a user exceeds a spending limit
        
        Args:
            folder_name: The folder that exceeded the limit
            current_amount: Current spending amount
            limit: The limit that was exceeded
        """
        message = f"⚠️ Spending limit exceeded for '{folder_name}'! You have spent ₹{current_amount:.2f}, which is above your ₹{limit:.2f} limit."
        
        self.add_notification("limit_exceeded", message)
        
    def add_notification(self, notification_type, message):
        """Add a generic notification
        
        Args:
            notification_type: Type of notification (e.g., limit_exceeded, reminder)
            message: The notification message
        """
        # Create notification entry
        notification = {
            'timestamp': datetime.now(),
            'type': notification_type,
            'message': message,
            'read': False
        }
        
        try:
            # Read existing notifications
            if os.path.exists(self.notifications_file):
                notifications = pd.read_csv(self.notifications_file)
            else:
                notifications = pd.DataFrame(columns=['timestamp', 'type', 'message', 'read'])
            
            # Append new notification
            notifications = pd.concat([notifications, pd.DataFrame([notification])], ignore_index=True)
            
            # Save to file
            notifications.to_csv(self.notifications_file, index=False)
            return True
        except Exception as e:
            print(f"Error adding notification: {str(e)}")
            return False
    
    def get_notifications(self, unread_only=False):
        """Get all notifications or only unread ones
        
        Args:
            unread_only: If True, return only unread notifications
        
        Returns:
            DataFrame containing notifications
        """
        try:
            if os.path.exists(self.notifications_file):
                notifications = pd.read_csv(self.notifications_file)
                
                # Convert timestamp to datetime
                notifications['timestamp'] = pd.to_datetime(notifications['timestamp'])
                
                # Sort by newest first
                notifications = notifications.sort_values('timestamp', ascending=False)
                
                if unread_only:
                    return notifications[notifications['read'] == False]
                return notifications
            else:
                return pd.DataFrame(columns=['timestamp', 'type', 'message', 'read'])
        except Exception as e:
            print(f"Error getting notifications: {str(e)}")
            return pd.DataFrame(columns=['timestamp', 'type', 'message', 'read'])
    
    def mark_as_read(self, notification_index):
        """Mark a notification as read
        
        Args:
            notification_index: Index of the notification to mark as read
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            notifications = pd.read_csv(self.notifications_file)
            
            # Check if index exists
            if notification_index < len(notifications):
                notifications.loc[notification_index, 'read'] = True
                notifications.to_csv(self.notifications_file, index=False)
                return True
            return False
        except Exception as e:
            print(f"Error marking notification as read: {str(e)}")
            return False
    
    def mark_all_as_read(self):
        """Mark all notifications as read
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            notifications = pd.read_csv(self.notifications_file)
            notifications['read'] = True
            notifications.to_csv(self.notifications_file, index=False)
            return True
        except Exception as e:
            print(f"Error marking all notifications as read: {str(e)}")
            return False
    
    def get_unread_count(self):
        """Get the count of unread notifications
        
        Returns:
            int: Number of unread notifications
        """
        try:
            notifications = self.get_notifications(unread_only=True)
            return len(notifications)
        except Exception as e:
            print(f"Error getting unread count: {str(e)}")
            return 0