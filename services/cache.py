from tinydb import TinyDB, Query
import os

script_dir = os.path.dirname(__file__)
characterCache = TinyDB(os.path.join(script_dir, 'cache/characters.json'))