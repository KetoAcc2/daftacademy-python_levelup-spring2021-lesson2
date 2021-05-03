import secrets
from hashlib import sha256

import uvicorn
from fastapi import FastAPI, Response, status, Request, Depends
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

app.secret_key = "very constant and random secret, best 64+ characters, I love elephants and bananas"
app.access_tokens = []
app.session_token = str()

security = HTTPBasic()


@app.post("/login_session")
def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    response.status_code = status.HTTP_201_CREATED

    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")

    if not (correct_username and correct_password):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response

    session_token = sha256(f"{correct_username}{correct_password}{app.secret_key}".encode()).hexdigest()
    app.access_tokens.append(session_token)
    app.session_token = session_token
    response.set_cookie(key="session_token", value=session_token)

    return response


@app.post("/login_token")
def login_session(response: Response, request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")

    if not (correct_username and correct_password):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response

    session_token = request.cookies['session_token']
    if session_token == app.session_token:
        response.status_code = status.HTTP_201_CREATED
        return {"token": session_token}

    response.status_code = status.HTTP_401_UNAUTHORIZED
    return response


if __name__ == "__main__":
    uvicorn.run(app)
