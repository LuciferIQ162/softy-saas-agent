from pydantic import BaseModel

class LeadInput(BaseModel):
    name : str
    email : str
    company : str
    company_size : int
    message : str