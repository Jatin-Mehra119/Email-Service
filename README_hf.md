---
license: apache-2.0
title: Email Service
emoji: 💻
colorFrom: red
colorTo: yellow
pinned: false
short_description: A REST API for sending emails through contact forms.
sdk: docker
---

# Email Service API

A REST API for sending emails through contact forms using FastAPI and Gmail SMTP. This service allows websites to send emails on behalf of users through a secure backend API.

## � Quick Links

- **Live API Documentation**: [https://jatinmehra-email-service.hf.space/docs](https://jatinmehra-email-service.hf.space/docs)
- **Repository**: [https://github.com/Jatin-Mehra119/Email-Service.git](https://github.com/Jatin-Mehra119/Email-Service.git)

## �🚀 Features

- **RESTful API** - Clean REST endpoints for email operations
- **Email Validation** - Built-in email address validation using Pydantic
- **CORS Support** - Cross-origin requests enabled for web integration
- **Secure SMTP** - Uses Gmail SMTP with app-specific passwords
- **Error Handling** - Comprehensive error handling and validation
- **Interactive Documentation** - Auto-generated API docs with Swagger/OpenAPI
- **Health Checks** - Built-in health monitoring endpoint

## 🛠️ Quick Start

### Clone the Repository

```bash
git clone https://github.com/Jatin-Mehra119/Email-Service.git
cd Email-Service
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Create a `.env` file in the project root:

```env
EMAIL_USER=your-gmail@gmail.com
EMAIL_PASS=your-app-password
```

### Run the Service

```bash
python backend_ports.py
```

The API will be available at:
- **Local API**: http://localhost:7860
- **Live API**: https://jatinmehra-email-service.hf.space/docs

## 📚 API Usage

### Send Email

**Endpoint**: `POST /send-email`

**Request Body**:
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
    "message": "Email from John Doe sent successfully to contact@yoursite.com!",
    "success": true
}
```

### Quick Example

```javascript
fetch('https://jatinmehra-email-service.hf.space/send-email', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        name: 'Jane Smith',
        email: 'jane@example.com',
        message: 'Hello from your website!',
        to: 'contact@yoursite.com'
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

## ⚙️ Gmail Setup

1. **Enable 2-Factor Authentication** in your Google Account
2. **Generate App Password**: Security → 2-Step Verification → App passwords
3. **Use the app password** in your `.env` file (not your regular Gmail password)

## � Common Issues

### Authentication Failed
- Enable 2FA on Gmail and use app-specific password
- Check EMAIL_USER and EMAIL_PASS in .env file

### Environment Variables Not Found
- Create .env file in project root
- Restart server after adding .env

### CORS Issues
- CORS is configured for all origins by default
- For production, configure specific origins

## 📁 Project Structure

```
Email-Service/
├── backend_ports.py      # FastAPI application
├── email_service.py      # Email functionality
├── requirements.txt      # Dependencies
├── readme.md            # Documentation
└── .env                 # Environment variables (create this)
```

## 👨‍� Author

**Jatin**
- GitHub: [Jatin-Mehra119](https://github.com/Jatin-Mehra119)
- Email Service API v1.0.0
- Date: June 26, 2025

---

⭐ **Star this repository if it helped you!**