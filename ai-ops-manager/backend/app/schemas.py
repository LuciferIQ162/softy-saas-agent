from pydantic import BaseModel

class EmailInput(BaseModel):
    subject : str
    body : str
    sender : str

class EmailClassification(BaseModel):
    intent : str
    priority : str
    confidence : float

class DecisionOutput(BaseModel):
    action : str
    notes : str
