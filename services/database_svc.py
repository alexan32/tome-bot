import json
from . import cache_svc
from config.config import UPDATE_FLAG


with open("../character2.json") as f:
    mockData = json.load(f)

def fetchCharacter(participant, guildId):
    cache_svc.storeCharacter(participant, guildId, mockData)
    return mockData

def updateCharacter(chararacterData):
    with open("../character2.json", "w") as f:
        f.write(json.dumps(chararacterData))