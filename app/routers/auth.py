from fastapi import APIRouter, Depends, HTTPException, Form
from ..dependencies import get_current_user
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db
import requests

router = APIRouter()

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    # Keycloak token endpoint
    token_url = "http://localhost:8080/realms/sample/protocol/openid-connect/token"
    client_id = "sampleweb"
    client_secret = "AUbBkFW1d4yVeEEsjqBINc7tjGGUnd82"

    # Payload with credentials and grant type
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "username": username,
        "password": password,
        "grant_type": "password"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Request to Keycloak
    response = requests.post(token_url, data=payload, headers=headers)

    # Check if the authentication was successful
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    # Return the token
    return response.json()


@router.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # First, create user in Keycloak
    keycloak_admin_token = get_keycloak_admin_token()
    created_user = create_user_in_keycloak(keycloak_admin_token, user)

    if not created_user.keycloak_id:
        raise HTTPException(status_code=400, detail="Failed to create user in Keycloak")

    # Then, add additional details to FastAPI database
    db_user = crud.create_user(db=db, user=user)
    return db_user

def get_keycloak_admin_token():
    token_url = "http://localhost:8080/realms/sample/protocol/openid-connect/token"
    payload = {
        "client_id": "admin-cli",  # or your specific admin client
        "client_secret": "Yxn2QJU6bo5H2wuV3BKtVfptVYMRYtcz", # 
        "grant_type": "client_credentials"
    }
    response = requests.post(token_url, data=payload)
    return response.json().get("access_token")

def create_user_in_keycloak(admin_token, user: schemas.UserCreate):
    keycloak_url = "http://localhost:8080/admin/realms/sample/users"
    headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json"
    }
    print("email:", user.email)
    print("password:", user)
    payload = {
        "username": user.email,  # using email as username
        "email": user.email,
        "enabled": True,
        "credentials": [{
            "type": "password",
            "value": user.password,
            "temporary": False
        }],
        "firstName": user.first_name,
        "lastName": user.last_name
    }
    response = requests.post(keycloak_url, json=payload, headers=headers)
    
    if response.status_code == 201:
        user.keycloak_id= response.headers["Location"].split('/')[-1]  # Extracting Keycloak user ID
        return user
    else:
        return None
