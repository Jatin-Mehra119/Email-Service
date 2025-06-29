# Email Service API

A REST API for sending emails through contact forms using FastAPI and Gmail SMTP with AI-enhanced content generation.

## Features

- RESTful API with FastAPI
- AI-enhanced email content and subject lines
- Gmail SMTP integration
- Email validation with Pydantic
- CORS support for web integration
- Comprehensive error handling

## Quick Start

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure environment**
Create a `.env` file:
```env
EMAIL_USER=your-gmail@gmail.com
EMAIL_PASS=your-app-password
GOOGLE_API_KEY=your-google-api-key
```

3. **Run the service**
```bash
python backend_ports.py
```

API available at: http://localhost:7860

**Live API**: https://email-service-9f1z.onrender.com/docs

## API Usage

**Endpoint**: `POST /send-email`

**Live Endpoint**: https://email-service-9f1z.onrender.com/send-email

**Request**:
```json
{
    "name": "John Doe",
    "email": "john@example.com", 
    "message": "Hello, this is a test message!",
    "to": "contact@yoursite.com"
}
```

**Response**:
```json
{
    "message": "Email from John Doe sent successfully!",
    "success": true
}
```

### Example Usage

```bash
curl -X POST "https://email-service-9f1z.onrender.com/send-email" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "message": "Hello, this is a test message!",
    "to": "contact@yoursite.com"
  }'
```

## Gmail Setup

1. Enable 2-Factor Authentication in your Google Account
2. Generate App Password: Security → 2-Step Verification → App passwords
3. Use the app password in your `.env` file

## Google AI Setup

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key for Gemini
3. Add the API key to your `.env` file as `GOOGLE_API_KEY`

## Requirements

- Python 3.7+
- Gmail account with 2FA enabled
- App-specific password for Gmail
- Google API key for AI features