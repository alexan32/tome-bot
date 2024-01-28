from tinydb import TinyDB, Query
import os
import time
import json
from config.config import CACHE_SIZE, LOGGER

Row = Query()
logger = LOGGER

def sizeOfDictionaryInBytes(data:dict):
    return len(json.dumps(data).encode('utf-8'))

class CacheHandler:

    def __init__(self, documentName:str, maxTableSize:int, maximumRowSizeInBytes:int) -> None:
        self.documentPath = os.path.join(os.path.dirname(__file__), documentName)
        self.maxTableSize = maxTableSize
        self.maximumRowSize = maximumRowSizeInBytes

        self.Table = TinyDB(self.documentPath)

    def sizeInBytes(self):
        fileStats = os.stat(self.documentPath)
        return fileStats.st_size
    
    def store(self, data:dict, idKey:str):
        copy = dict(data)
        copy["cache_ts"] = time.time()

        sizeOfRow = sizeOfDictionaryInBytes(copy)
        if sizeOfRow > self.maximumRowSize:
            raise Exception(f"Row of size {sizeOfRow} too large for cache. Maximum row size: {self.maximumRowSize}")

        self.makeRoom(sizeOfRow)

        self.Table.upsert(copy, (Row[idKey] == data[idKey]))

        logger.debug(f"New size of {self.documentPath}: {self.sizeInBytes()}")

    def makeRoom(self, bytesNeeded:int):
        rows = sorted(self.Table.all(), key=lambda row: row["cache_ts"])
        sizeOfTable = self.sizeInBytes()
        logger.debug(f"Attempting to cache a row of size {bytesNeeded} bytes. Size of table: {sizeOfTable}/{self.maxTableSize} bytes.")

        while self.maxTableSize < sizeOfTable + bytesNeeded:
            self.Table.remove(Row.cache_ts == rows.pop(0)["cache_ts"])
            logger.debug(f"Removed a row from {self.documentPath} to make room.")
            sizeOfTable = self.sizeInBytes()

    def fetch(self, id:str, idKey:str):
        data = self.Table.get(Row[idKey] == id)
        
        if data:
            del data["cache_ts"]        # remove meta
            self.store(data, idKey)     # storing data will reset the timestamp, moving data back to bottom of the deletion queue

        return data
    

characterCache = CacheHandler("character-cache.json", CACHE_SIZE, CACHE_SIZE/4)
gameCache = CacheHandler("game-cache.json", CACHE_SIZE, CACHE_SIZE/4)

def storeCharacter(participant, guildId, characterData:dict):
    compositeKey = f"{guildId}-{participant}"
    characterData["compositeKey"] = compositeKey
    characterCache.store(characterData, "compositeKey")

def fetchCharacter(participant, guildId):
    compositeKey = f"{guildId}-{participant}"
    characterData = characterCache.fetch(compositeKey, "compositeKey")
    if characterData:
        del characterData["compositeKey"]
    return characterData