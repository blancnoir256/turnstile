from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.post("/api/turnstile")
def read_root():
    return {"Hello": "World"}
