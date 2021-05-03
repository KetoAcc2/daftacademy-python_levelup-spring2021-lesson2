import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import Request
from datetime import datetime

app = FastAPI()


@app.get("/hello", response_class=HTMLResponse)
def read_main():
    today_date = datetime.now()
    today_date = today_date.strftime("%Y-%m-%d")
    return "<h1>" \
           "Hello! Today date is " + today_date + \
           "</h1>"


if __name__ == "__main__":
    uvicorn.run(app)
