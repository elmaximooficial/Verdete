from fastapi import FastAPI

app = None


def start():
    global app
    app = FastAPI()
