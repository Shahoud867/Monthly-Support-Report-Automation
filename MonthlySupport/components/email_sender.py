import smtplib
from email.mime.text import MIMEText
from langflow.custom import Component
from langflow.io import Output, Input, StrInput, SecretStrInput
from langflow.schema import Data

class EmailSender(Component):
    display_name = "Email Sender"
    description = "Send email report to specified recipient"
    
    inputs = [
        Input(display_name="Report Content", name="report_input"),
        StrInput(name="discord_username", display_name="Discord Username", value="SupportAnalyst"),
        StrInput(name="sender_email", display_name="Sender Email", value="your-email@gmail.com"),
        SecretStrInput(name="sender_password", display_name="App Password")
    ]
    
    outputs = [
        Output(display_name="Email Status", name="email_status", method="send_email")
    ]
    
    def send_email(self) -> Data:
        report = self.report_input.value
        
        # Extract month from report
        month = "2025-05"
        if "Summary for" in report:
            month = report.split("Summary for ")[1].split("\n")[0]
        
        subject = f"Monthly Support Ticket Report – {month} – {self.discord_username}"
        
        try:
            # Create email message
            msg = MIMEText(report)
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = "contact@langflow.org"
            
            # Send email via Gmail SMTP
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            status = "sent"
            message = f"Email sent successfully to contact@langflow.org"
            
        except Exception as e:
            status = "failed"
            message = f"Failed to send email: {str(e)}"
        
        email_data = {
            "to": "contact@langflow.org",
            "subject": subject,
            "body": report,
            "status": status,
            "message": message
        }
        
        return Data(value=email_data)