import sqlite3
from configs import DATA_BASE_CONFIG
from models.data_models import PlayerData, PlayerPassword

def get_player_data_by_login(login:str) -> PlayerPassword | None:
    connection = sqlite3.connect(DATA_BASE_CONFIG.path)
    cursor = connection.cursor()

    cursor.execute(
        f"SELECT id, password FROM Players WHERE login = '{login}' LIMIT 1"
    )
    result = cursor.fetchall()

    connection.close()

    if len(result) == 0:
        return None
    
    id = result[0][0]
    password = result[0][1]

    return PlayerPassword(id, password)

def update_player_token(id:int, token:str) -> bool:
    connection = sqlite3.connect(DATA_BASE_CONFIG.path)
    cursor = connection.cursor()

    cursor.execute(
        f"SELECT count(id)>0 FROM Players WHERE id = '{id}'"
    )
    result = cursor.fetchall()[0][0]
    if result == False:
        connection.close()
        return False
    
    cursor.execute(
        f"UPDATE Players SET token = '{token}' WHERE id = '{id}'"
    )
    connection.commit()
    connection.close()

    return True