from fastapi import FastAPI
from app.schemas import LeadInput
from app.agent import qualify_lead

app = FastAPI(title = "AI - Sales - Agent")

@app.post("/sales/qualify")
def qualify(lead: LeadInput):
    return qualify_lead(lead.dict())

@app.get("/")
def health():
    return {"status":"ok"}



