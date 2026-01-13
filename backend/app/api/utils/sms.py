import requests
from app.api.core.config import settings


def send_sms_otp(to_phone: str, otp_code: str) -> bool:
    try:
        url = "https://rest.nexmo.com/sms/json"
        
        message_text = f"""Infinity Events

Your Account Verification OTP code is: {otp_code}

This code expires in 5 minutes.

If you didn't request this code, please ignore this message."""
        
        payload = {
            "from": settings.VONAGE_FROM_NUMBER,
            "to": to_phone,
            "text": message_text,
            "api_key": settings.VONAGE_API_KEY,
            "api_secret": settings.VONAGE_API_SECRET
        }
        
        response = requests.post(url, json=payload)
        response_data = response.json()
        
        if response_data["messages"][0]["status"] == "0":
            print(f"SMS sent successfully to {to_phone}")
            print(f"Message ID: {response_data['messages'][0]['message-id']}")
            return True
        else:
            error_text = response_data["messages"][0].get("error-text", "Unknown error")
            print(f"SMS failed: {error_text}")
            return False
            
    except Exception as e:
        print(f"Vonage SMS Error: {e}")
        return False