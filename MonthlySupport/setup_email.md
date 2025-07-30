# Email Setup Instructions

## To Send Actual Emails:

### 1. Gmail App Password Setup:
1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account Settings → Security → App passwords
3. Generate an app password for "Mail"
4. Copy the 16-character password

### 2. Set Environment Variables:
```bash
# Windows
set SENDER_EMAIL=your-email@gmail.com
set SENDER_PASSWORD=your-app-password

# Linux/Mac
export SENDER_EMAIL=your-email@gmail.com
export SENDER_PASSWORD=your-app-password
```

### 3. Run with Email Sending:
```bash
python run.py
```

### 4. Alternative - Direct Parameters:
```python
from run import run_report
run_report(
    target_month="2025-05",
    sender_email="your-email@gmail.com", 
    sender_password="your-app-password"
)
```

## Security Note:
- Never commit credentials to code
- Use environment variables or secure credential storage
- App passwords are safer than regular passwords