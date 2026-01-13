from app.api.utils.email import send_email_otp 
from app.api.utils.sms import send_sms_otp
from app.api.utils.otp_manager import generate_otp, store_otp, verify_otp_logic


class VerificationService:
    
    async def send_verification(self, method: str, receiver: str) -> dict:
        otp_code = generate_otp()
        store_otp(receiver, otp_code)
        
        if method == "email":
            sent = send_email_otp(receiver, otp_code)
            return {
                "success": sent, 
                "message": "Email sent" if sent else "Email failed"
            }
            
        elif method == "mobile":
            sent = send_sms_otp(receiver, otp_code)
            return {
                "success": sent, 
                "message": "SMS sent" if sent else "SMS failed"
            }
            
        return {"success": False, "message": "Invalid method"}

    def verify_code(self, receiver: str, otp: str) -> bool:
        return verify_otp_logic(receiver, otp)