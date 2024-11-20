class PlayerData():
    def __init__(self, id: int, login: str, score: int, prewUpdateTime: float):
       self.id = id 
       self.login = login
       self.score = score
       self.prewUpdateTime = prewUpdateTime

class PlayerPassword():
    def __init__(self, id: int, password: str):
       self.id = id 
       self.password = password