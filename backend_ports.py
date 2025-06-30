"""
FastAPI Email Service Backend

This module provides a REST API for sending emails through a web service.
It uses FastAPI framework and integrates with the email_service module to handle
email sending functionality.

Author: Jatin
Date: June 26, 2025
Port: 7860
Endpoints: /, /docs, /health, /send-email

Dependencies:
    - fastapi
    - uvicorn
    - email_service (local module)
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from email_service import send_email  # Import the send_email function from email_service.py
from fastapi.responses import FileResponse
from models import EmailRequest, EmailResponse
from datetime import datetime

# Create FastAPI application instance
app = FastAPI(
    title="Email Service API",
    description="A powerful REST API that transforms any website's contact form into an intelligent email delivery system with AI-enhanced content generation",
    version="1.0.0"
)

# Configure CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow all origins (configure specific domains for production)
    allow_credentials=True,     # Allow cookies and credentials
    allow_methods=["*"],        # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],        # Allow all headers
)

@app.get("/")
async def read_root():
    """Serve the main HTML page for the contact form."""
    return FileResponse("frontend/index.html")
    
@app.get("/documents", response_model=dict)
async def get_docs():
    """
    Return:
    Show the API documentation for the Email Service.
    """
    return {
        "title": "Email Service API Documentation",
        "version": "1.0.0",
        "description": "A simple email service API that allows sending emails through a contact form",
        "endpoints": {
            "/": {
                "method": "GET",
                "description": "Welcome message and basic API information"
            },
            "/health": {
                "method": "GET", 
                "description": "Health check endpoint to verify API status"
            },
            "/send-email": {
                "method": "POST",
                "description": "Send an email using the configured email service",
                "parameters": {
                    "name": {
                        "type": "string",
                        "required": True,
                        "description": "Name of the person sending the email"
                    },
                    "email": {
                        "type": "string", 
                        "required": True,
                        "description": "Email address of the sender"
                    },
                    "message": {
                        "type": "string",
                        "required": True,
                        "description": "The message content to be sent"
                    }
                },
                "response": {
                    "success": {
                        "message": "Email sent successfully!"
                    },
                    "error": {
                        "error": "Error description"
                    }
                },
                "example_usage": {
                    "curl": "curl -X POST 'http://localhost:7860/send-email?name=John%20Doe&email=john@example.com&message=Hello%20World'",
                    "python": {
                        "import requests": "",
                        "response": "requests.post('http://localhost:7860/send-email', params={'name': 'John Doe', 'email': 'john@example.com', 'message': 'Hello World'})"
                    }
                }
            }
        },
        "notes": [
            "This API uses Gmail SMTP for sending emails",
            "Environment variables EMAIL_USER and EMAIL_PASS must be configured",
            "CORS is enabled for all origins",
            "All endpoints return JSON responses"
        ]
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API status.
    
    Returns:
        dict: Current status of the API service
    """
    current_time = datetime.now().isoformat()
    return {
        "status": "healthy",
        "service": "Email Service API",
        "timestamp": current_time,
        "version": "1.0.0"
    }

@app.post("/send-email", response_model=EmailResponse)
async def send_email_endpoint(email_data: EmailRequest):
    """
    Send an email using the configured email service.
    
    Args:
        email_data (EmailRequest): Email data including sender info and message
        
    Returns:
        EmailResponse: Success message if email sent successfully
        
    Raises:
        HTTPException: If email sending fails
        
    Example:
        POST /send-email
        {
            "name": "John Doe",
            "email": "john@example.com",
            "message": "Hello, this is a test message!",
            "to": "contact@yoursite.com"
        }
    """
    try:
        # Call the email service function
        result = send_email(
            Name=email_data.name,
            Email=email_data.email,
            Message=email_data.message,
            To=email_data.to
        )
        
        if result:
            return EmailResponse(
                message=f"Email from {email_data.name} sent successfully to {email_data.to}!",
                success=True
            )
        else:
            raise HTTPException(status_code=500, detail="Email sending failed")
            
    except ValueError as ve:
        # Handle configuration errors (missing environment variables)
        raise HTTPException(
            status_code=500, 
            detail=f"Configuration error: {str(ve)}"
        )
    except Exception as e:
        # Handle any other errors
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to send email: {str(e)}"
        )

# Alternative endpoint with query parameters (for backward compatibility)
@app.post("/send-email-query")
async def send_email_query_endpoint(
    name: str = Query(..., description="Name of the person sending the email"),
    email: str = Query(..., description="Email address of the sender"),
    message: str = Query(..., description="Message content to be sent"),
    to: str = Query(..., description="Recipient email address")
):
    """
    Alternative endpoint to send email using query parameters.
    
    This endpoint provides backward compatibility for clients that prefer
    to send data as query parameters instead of JSON body.
    
    Args:
        name: Name of the person sending the email
        email: Email address of the sender  
        message: Message content to be sent
        to: Recipient email address
        
    Returns:
        dict: Success or error message
    """
    try:
        # Create EmailRequest object for validation
        email_data = EmailRequest(name=name, email=email, message=message, to=to)
        
        # Use the main endpoint logic
        result = await send_email_endpoint(email_data)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid input: {str(e)}")
    
if __name__ == "__main__":
    import uvicorn
    # Fixed host address - use "0.0.0.0" to bind to all interfaces or "127.0.0.1" for localhost only
    uvicorn.run(app, host="0.0.0.0", port=7860)