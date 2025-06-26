# Email Service API

A REST API for sending emails through contact forms using FastAPI and Gmail SMTP. This service allows websites to send emails on behalf of users through a secure backend API.

## 🚀 Features

- **RESTful API** - Clean REST endpoints for email operations
- **Email Validation** - Built-in email address validation using Pydantic
- **CORS Support** - Cross-origin requests enabled for web integration
- **Secure SMTP** - Uses Gmail SMTP with app-specific passwords
- **Error Handling** - Comprehensive error handling and validation
- **Interactive Documentation** - Auto-generated API docs with Swagger/OpenAPI
- **Health Checks** - Built-in health monitoring endpoint

## 📋 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Examples](#examples)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- Gmail account with 2-factor authentication enabled
- App-specific password for Gmail

### Setup

1. **Clone or download the project**
   ```bash
   cd Email
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create environment file**
   ```bash
   # Create .env file in the project root
   touch .env
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
EMAIL_USER=your-gmail@gmail.com
EMAIL_PASS=your-app-password
```

### Gmail Setup

1. **Enable 2-Factor Authentication**
   - Go to your Google Account settings
   - Security → 2-Step Verification → Turn on

2. **Generate App Password**
   - Security → 2-Step Verification → App passwords
   - Select "Mail" and generate a password
   - Use this password in `EMAIL_PASS` (not your regular Gmail password)

## 🚀 Usage

### Starting the Server

```bash
# Development mode
python backend_ports.py

# Or using uvicorn directly
uvicorn backend_ports:app --host 0.0.0.0 --port 7860 --reload
```

The API will be available at:
- **API**: http://localhost:7860
- **Interactive Docs**: http://localhost:7860/docs
- **Custom Docs**: http://localhost:7860/documents

### Testing the Email Service

```bash
# Test the email service directly
python email_service.py
```

## 📚 API Endpoints

### Base Information

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Welcome message and API information |
| `/health` | GET | Health check endpoint |
| `/documents` | GET | Custom API documentation |
| `/docs` | GET | Interactive Swagger documentation |

### Email Operations

#### Send Email (JSON Body)
```http
POST /send-email
Content-Type: application/json

{
    "name": "John Doe",
    "email": "john@example.com", 
    "message": "Hello, this is a test message!",
    "to": "contact@yoursite.com"
}
```

#### Send Email (Query Parameters)
```http
POST /send-email-query?name=John%20Doe&email=john@example.com&message=Hello&to=contact@yoursite.com
```

### Response Format

**Success Response:**
```json
{
    "message": "Email from John Doe sent successfully to contact@yoursite.com!",
    "success": true
}
```

**Error Response:**
```json
{
    "error": "Configuration error: EMAIL_USER and EMAIL_PASS environment variables must be set",
    "success": false
}
```

## 🔧 Examples

### Python Client

```python
import requests
import json

# Using JSON body
url = "http://localhost:7860/send-email"
data = {
    "name": "Jane Smith",
    "email": "jane@example.com",
    "message": "Thank you for your service!",
    "to": "support@yourcompany.com"
}

response = requests.post(url, json=data)
print(response.json())
```

### JavaScript/Fetch

```javascript
fetch('http://localhost:7860/send-email', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        name: 'Mike Johnson',
        email: 'mike@example.com',
        message: 'Great website! Looking forward to hearing from you.',
        to: 'hello@yoursite.com'
    })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

### cURL

```bash
curl -X POST "http://localhost:7860/send-email" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Alice Brown",
       "email": "alice@example.com",
       "message": "Hello from cURL!",
       "to": "info@yourcompany.com"
     }'
```

### HTML Contact Form

```html
<!DOCTYPE html>
<html>
<head>
    <title>Contact Form</title>
</head>
<body>
    <form id="contactForm">
        <input type="text" id="name" placeholder="Your Name" required>
        <input type="email" id="email" placeholder="Your Email" required>
        <textarea id="message" placeholder="Your Message" required></textarea>
        <input type="hidden" id="to" value="contact@yoursite.com">
        <button type="submit">Send Message</button>
    </form>

    <script>
        document.getElementById('contactForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                message: document.getElementById('message').value,
                to: document.getElementById('to').value
            };
            
            try {
                const response = await fetch('http://localhost:7860/send-email', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                alert(result.message || result.error);
            } catch (error) {
                alert('Error sending message: ' + error.message);
            }
        });
    </script>
</body>
</html>
```

## 🔒 Security

### Best Practices

1. **Environment Variables**
   - Never commit `.env` file to version control
   - Use app-specific passwords, not regular Gmail passwords
   - Rotate passwords regularly

2. **Production Deployment**
   - Configure specific CORS origins instead of `"*"`
   - Use HTTPS in production
   - Implement rate limiting
   - Add authentication if needed

3. **Gmail Security**
   - Enable 2-factor authentication
   - Monitor account activity
   - Use app-specific passwords only

### Example Production CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourwebsite.com", "https://www.yourwebsite.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## 🐛 Troubleshooting

### Common Issues

1. **Authentication Failed**
   ```
   Error: Authentication failed
   ```
   - Ensure 2FA is enabled on Gmail
   - Use app-specific password, not regular password
   - Check EMAIL_USER and EMAIL_PASS in .env file

2. **Environment Variables Not Found**
   ```
   Error: EMAIL_USER and EMAIL_PASS environment variables must be set
   ```
   - Create .env file in project root
   - Check variable names match exactly
   - Restart the server after adding .env

3. **CORS Issues**
   ```
   Error: Access blocked by CORS policy
   ```
   - Check that CORS is properly configured
   - Verify the frontend domain is allowed

4. **Port Already in Use**
   ```
   Error: Address already in use
   ```
   - Change port in the uvicorn.run() call
   - Kill existing process: `lsof -ti:7860 | xargs kill -9` (Mac/Linux)

### Debug Mode

Enable debug logging by modifying the uvicorn run command:

```python
uvicorn.run(app, host="0.0.0.0", port=7860, log_level="debug")
```

## 📁 Project Structure

```
Email/
├── backend_ports.py      # FastAPI application and endpoints
├── email_service.py      # Email sending functionality
├── requirements.txt      # Python dependencies
├── readme.md            # Project documentation
├── .env                 # Environment variables (create this)
└── __pycache__/         # Python bytecode cache
```

## 🚀 Deployment

### Local Development

```bash
python backend_ports.py
```

### Production with Gunicorn

```bash
pip install gunicorn
gunicorn backend_ports:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:7860
```

### Docker (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 7860

CMD ["uvicorn", "backend_ports:app", "--host", "0.0.0.0", "--port", "7860"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review the logs for error details
3. Ensure all environment variables are properly set
4. Verify Gmail app password configuration

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Jatin**
- Date: June 26, 2025
- Email Service API v1.0.0

---

⭐ **Star this repository if it helped you!**