import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()


class WhatsAppSender:

    def __init__(self) -> None:
        self.sid = os.getenv("TWILIO_SID")
        self.token = os.getenv("TWILIO_AUTH_TOKEN")
        self.whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
        self.client = Client(self.sid, self.token)

    def send_whatsapp(self, to_number: str, otp: str) -> bool:
        message_body = f"Your ESMS Account Verification OTP is: {otp}"

        try:
            self.client.messages.create(
                body=message_body,
                from_=self.whatsapp_number,
                to=f"whatsapp:{to_number}"
            )
            return True

        except Exception as exc:
            print("WhatsApp sending failed:", exc)
            return False
