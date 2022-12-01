import os

from typing import Union
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.head("/")
@app.get("/", response_class=HTMLResponse)
async def read_items():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>Welcome to you own service!</title>
    <style>
    body {{ 
        width: 35em; margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif; 
        background-color: {os.getenv('BACKGROUND_COLOR')};
    }}
    </style>
    </head>
    <body>
    <h1>Welcome to you own service!</h1>
    <p>If you see this page, the web server is successfully installed and
    working. Further configuration is required.</p>
    </body>
    </html>
    """