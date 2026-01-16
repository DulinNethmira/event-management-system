from datetime import timedelta, datetime
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from backend.app.main import app
from passlib.context import CryptContext
import jwt
from authlib.integrations.starlette_client import OAuth
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = "31a4203acf14f91f2ec26dd39eafcc4e79bd7720207ee728c091d39aa966ebcd"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token : str
    token_type : str

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str , hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict , expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expires_delta = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except jwt.PyJWTError:
        return None

#google facebook login auth

oauth = OAuth()

oauth.register(
    name='google',
    client_id='your-google-client-id',
    client_secret='your-google-client-secret',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    client_kwargs={'scope': 'openid profile email'},
)

oauth.register(
    name='facebook',
    client_id='your-facebook-client-id',
    client_secret='your-facebook-client-secret',
    authorize_url='https://www.facebook.com/v9.0/dialog/oauth',
    authorize_params=None,
    access_token_url='https://graph.facebook.com/v9.0/oauth/access_token',
    access_token_params=None,
    refresh_token_url=None,
    client_kwargs={'scope': 'email'},
)

#google facebook OAuth callback route
@app.route("/auth/google")
async def auth_google(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    return {"user" : user}

@app.route("/auth/facebook")
async def auth_facebook(request: Request):
    token = await oauth.facebook.authorize_access_token(request)
    user = await oauth.facebook.parse_id_token(request, token)
    return {"user" : user}

