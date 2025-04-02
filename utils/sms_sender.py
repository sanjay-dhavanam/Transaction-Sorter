import os
from twilio.rest import Client

# Environment variables for Twilio
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")

class SMSSender:
    def __init__(self):
        """Initialize SMS sender with Twilio credentials"""
        self.is_configured = all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER])
        if self.is_configured:
            self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            self.phone_number = TWILIO_PHONE_NUMBER
        
    def send_limit_exceeded_notification(self, user_phone, folder_name, current_amount, limit_amount):
        """Send SMS notification when a folder spending limit is exceeded
        
        Args:
            user_phone: User's phone number (must include country code, e.g., +1234567890)
            folder_name: Name of the folder that exceeded limit
            current_amount: Current spending amount
            limit_amount: The spending limit that was exceeded
        
        Returns:
            dict: Status and message details
        """
        if not self.is_configured:
            return {
                "success": False,
                "message": "Twilio is not configured. Please add TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER to environment variables."
            }
        
        try:
            # Calculate the percentage
            percentage = (current_amount / limit_amount) * 100
            
            # Format the message
            message_body = (
                f"📊 PhonePe Spending Alert!\n\n"
                f"Your '{folder_name}' folder has exceeded the spending limit.\n\n"
                f"• Current spending: ₹{current_amount:.2f}\n"
                f"• Spending limit: ₹{limit_amount:.2f}\n"
                f"• Percentage: {percentage:.1f}%\n\n"
                f"Login to your app to review your transactions and adjust your spending habits."
            )
            
            # Send the message
            message = self.client.messages.create(
                body=message_body,
                from_=self.phone_number,
                to=user_phone
            )
            
            return {
                "success": True,
                "message": f"Notification sent successfully (SID: {message.sid})"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to send notification: {str(e)}"
            }
    
    def send_transaction_confirmation(self, user_phone, merchant, amount, folder):
        """Send SMS confirmation after a transaction is completed
        
        Args:
            user_phone: User's phone number with country code
            merchant: Merchant name or UPI ID
            amount: Transaction amount
            folder: Folder where transaction was saved
        
        Returns:
            dict: Status and message details
        """
        if not self.is_configured:
            return {
                "success": False,
                "message": "Twilio is not configured. Please add TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER to environment variables."
            }
        
        try:
            # Format the message
            message_body = (
                f"✅ Transaction Confirmed\n\n"
                f"• Paid to: {merchant}\n"
                f"• Amount: ₹{amount:.2f}\n"
                f"• Folder: {folder}\n\n"
                f"Thank you for using PhonePe!"
            )
            
            # Send the message
            message = self.client.messages.create(
                body=message_body,
                from_=self.phone_number,
                to=user_phone
            )
            
            return {
                "success": True,
                "message": f"Confirmation sent successfully (SID: {message.sid})"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to send confirmation: {str(e)}"
            }