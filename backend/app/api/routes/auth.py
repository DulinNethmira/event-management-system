from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal
from backend.app.api.utils.verification_service import VerificationService

router = APIRouter(prefix="/auth", tags=["Auth"])
verification_service = VerificationService()


class VerificationRequest(BaseModel):
    method: Literal["email", "mobile"]
    receiver: str 


# Endpoint to send OTP via email or WhatsApp
@router.post("/send-verification")
async def send_verification(request: VerificationRequest):
    result = verification_service.send_verification(
        method=request.method,
        receiver=request.receiver
    )

    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail="Failed to send verification code"
        )

    return {"message": "Verification code sent successfully", "data": result}
