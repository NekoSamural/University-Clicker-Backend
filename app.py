from fastapi import FastAPI, status, HTTPException, Depends
from models.api_data_models import AuthModel, TokenModel, StatusModel
from error_responses import ErrorResponse
from auth import create_token_for_player
import db_controller

app = FastAPI(
    title="Clicker-Backend"
)

@app.post(path = "/registration",
    response_model = StatusModel,
    status_code = status.HTTP_200_OK,
    responses = ErrorResponse.HTTP_401_INVALID_LOGIN
)
async def registration(reg_data: AuthModel):
    if db_controller.checking_login_for_uniqueness(reg_data.login) == False:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid login"
        )
    
    db_controller.create_new_player(reg_data.login, reg_data.password)
    create_token_for_player(reg_data)

    return StatusModel(status=True)

@app.post(path = "/auth",
    response_model = TokenModel,
    status_code = status.HTTP_200_OK,
    responses = ErrorResponse.HTTP_401_INVALID_LOGIN_OR_PASSWORD
)
async def auth(auth: AuthModel):
    token = create_token_for_player(auth)

    if token == None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid login or password"
        )
    return token

#команда для запуска
#uvicorn app:app --host 0.0.0.0 --port 7777 --reload

#Документация
#http://127.1.1.1:7777/docs