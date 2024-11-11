from fastapi import FastAPI, status, HTTPException, Depends
from models.api_data_models import Authentication, TokenInfo
from error_responses import ErrorResponse
from auth import create_token_for_player

app = FastAPI(
    title="Clicker-Backend"
)

@app.post(path = "/auth",
    response_model = TokenInfo,
    status_code = status.HTTP_200_OK,
    responses = ErrorResponse.HTTP_401_INVALID_LOGIN_OR_PASSWORD
)
async def auth(auth: Authentication):
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