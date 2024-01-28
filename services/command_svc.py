from .cmd_handler import execute
from . import cache_svc
from . import database_svc
from config.config import UPDATE_FLAG

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

def func(participant, guildId, _input:str):
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


def updateCharacter(participant, guildId, characterData:dict):
    if characterData.get(UPDATE_FLAG, False):
        del characterData[UPDATE_FLAG]
        cache_svc.storeCharacter(participant, guildId, characterData)
        database_svc.updateCharacter(characterData)

if __name__ == "__main__":
    print(execute("roll 1d20 + 7", {}))