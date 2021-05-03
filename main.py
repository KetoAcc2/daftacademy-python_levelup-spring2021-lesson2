from hashlib import sha256

import uvicorn
from fastapi import FastAPI, Response, status
from pydantic import BaseModel

app = FastAPI()

app.secret_key = "very constant and random secret, best 64+ characters, I love elephants and bananas"
app.access_tokens = []


class Data(BaseModel):
    login: str
    password: str


@app.post("/login_session")
def login_session(data: Data, response: Response):
    response.status_code = status.HTTP_201_CREATED

    if data.login is None or data.login != '4dm1n' or\
            data.password is None or data.password != 'NotSoSecurePa$$':
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response

    session_token = sha256(f"{data.login}{data.password}{app.secret_key}".encode()).hexdigest()
    app.access_tokens.append(session_token)
    response.set_cookie(key="session_token", value=session_token)

    return response


@app.post("/login_token")
def login_session(data: Data, response: Response):
    response.status_code = status.HTTP_201_CREATED

    if data.login is None or data.login != '4dm1n' or\
            data.password is None or data.password != 'NotSoSecurePa$$':
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response

    session_token = sha256(f"{data.login}{data.password}{app.secret_key}".encode()).hexdigest()
    app.access_tokens.append(session_token)
    response.set_cookie(key="session_token", value=session_token)

    return {"token": session_token}


if __name__ == "__main__":
    uvicorn.run(app)
