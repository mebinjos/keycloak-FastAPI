## Run keycloak in Local

`docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:23.0.3 start-dev
`


## Create virtualenv

`virtualenv venv`

## Install Dependencies

`pip install -r requirements.txt`


## Run the app

`uvicorn main:app --reload`

