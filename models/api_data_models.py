from pydantic import BaseModel

class Authentication(BaseModel):
    login : str
    password : str

class TokenInfo(BaseModel):
    access_token: str
    token_type: str