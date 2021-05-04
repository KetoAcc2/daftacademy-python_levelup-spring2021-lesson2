import secrets
from typing import List

import uvicorn
from hashlib import sha256
from fastapi import FastAPI, Response, status, Request, Depends, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import HTMLResponse

app = FastAPI()

app.secret_key = "very constant and random secret, best 64+ characters, I love elephants and bananas"
app.key_counter = 1
app.access_tokens = []

security = HTTPBasic()


@app.get("/welcome_session")
def welcome_session(response: Response, format: str = None, token: str = Cookie(None)):
    print("token:", token)

    if (token is not None) and (token in app.access_tokens):
        response.status_code = status.HTTP_200_OK

        if format == 'json':
            response.media_type = 'json'
            return {"message": "Welcome!"}
        else:
            if format == 'html':
                response.media_type = 'html'
                return HTMLResponse("<h1>Welcome!</h1>", status_code=200, media_type='text/html')
            else:
                response.media_type = 'plain'
                return Response("Welcome!", 200, media_type='text/plain')

    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response


@app.get("/welcome_token")
def welcome_token(response: Response, token: str = None, format: str = None):

    print("token:", token)

    if (token is not None) and (token in app.access_tokens):
        response.status_code = status.HTTP_200_OK

        if format == 'json':
            response.media_type = 'json'
            return {"message": "Welcome!"}
        else:
            if format == 'html':
                response.media_type = 'html'
                return HTMLResponse("<h1>Welcome!</h1>", status_code=200, media_type='text/html')
            else:
                response.media_type = 'plain'
                return Response("Welcome!", 200, media_type='text/plain')

    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response


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
    response.set_cookie(key="token", value=session_token)

    app.key_counter += 1

    return response


@app.post("/login_token")
def login_token(*, response: Response, credentials: HTTPBasicCredentials = Depends(security),
                session_token: str = Cookie(None)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")

    if correct_username and correct_password:
        app.secret_key += str(app.key_counter)
        preparing_session_token = sha256(f"{correct_username}{correct_password}{app.secret_key}".encode()).hexdigest()
        app.access_tokens.append(preparing_session_token)
        response.set_cookie(key="token", value=preparing_session_token)

        app.key_counter += 1

        response.status_code = status.HTTP_201_CREATED
        return {"token": preparing_session_token}

    if session_token in app.access_tokens:
        response.status_code = status.HTTP_201_CREATED
        return {"token": session_token}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response


if __name__ == "__main__":
    uvicorn.run(app)
