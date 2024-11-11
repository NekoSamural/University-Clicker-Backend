import sqlite3
from configs import DATA_BASE_CONFIG
from models.data_models import PlayerData, PlayerPassword

def execute_query(query: str) -> list[any]:
    connection = sqlite3.connect(DATA_BASE_CONFIG.path)
    cursor = connection.cursor()
    
    cursor.execute(query)
    result = cursor.fetchall()
    connection.commit()
    connection.close()

    return result

def get_player_data_by_login(login:str) -> PlayerPassword | None:
    data = execute_query(
        f"SELECT id, password FROM Players WHERE login = '{login}' LIMIT 1"
    )

    if len(data) == 0:
        return None
    
    id = data[0][0]
    password = data[0][1]

    return PlayerPassword(id, password)