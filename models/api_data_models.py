from pydantic import BaseModel

class AuthModel(BaseModel):
    login : str
    password : str

class TokenModel(BaseModel):
    access_token: str
    token_type: str

class StatusModel(BaseModel):
    status: bool