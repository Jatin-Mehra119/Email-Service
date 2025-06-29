"""
Email Service Module

This module provides functionality to send emails through SMTP using Gmail's SMTP server.
It's designed to handle contact form submissions from websites, sending emails on behalf
of users using your own email credentials.

Author: Jatin
Date: June 26, 2025
Dependencies: python-dotenv, smtplib (built-in)

Required Environment Variables:
    EMAIL_USER: Your Gmail email address
    EMAIL_PASS: Your Gmail app password (not your regular password)

Security Note:
    - Use app-specific passwords for Gmail, not your regular password
    - Store credentials in .env file, never in source code
    - Enable 2-factor authentication on your Gmail account before generating app passwords
"""

import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Email configuration - loaded from environment variables for security
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')  # Your Gmail address
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')  # Your Gmail app password

def send_email(Name, Email, Message, To):
    """
    Send an email using Gmail's SMTP server.

    This function sends an email on behalf of a contact form user using your own
    Gmail credentials. The actual sender's information is included in the email body
    and subject line for identification.

    Args:
        Name (str): The name of the person sending the message
        Email (str): The email address of the person sending the message
        Message (str): The content/body of the message to be sent
        To (str): The recipient's email address where the message will be delivered

    Returns:
        bool: True if email was sent successfully
    """
    # Validate that required environment variables are set
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise ValueError("EMAIL_USER and EMAIL_PASS environment variables must be set")

    # Create email message object
    msg = EmailMessage()
    msg['Subject'] = f"Email from {Name} through your website contact form"
    msg['From'] = EMAIL_ADDRESS  # Your email (the authenticated sender)
    msg['To'] = To  # Recipient's email

    # Set email body with sender's information
    msg.set_content(f"Message from {Name} ({Email}):\n\n{Message}")

    try:
        # Connect to Gmail SMTP server with STARTTLS encryption
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print("Email sent successfully!")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"Authentication failed: {e}")
        print("Check your email credentials and ensure 2FA is enabled with app password")
        raise
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

# Example usage and testing
if __name__ == "__main__":
    """
    Example usage of the email service.

    This section demonstrates how to use the send_email function and provides
    important setup information for developers.
    """
    try:
        send_email(
            Name="John Doe",
            Email="Xyz@gmail.com",
            Message="Hello, this is a test message.",
            To="jatinmehra119@gmail.com"
        )
    except Exception as e:
        print(f"Failed to send email: {e}")

    """
    SETUP INSTRUCTIONS:

    1. Create a .env file in the same directory with:
       EMAIL_USER=your-gmail@gmail.com
       EMAIL_PASS=your-app-password

    2. Gmail Setup:
       - Enable 2-factor authentication on your Gmail account
       - Generate an app-specific password (not your regular password)
       - Use the app password in the EMAIL_PASS variable

    3. Install required dependencies:
       pip install python-dotenv

    USAGE NOTES:

    - Name: The name of the person sending the email
    - Email: Their email address (for identification in the email body)
    - Message: The content of the email they want to send
    - To: The recipient's email address (usually your contact email)
    """