import sqlite3
from configs import DATA_BASE_CONFIG
from models.data_models import PlayerData, PlayerPassword
from models.api_data_models import TopPlayerModel
import bcrypt
from datetime import datetime

def get(query: str) -> any:
    connection = sqlite3.connect(DATA_BASE_CONFIG.path)
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    return result

def update(query: str):
    connection = sqlite3.connect(DATA_BASE_CONFIG.path)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

def checking_login_for_uniqueness(login: str) -> bool:
    result = get(f"SELECT count(login)>0 FROM Players WHERE login = '{login}'")[0][0]
    return result != True

def create_new_player(login: str, password: str):
    hashPassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    update(f"INSERT INTO Players (login, password, score) VALUES ('{login}', '{hashPassword.decode()}', 0)")

def get_player_password_by_login(login:str) -> PlayerPassword | None:
    result = get(f"SELECT id, password FROM Players WHERE login = '{login}' LIMIT 1")

    if len(result) == 0:
        return None
    
    id = result[0][0]
    password = result[0][1]
    return PlayerPassword(id, password)

def update_player_token(id:int, token:str) -> bool:
    if get(f"SELECT count(id)>0 FROM Players WHERE id = '{id}'")[0][0] != True:
        return False
    
    update(f"UPDATE Players SET token = '{token}' WHERE id = '{id}'")
    return True

def get_player_data_by_token(token:str) -> PlayerData | None:
    if get(f"SELECT count(id)>0 FROM Players WHERE token = '{token}'")[0][0] != True:
        return None
    
    result = get(f"SELECT id, login, score, prewUpdateTime FROM Players WHERE token = '{token}' LIMIT 1")
    if len(result) == 0:
        return None
    
    id = result[0][0]
    login = result[0][1]
    score = result[0][2]
    prewUpdateTime = result[0][3]

    return PlayerData(id, login, score, prewUpdateTime)

def update_player_score(id:int, score:int) -> bool:
    if get(f"SELECT count(id)>0 FROM Players WHERE id = '{id}'")[0][0] != True:
        return False

    current_unix_time = datetime.now().timestamp()
    update(f"UPDATE Players SET score = '{score}', prewUpdateTime = '{current_unix_time}' WHERE id = '{id}'")
    return True

def get_player_score_by_id(id:int) -> int | None:
    if get(f"SELECT count(id)>0 FROM Players WHERE id = '{id}'")[0][0] != True:
        return None
    
    result = get(f"SELECT score FROM Players WHERE id = '{id}' LIMIT 1")
    if len(result) == 0:
        return None
    
    return result[0][0]

def get_top_players() -> list[TopPlayerModel] | None:
    result = get(f"SELECT login, score FROM players ORDER BY score DESC LIMIT 5")

    if len(result) == 0:
        return None
    
    players = list()
    for player in result:
        players.append(TopPlayerModel(name = player[0], score = player[1]))
    
    return players