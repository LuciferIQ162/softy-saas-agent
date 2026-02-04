from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from app.utils.prompts import CLASSIFICATION_PROMPT
from app.schemas import EmailClassification
import json
import re

llm = ChatOllama(
    model="mistral",
    temperature=0)

def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in THE LLM RESPONSE")

    return match.group()


def classify_email(subject: str, body: str) -> EmailClassification:
    prompt = PromptTemplate.from_template(CLASSIFICATION_PROMPT)
    response = llm.invoke(prompt.format(subject=subject, body=body))

    json_text = extract_json(response.content)
    result = EmailClassification.model_validate_json(json_text)
    
    result.intent = result.intent.lower()

    return result