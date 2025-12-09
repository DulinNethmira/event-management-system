import os
import smtplib
from random import randint
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()


# Generate a 6-digit numeric OTP.
def generate_otp() -> str:
    return str(randint(100000, 999999))


class EmailSender:
    """Handles sending OTP emails with custom sender name and body."""

    def __init__(self, sender_name: str = "ESMS Support") -> None:
        self.host = os.getenv("EMAIL_HOST")
        self.port = int(os.getenv("EMAIL_PORT"))
        self.username = os.getenv("EMAIL_USERNAME")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.sender_name = sender_name  # Name shown in recipient inbox

    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """
        Send an email with subject & body.
        """
        msg = MIMEMultipart()
        msg["From"] = f"{self.sender_name} <{self.username}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.username, to_email, msg.as_string())
            return True

        except Exception as exc:
            print("Email sending failed:", exc)
            return False
