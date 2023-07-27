from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def greetings():
    return {
        "name": "Verdete",
        "description": "Network monitoring and managing software",
        "author": "Matteus Maximo Felisberto - matteusmaximof@gmail.com",
        "version": '0.0.1-alpha'
    }
