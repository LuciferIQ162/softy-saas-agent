from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from app.prompts import SALES_AGENT_PROMPT
from app.rag.retriever import get_sales_context
import json, re


llm = ChatOllama(model="mistral", temperature = 0)

def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No json found in LLM response")
    return json.loads(match.group())

def qualify_lead(lead: dict):
    query = f"""
    company : {lead['company']}
    company_size : {lead['company_size']}
    message : {lead['message']}
    """
    context = get_sales_context(lead["message"])
    enriched_lead = {
        **lead,
        "context": context,
    }
    # context = get_sales_context(lead["message"])
    # print("RAG CONTEXT:", context)

    
    prompt = PromptTemplate.from_template(template=SALES_AGENT_PROMPT)
    response = llm.invoke(prompt.format(lead=enriched_lead))
    result =  extract_json(response.content)
    result["context_used"] = context
    return result


     
        
    