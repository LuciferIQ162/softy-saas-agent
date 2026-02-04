from fastapi import FastAPI

import app.config  # load .env before any OpenAI-using code

from app.api.email import router as email_router

app = FastAPI(title="AI Ops Manager")

app.include_router(email_router, prefix="/email")

@app.get("/")
def health():
    return {"status": "ok"}