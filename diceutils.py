from d20 import roll
import re
from objects.character import Character
from config.config import DICE_OPERATORS, VARIABLE, MAX_DEPTH, LOGGER

logger = LOGGER


# returns a set containing the following:
# key - either string or None. returns the string if the input matches a saved value in the character data, otherwise None
# total - string representing the total of the dice roll
# roll - the string representing the final dice expression including the total
def evaluate(rollString:str, character:Character, depth:int=0, logging=False) -> set:
    rollString = rollString.strip()
    key = None
    _print = lambda content : logger.debug("".ljust(depth, "\t") + content) if logging else None

    # if rollstring is a variable, we want to set it to its saved value for display purposes.
    if depth == 0 and re.fullmatch(r"\b" + VARIABLE + r"\b", rollString):
        _print(f"depth level 0 '{rollString}' is a variable!")
        key = rollString
        rollString = character.findRoll(rollString)
        _print(f"found match for {rollString}: '{rollString}'")
        if not rollString:
            raise Exception(f'No data found for "{rollString}"')

    # find all variables, and make sure to ignore operations like "kh1", "kl2", etc
    matches = re.findall(VARIABLE, rollString)
    matches = [x for x in matches if not re.fullmatch(DICE_OPERATORS, x)]
    _print(f"rollString: '{rollString}'. matches: {matches}")

    # perform string replacements
    misses = []
    for match in matches:
        replaceValue = character.findRoll(match)
        if replaceValue:
            if not replaceValue.isdigit():
                if depth == MAX_DEPTH:
                    raise Exception(f"'evaluate' function maximum depth ({MAX_DEPTH}) reached! Failed to replace '{replaceValue}'.")
                _print(f"RECURSIVE CALL! '{match}' ==> '{replaceValue}'?")
                _, replaceValue, _ = evaluate(replaceValue, character, depth=depth+1, logging=logging)
                _print(f"DONE! '{match}' ==> '{replaceValue}'")
            exact = r"\b(" + match + r")\b" # make sure you are not matching on a portion of another var. ie 'dex' in 'dexterity'
            _print(f"performing replacement on {exact}")
            rollString = re.sub(exact, replaceValue, rollString)
        else:
            _print(f"no variable for {match}")
            misses.append(match)
    
    if len(misses) > 0:
        raise Exception(f"Failed to perform variable replacement for the following: {misses}")
    
    # roll result, return values
    result = roll(rollString)
    return key, str(result.total), str(result)