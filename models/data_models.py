class PlayerData():
    id: int
    login: str
    password: str
    token: str
    score: int

class PlayerPassword():
    def __init__(self, id: int, password: str):
       self.id = id 
       self.password = password