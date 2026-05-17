import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

class EmailNotifier:
    """Send email notifications to users"""
    
    def __init__(self):
        self.config = Config()
    
    def send_notification(self, to_email, subject, message, complaint_id=None):
        """Send email notification"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.config.EMAIL_ADDRESS
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Create HTML and plain text versions
            text_content = message
            html_content = self._create_html_template(message, complaint_id)
            
            # Attach parts
            part1 = MIMEText(text_content, 'plain')
            part2 = MIMEText(html_content, 'html')
            
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.config.SMTP_SERVER, self.config.SMTP_PORT) as server:
                server.starttls()
                server.login(self.config.EMAIL_ADDRESS, self.config.EMAIL_PASSWORD)
                server.send_message(msg)
            
            print(f"✓ Notification sent to {to_email}")
            return True
        
        except Exception as e:
            print(f"✗ Error sending notification: {e}")
            return False
    
    def send_complaint_received(self, to_email, complaint_id, subject):
        """Send complaint received confirmation"""
        message = f"""
Dear Customer,

Thank you for contacting us. We have received your complaint.

Complaint ID: #{complaint_id}
Subject: {subject}

We will review your complaint and get back to you shortly.

Best regards,
Complaint Management Team
        """
        
        return self.send_notification(
            to_email,
            f"Complaint Received - #{complaint_id}",
            message,
            complaint_id
        )
    
    def send_status_update(self, to_email, complaint_id, subject, old_status, new_status):
        """Send status update notification"""
        message = f"""
Dear Customer,

Your complaint status has been updated.

Complaint ID: #{complaint_id}
Subject: {subject}
Previous Status: {old_status}
New Status: {new_status}

Thank you for your patience.

Best regards,
Complaint Management Team
        """
        
        return self.send_notification(
            to_email,
            f"Complaint Status Updated - #{complaint_id}",
            message,
            complaint_id
        )
    
    def send_complaint_resolved(self, to_email, complaint_id, subject):
        """Send complaint resolved notification"""
        message = f"""
Dear Customer,

We are pleased to inform you that your complaint has been resolved.

Complaint ID: #{complaint_id}
Subject: {subject}
Status: Resolved

If you have any further concerns, please feel free to contact us.

Thank you for your patience.

Best regards,
Complaint Management Team
        """
        
        return self.send_notification(
            to_email,
            f"Complaint Resolved - #{complaint_id}",
            message,
            complaint_id
        )
    
    def _create_html_template(self, message, complaint_id):
        """Create HTML email template"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .header {{
            background-color: #2563eb;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .content {{
            background-color: white;
            padding: 30px;
            margin-top: 20px;
            border-radius: 5px;
        }}
        .complaint-id {{
            font-size: 24px;
            font-weight: bold;
            color: #2563eb;
            margin: 10px 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            color: #666;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Complaint Management System</h1>
        </div>
        <div class="content">
            <pre style="white-space: pre-wrap; font-family: Arial, sans-serif;">{message}</pre>
        </div>
        <div class="footer">
            <p>This is an automated message. Please do not reply to this email.</p>
            <p>&copy; 2026 Complaint Management System</p>
        </div>
    </div>
</body>
</html>
        """
