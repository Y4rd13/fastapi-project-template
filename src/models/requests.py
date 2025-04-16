from pydantic import BaseModel

# Replace the following with your actual request model that will be used in routes
# This is a placeholder for the actual request model
class RequestTemplate(BaseModel):
    id: str
    name: str
    description: str
    method: str
    url: str
    headers: dict
    params: dict
    body: dict

class ResponseTemplate(BaseModel):
    status_code: int
    headers: dict
    body: dict