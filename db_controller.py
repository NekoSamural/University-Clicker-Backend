import sqlite3
from configs import DATA_BASE_CONFIG

def ExecuteQuery(query: str):
    connection = sqlite3.connect(DATA_BASE_CONFIG.path)
    cursor = connection.cursor()
    
    cursor.execute(query)
    result = cursor.fetchall()
    connection.commit()
    connection.close()

    return result