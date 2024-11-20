import jwt
import db_controller
from configs import AUTH_JWT_CONFIG
from datetime import datetime
from models.api_data_models import AuthModel, TokenModel
import bcrypt

def create_token_for_player(data: AuthModel) -> TokenModel | None:
    player_data = db_controller.get_player_autch_data_by_login(data.login)

    if player_data == None:
        return None

    if bcrypt.checkpw(data.password.encode(), player_data.password.encode()) != True:
        return None
    
    new_token = generate_token(
        id = player_data.id,
        login = player_data.login,
        private_key = AUTH_JWT_CONFIG.private_key_path,
        algorithm = AUTH_JWT_CONFIG.algorithm
    )
    
    if db_controller.update_player_token(player_data.id, new_token) == False:
        return None
    
    return TokenModel( access_token = new_token, token_type = "Bearer") 

def generate_token(id : str, login: str, private_key: str, algorithm: str) -> str:
    now = datetime.utcnow()

    jwt_payload = {
        "id" : id,
        "login" : login,
        "iat" : now
    }

    return jwt.encode(jwt_payload, private_key, algorithm)