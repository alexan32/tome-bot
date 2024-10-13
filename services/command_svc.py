from .cmd_handler import execute
from . import cache_svc
from . import database_svc
from config.config import UPDATE_FLAG
import json

def counter(participant, guildId, _input:str):
    characterData = getCharacterData(participant, guildId)
    messages = execute(_input, characterData)
    updateCharacter(participant, guildId, characterData)
    return messages

def composite(participant, guildId, _input:str):
    characterData = getCharacterData(participant, guildId)
    messages = execute(_input, characterData)
    updateCharacter(participant, guildId, characterData)
    return messages

def func(participant,  guildId, _input:str):
    characterData = getCharacterData(participant, guildId)
    messages = execute(_input, characterData)
    updateCharacter(participant, guildId, characterData)
    return messages

def roll(participant, guildId, _input:str):
    characterData = getCharacterData(participant, guildId)
    messages = execute(_input, characterData)
    updateCharacter(participant, guildId, characterData)
    return messages

def getCharacterData(participant, guildId):
    characterData = cache_svc.fetchCharacter(participant, guildId)
    if not characterData:
        characterData = database_svc.fetchCharacter(participant, guildId)
    return characterData

# temporary command to get the game going
def quickPlay(participant, guildId, first, last):
    import os
    file_path = f"{os.path.dirname(os.path.realpath(__file__))}/../character2.json"
    print(file_path)
    with open(file_path) as f:
        characterData = json.load(f)
    characterData["characterId"] = str(participant)
    characterData["participant"] = str(participant)
    characterData["meta"]["first"] = first
    characterData["meta"]["last"] = last
    characterData[UPDATE_FLAG] = True
    updateCharacter(participant, guildId, characterData)

    return []

def updateCharacter(participant, guildId, characterData:dict):
    if characterData.get(UPDATE_FLAG, False):
        del characterData[UPDATE_FLAG]
        cache_svc.storeCharacter(participant, guildId, characterData)
        status, message =database_svc.updateCharacter(characterData)
        return status, [message]
    return 200, []

if __name__ == "__main__":
    print(execute("roll 1d20 + 7", {}))