import secrets
from hashlib import sha256

import uvicorn
from fastapi import FastAPI, Response, status, Request, Depends, Cookie
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

app.secret_key = "very constant and random secret, best 64+ characters, I love elephants and bananas"
app.key_counter = 1
app.access_tokens = []

security = HTTPBasic()


@app.post("/login_session")
def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    response.status_code = status.HTTP_201_CREATED

    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")

    if not (correct_username and correct_password):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response

    app.secret_key += str(app.key_counter)
    session_token = sha256(f"{correct_username}{correct_password}{app.secret_key}".encode()).hexdigest()
    app.access_tokens.append(session_token)
    response.set_cookie(key="session_token", value=session_token)

    app.key_counter += 1

    return response


@app.post("/login_token")
def login_session(*, response: Response, credentials: HTTPBasicCredentials = Depends(security),
                  session_token: str = Cookie(None)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")

    if not (correct_username and correct_password):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response

    if session_token in app.access_tokens:
        app.secret_key += str(app.key_counter)
        preparing_session_token = sha256(f"{correct_username}{correct_password}{app.secret_key}".encode()).hexdigest()
        app.access_tokens.append(preparing_session_token)
        response.set_cookie(key="session_token", value=preparing_session_token)

        app.key_counter += 1

        response.status_code = status.HTTP_201_CREATED
        return {"token": session_token}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response


if __name__ == "__main__":
    uvicorn.run(app)
