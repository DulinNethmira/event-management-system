from typing import Literal
from backend.app.api.utils.email import EmailSender, generate_otp
from backend.app.api.utils.whatsapp import WhatsAppSender


class VerificationService:

    def __init__(self) -> None:
        self.email_sender = EmailSender()
        self.whatsapp_sender = WhatsAppSender()

    def send_verification(
        self,
        method: Literal["email", "mobile"],
        receiver: str
    ) -> dict:

        otp = generate_otp()

        if method == "email":
            subject = "Your ESMS Verification Code"
            body = f"Your verification OTP is: {otp}\n\nThis code expires in 5 minutes."

            status = self.email_sender.send_email(receiver, subject, body)

        elif method == "mobile":
            status = self.whatsapp_sender.send_whatsapp(receiver, otp)

        else:
            raise ValueError("Invalid verification method")

        return {
            "success": status,
            "otp": otp if status else None,
            "method": method,
            "receiver": receiver,
        }
