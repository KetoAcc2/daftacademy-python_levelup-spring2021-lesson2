from hashlib import sha256

import uvicorn
from fastapi import FastAPI, Response, status, Request
from pydantic import BaseModel

app = FastAPI()

app.secret_key = "very constant and random secret, best 64+ characters, I love elephants and bananas"
app.access_tokens = []
app.session_token = str()


class Data(BaseModel):
    login: str
    haslo: str


@app.post("/login_session")
def login_session(*, data: Data, response: Response):
    response.status_code = status.HTTP_201_CREATED

    if data.login is None or data.login != '4dm1n' or\
            data.haslo is None or data.haslo != 'NotSoSecurePa$$':
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response

    session_token = sha256(f"{data.login}{data.haslo}{app.secret_key}".encode()).hexdigest()
    app.access_tokens.append(session_token)
    app.session_token = session_token
    response.set_cookie(key="session_token", value=session_token)

    return response


@app.post("/login_token")
def login_session(*, data: Data, response: Response, request: Request):
    response.status_code = status.HTTP_201_CREATED

    if data.login is None or data.login != '4dm1n' or\
            data.haslo is None or data.haslo != 'NotSoSecurePa$$':
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response

    session_token = request.cookies['session_token']
    if session_token == app.session_token:
        return {"token": session_token}

    response.status_code = status.HTTP_401_UNAUTHORIZED
    return response


if __name__ == "__main__":
    uvicorn.run(app)
