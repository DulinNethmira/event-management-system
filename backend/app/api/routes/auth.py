from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Literal
from backend.app.api.utils.verification_service import VerificationService

router = APIRouter(tags=["Auth"])

# --- Schemas ---
class VerificationRequest(BaseModel):
    method: Literal["email", "mobile"]
    receiver: str = Field(..., min_length=5)

class VerifyOTPRequest(BaseModel):
    receiver: str
    otp: str

# --- Dependency ---
def get_verification_service():
    return VerificationService()

# --- Endpoints ---
@router.post("/send-verification", status_code=status.HTTP_200_OK)
async def send_verification(
    request: VerificationRequest,
    service: VerificationService = Depends(get_verification_service)
):
    try:
        # ADD 'await' HERE
        result = await service.send_verification(
            method=request.method,
            receiver=request.receiver
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("message", "Failed to send verification")
            )
            
        return {"message": "Verification code sent successfully", "data": result}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/verify-otp", status_code=status.HTTP_200_OK)
async def verify_otp(
    request: VerifyOTPRequest,
    service: VerificationService = Depends(get_verification_service)
):
    # This logic is still sync (in-memory db), so no await needed yet
    is_valid = service.verify_code(request.receiver, request.otp)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
        
    return {"message": "Verification successful"}