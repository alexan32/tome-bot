import os
import json
import logging
import logging.handlers

INITIALIZED = False     # whether config init has been ran or not
STAGE = None            # dev/test/prd
ENVIRONMENT = None      # dictionary loaded from json file in config folder
HANDLER = None          # logger handler
LOGGER = None           # logger obj
ROLES = ['gm', 'player', 'admin']
DICE_OPERATORS = r"(k|p|rr|ro|ra|e|mi|ma)(l|h)?"
VARIABLE = r"([a-ce-z][a-z_]*|d[a-z_]+)"
MAX_DEPTH = 10
CACHE_SIZE = 100000    # 10 Kb
UPDATE_FLAG = "UPDATE"

def init(stage):
    global STAGE
    global ENVIRONMENT
    global LOGGER
    global HANDLER
    global INITIALIZED

    STAGE = stage

    # LOAD ENVIRONMENT VARIABLES FILE
    script_dir = os.path.dirname(__file__)
    with open(os.path.join(script_dir, f"./{STAGE}.json")) as f:
        ENVIRONMENT = json.load(f)

    # BOT LOGGING
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s]: %(message)s')
    if STAGE == "prd":
        LOGGER = logging.getLogger('discord')
        LOGGER.setLevel(logging.WARN)
        handler = logging.handlers.RotatingFileHandler(
            filename='discord.log', 
            encoding='utf-8', 
            maxBytes=32 * 1024 * 1024,  # 32 MiB
            backupCount=5  # Rotate through 5 files
        )
        handler.setFormatter(formatter)
    
    else:
        LOGGER = logging.Logger('discord')
        LOGGER.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

    HANDLER = handler
    LOGGER.addHandler(HANDLER)
    INITIALIZED = True