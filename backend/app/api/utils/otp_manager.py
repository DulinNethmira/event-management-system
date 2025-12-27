import secrets
import string
import time
from typing import Dict, Any

OTP_LENGTH = 6
OTP_EXPIRY_SECONDS = 300 

_otp_db: Dict[str, Any] = {}

def generate_otp() -> str:
    return "".join(secrets.choice(string.digits) for _ in range(OTP_LENGTH))

def store_otp(receiver: str, otp: str) -> None:
    expiry_time = time.time() + OTP_EXPIRY_SECONDS
    _otp_db[receiver] = {
        "otp": otp,
        "expires_at": expiry_time
    }

def verify_otp_logic(receiver: str, otp_input: str) -> bool:
    record = _otp_db.get(receiver)

    if not record:
        return False

    if time.time() > record["expires_at"]:
        del _otp_db[receiver]
        return False

    if record["otp"] == otp_input:
        del _otp_db[receiver]
        return True

    return False