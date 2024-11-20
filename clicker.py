import db_controller
from datetime import datetime
from configs import CLICK_REQUEST_TIME
import enum

class ClickResultCodes(enum.Enum):
    success = 0
    invalid_token = 1
    too_many_request = 2

def click(token: str) -> ClickResultCodes:
    player_info = db_controller.get_player_data_by_token(token)

    if player_info == None:
        return ClickResultCodes.invalid_token
    
    if player_info.prewUpdateTime != None:

        current_unix_time = datetime.now().timestamp()

        if current_unix_time - player_info.prewUpdateTime <= CLICK_REQUEST_TIME:
            return ClickResultCodes.too_many_request
        
    new_score = player_info.score + 1
    if db_controller.update_player_score(player_info.id, new_score) == False:
        return ClickResultCodes.invalid_token
    
    return ClickResultCodes.success