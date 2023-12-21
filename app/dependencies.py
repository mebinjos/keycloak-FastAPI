import requests
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from . import crud, models, schemas
from jose.backends import RSAKey
from jose.utils import base64url_decode
from sqlalchemy.orm import Session
from .database import get_db

def get_jwks(jwks_url):
    response = requests.get(jwks_url)
    return response.json()

def decode_verify_jwt(token, jwks_url, audience):
    jwks = get_jwks(jwks_url)
    try:
        # Decode and validate the token
        decoded_token = jwt.decode(token, jwks, algorithms=["RS256"], audience=audience)
        return decoded_token
    except jwt.JWTError as e:
        raise Exception(f"Token verification failed: {e}")

# Example usage
jwks_url = "http://localhost:8080/realms/sample/protocol/openid-connect/certs"
expected_audience = "account"  

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Optional[schemas.User]:
    try:
        # Decode and validate the token
        payload = decode_verify_jwt(token, jwks_url, expected_audience)
        username: str = payload.get("preferred_username")  # or "sub", etc.
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    
    # Here, you can fetch user details from your database if needed
    user = db.query(models.User).filter(models.User.email == username).first()
    return user

    # For simplicity, just returning a user object
    #return schemas.User(username=username, email=payload.get("email"))  # Adjust according to your schema
