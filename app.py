from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.api_data_models import AuthModel, TokenModel, StatusModel, ScoreResponseModel, TopPlayerModel
from error_responses import ErrorResponse
from auth import create_token_for_player
import clicker
import db_controller

app = FastAPI(
    title="Бекенд кликера",
    version="1.0"
)

http_bearer = HTTPBearer()

#-------------------- Регистрация
@app.post(path = "/registration",
    response_model = StatusModel,
    status_code = status.HTTP_200_OK,
    responses = ErrorResponse.HTTP_401_INVALID_LOGIN,
    description="Запрос на регистрацию нового пользователя.",
    name="Регистрация"
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

#-------------------- Аутентификация
@app.post(path = "/auth",
    response_model = TokenModel,
    status_code = status.HTTP_200_OK,
    responses = ErrorResponse.HTTP_401_INVALID_LOGIN_OR_PASSWORD,
    description="Запрос на получение токена.",
    name="Аутентификация"
)
async def auth(auth: AuthModel):
    token = create_token_for_player(auth)

    if token == None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid login or password"
        )
    return token

#-------------------- Клик
@app.put(path = "/click",
    response_model = StatusModel,
    status_code = status.HTTP_200_OK,
    responses = ErrorResponse.HTTP_401_UNAUTHORIZED | ErrorResponse.HTTP_429_TOO_MANY_REQUESTS,
    description="Запрос на клик. Есть ограничение на 5 кликов в секунду.",
    name="Запрос на клик"
)
async def click(token: HTTPAuthorizationCredentials = Depends(http_bearer)):

    click_result = clicker.click(token.credentials)

    if click_result == clicker.ClickResultCodes.invalid_token:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid token"
        )
    
    elif click_result == clicker.ClickResultCodes.too_many_request:
        raise HTTPException(
            status_code = status.HTTP_429_TOO_MANY_REQUESTS,
            detail = "Too Many Requests"
        )
    
    return StatusModel(status=True)

#-------------------- Получение счёта
@app.get(path = "/get-player-score/{id}",
    response_model = ScoreResponseModel,
    status_code = status.HTTP_200_OK,
    responses = ErrorResponse.HTTP_404_NOT_FOUND_ID,
    description="Запрос на получение очков игрока по id.",
    name="Получение Score игрока по id"
)
async def get_player_score(id: int):
    palyer_score = db_controller.get_player_score_by_id(id)

    if palyer_score == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Id not found"
        )
    return ScoreResponseModel(score = palyer_score)

#-------------------- Получение топ 5 игроков
@app.get(path = "/get-top-players",
    response_model = list[TopPlayerModel] | None,
    status_code = status.HTTP_200_OK,
    description="Запрос на получение топ 5 игроков",
    name="Получение топ 5 игроков"
)
async def get_top_players_func():
    return db_controller.get_top_players()

#команда для запуска
#uvicorn app:app --host 0.0.0.0 --port 7777 --reload

#Документация
#http://127.1.1.1:7777/docs
#http://127.1.1.1:7777/redoc