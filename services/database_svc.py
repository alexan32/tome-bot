import json
import requests
from . import cache_svc
from config.config import ENVIRONMENT, LOGGER

logger = LOGGER


def fetchCharacter(participant, guildId):
    mockData = {} #@## TODO
    cache_svc.storeCharacter(participant, guildId, mockData)
    return mockData

def updateCharacter(chararacterData:dict):
    logger.info("performing character update")
    status = 200
    message = "ok"
    
    url = ENVIRONMENT["characterServiceEndpoint"]
    response = requests.put(url, json=chararacterData)
    logger.debug(f"PUT Response from character service: {response.status_code}")

    status = response.status_code
    if status != 200:
        logger.error(response.text)
        message = "Failed to update character data. Please try again later"
    return status, message


def fetchGameData(guildId):
    pass

def updateGameData(guildId, gameData:dict):
    pass