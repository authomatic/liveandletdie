# encoding: utf-8
from fastapi import FastAPI, Request

app = FastAPI()


@app.get('/')
def home(request: Request):
    content = 'Home FastAPI'
    if request.url.startswith('https://'):
        content += ' SSL'

    return content
