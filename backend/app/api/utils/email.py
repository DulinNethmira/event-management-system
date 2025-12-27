import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.app.api.core.config import settings

# If you want to use a simple SMTP approach (Gmail, Outlook, etc.)
def send_email_otp(to_email: str, otp_code: str) -> bool:
    try:
        # Standard SMTP Setup
        # Update these env variables in your .env file
        sender_email = settings.EMAIL_USERNAME
        sender_password = settings.EMAIL_PASSWORD
        smtp_server = settings.EMAIL_HOST
        smtp_port = settings.EMAIL_PORT

        message = MIMEMultipart("alternative")
        message["Subject"] = "Your Verification Code"
        message["From"] = sender_email
        message["To"] = to_email

        # Email Body
        text = f"Your verification code is: {otp_code}"
        html = f"""
        <html>
          <body>
            <p>Your verification code is: <b>{otp_code}</b></p>
            <p>This code expires in 5 minutes.</p>
          </body>
        </html>
        """

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        # Sending Logic
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())
            
        return True

    except Exception as e:
        print(f"Email Error: {e}")
        # Return False so the API knows it failed, but doesn't crash
        return False