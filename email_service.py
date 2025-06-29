import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# Load environment variables from .env file
load_dotenv()

# Email configuration - loaded from environment variables for security
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')  # Your Gmail address
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')  # Your Gmail app password

# Initialize the AI model for email content enhancement
model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

def enhance_email_content(content, Name):
    """
    Enhance email content using AI for clarity and professionalism.
    
    This function takes raw email content and uses a generative AI model to create
    a clear, professional summary that helps the recipient understand the email's
    purpose and main points.
    
    Args:
        content (str): The original email message content to be enhanced.
        Name (str): The name of the email sender.
    
    Returns:
        str: Enhanced email content with clear purpose statement and bullet points.
        
    Example:
        >>> enhanced = enhance_email_content("Need help with website", "John")
        >>> print(enhanced)
        Purpose: John is requesting assistance with website-related issues.
        • Requires help with website functionality
        • Seeking technical support
    """
    response = model.invoke(f"""
You are an AI assistant that generates clear summaries.
Note: Your function is to enhances the email content for clarity and professionalism. You are helping the reciver to understand the email's purpose and main points.

Instructions:
- Clearly state the purpose of the email in 2-3 sentences.
- Provide a concise summary of the main points as bullet points.
- Keep the tone professional.
- Don't use markdown formatting.

Sender's Name: {Name}
Email content:
{content}
"""
)
    return response.content.strip()

def enhanced_subject(Name, Message):
    """
    Generate an enhanced email subject line using AI.
    
    Creates a concise, professional subject line for contact form submissions
    based on the sender's name and message content. The subject line is
    optimized for email readability and limited to appropriate length.
    
    Args:
        Name (str): The name of the email sender.
        Message (str): The email message content to base the subject on.
    
    Returns:
        str: A concise email subject line (maximum 78 characters) that
             summarizes the email's purpose.
             
    Example:
        >>> subject = enhanced_subject("John Doe", "I need help with my website")
        >>> print(subject)
        "Contact Form: John Doe - Website Support Request"
    """
    response = model.invoke(
        f"Generate a concise email subject line (maximum 50 characters) for a contact form submission "
        f"from {Name}. Message: {Message}... "
        f"Return only the subject line without any extra text or formatting."
    )
    # Clean the response to remove any newlines or carriage returns
    subject = response.content.strip().replace('\n', ' ').replace('\r', ' ')
    # Limit length to prevent overly long subjects
    return subject[:78] if len(subject) > 78 else subject


def send_email(Name, Email, Message, To):
    """
    Send an email with AI-enhanced content through Gmail SMTP server.
    
    This function processes contact form submissions by enhancing the email content
    with AI-generated summaries and sending them via Gmail's SMTP server. The email
    includes both the AI-enhanced summary and the original message.
    
    Args:
        Name (str): The name of the person sending the email.
        Email (str): The email address of the sender (for contact purposes).
        Message (str): The original message content to be sent.
        To (str): The recipient's email address.
    
    Returns:
        bool: True if email was sent successfully.
        
    Raises:
        ValueError: If EMAIL_USER or EMAIL_PASS environment variables are not set.
        smtplib.SMTPAuthenticationError: If Gmail authentication fails.
        smtplib.SMTPException: If any SMTP-related error occurs.
        Exception: For any other unexpected errors.
        
    Example:
        >>> success = send_email(
        ...     Name="John Doe",
        ...     Email="john@example.com", 
        ...     Message="I need help with my website",
        ...     To="support@company.com"
        ... )
        Email sent successfully!
        >>> print(success)
        True
        
    Note:
        Requires the following environment variables to be set:
        - EMAIL_USER: Your Gmail email address
        - EMAIL_PASS: Your Gmail app password (not regular password)
    """
    # Validate that required environment variables are set
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise ValueError("EMAIL_USER and EMAIL_PASS environment variables must be set")

    # Create email message object
    msg = EmailMessage()
    # Enhance the email content using generative AI
    enhanced_content = enhance_email_content(Message, Name)
    # Generate an enhanced subject line
    enhanced_subject_line = enhanced_subject(Name, enhanced_content)

    msg['Subject'] = enhanced_subject_line
    msg['From'] = EMAIL_ADDRESS  # Sender's email
    msg['To'] = To  # Recipient's email

    # Set email body with sender's information
    msg.set_content(
    f"""Message from {Name}
    Email:({Email}):
    AI Assisted Summary:
    {enhanced_content}

    
    Original Message:
    {Message}""")

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
