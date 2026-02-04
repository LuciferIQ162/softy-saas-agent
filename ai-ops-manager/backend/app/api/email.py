from fastapi import APIRouter
from app.schemas import EmailInput
from app.agents.classifier import classify_email
from app.agents.decision import decide_action
from app.rag.retriever import retrieve_context

router = APIRouter()

@router.post("/process")
def process_email(email: EmailInput):
    classification = classify_email(email.subject , email.body)
    context = retrieve_context(f"{email.subject}\n{email.body}")
    action = decide_action(classification.intent)
    
    return {
        "classification" : classification,
        "action" : action,
        "context_used": {
            "found": bool(context),
            "text": context[:500] if context else "",
        },
    }