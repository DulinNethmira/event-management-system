from twilio.rest import Client
from backend.app.api.core.config import settings

def send_sms_otp(to_phone: str, otp_code: str) -> bool:
    try:
        # Header: Initialization
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        # Header: Execution
        message = client.messages.create(
            body=f"Your Account Verification OTP code is : {otp_code}",
            from_=settings.TWILIO_SMS_NUMBER,
            to=to_phone
        )
        
        return True if message.sid else False
        
    except Exception as e:
        print(f"Twilio Error: {e}")
        return False