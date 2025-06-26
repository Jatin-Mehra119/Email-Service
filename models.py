from pydantic import BaseModel, EmailStr

# Pydantic models for request/response validation
class EmailRequest(BaseModel):
    """
    Email request model for structured data validation.
    
    Attributes:
        name (str): Name of the person sending the email
        email (EmailStr): Valid email address of the sender
        message (str): Content of the message to be sent
        to (str): Recipient email address
    """
    name: str
    email: EmailStr
    message: str
    to: str

class EmailResponse(BaseModel):
    """Response model for email sending operations."""
    message: str
    success: bool = True