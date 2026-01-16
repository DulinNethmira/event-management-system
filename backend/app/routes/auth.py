# from fastapi import APIRouter, Depends, Request
# from backend.app.api.core.security import oauth

# router = APIRouter()

# #route to handle Google OAuth
# @router.get("/auth/google")
# async def auth_google(request: Request):
#     token = await oauth.google.authorize_access_token(request)
#     user = await oauth.google.parse_id_token(request, token)
#     return {"user": user}

# # Route to handle Facebook OAuth
# @router.get("/auth/facebook")
# async def auth_facebook(request: Request):
#     token = await oauth.facebook.authorize_access_token(request)
#     user = await oauth.facebook.parse_id_token(request, token)
#     return {"user": user}