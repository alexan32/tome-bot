from d20 import roll
import re

# converts a dictionary that represents a roll into a roll string
def processCompositeRollDict(rollDict: dict) -> str:
    keys = rollDict.keys()
    values = map(lambda key : rollDict[key], keys)
    values = [x for x in values if x not in ["", "0", 0, None]]
    return " + ".join(values).lower()


# processes a dice string and performs variable replacement
# much easier to process dice roll before performing roll instead of modifying d20 module. I tried :')
def replaceVariables(rollString: str, variables:dict = {}) -> str:
    regex = r"([a-ce-z][a-z]*|d[a-z]+)"
    matches = re.findall(regex, rollString)
    depth = 0

    while len(matches) > 0:
        print(f"matches in this pass: {matches}")
        for match in matches:
            if match in variables:

                replaceValue = variables[match]
                if type(replaceValue) == "dict":
                    replaceValue = processCompositeRollDict(replaceValue)

                exact = r"\b(" + match + r")\b" # make sure you are not matching on a portion of another var. ie 'dex' in 'dexterity'
                print(f"performing replacement on {exact}")
                rollString = re.sub(exact, replaceValue, rollString)
            else:
                print(f"no variable for {match}")

        print(f"updated rollstring: {rollString}")

        matches = re.findall(regex, rollString)
        depth += 1
        if len(matches) > 0 and depth == 10:
            print("maximum depth hit!")
            raise Exception(f"Hit maximum depth limit while attempting variable replacement. variables: {matches}")

    return rollString.lower()


# creates/updates variables using the values in the formulas dict
def runFormulas(variables:dict, formulas:dict) -> dict:
    keys = formulas.keys()
    for key in keys:
        try:
            rollString = replaceVariables(formulas[key], variables)
            result = str(roll(rollString).total)
            variables[key] = result
        except Exception as e:
            print(f"failed to run formuala '{key}'. Error: {e}")
            variables[key] = f"ERROR! {e}"
    return variables


# creates/updates variables using the values in the composite rolls dict
def runCompositeRolls(variables:dict, compositeRolls:dict) -> dict:
    keys = compositeRolls.keys()
    for key in keys:
        try:
            rollString = processCompositeRollDict(compositeRolls[key])
            variables[key] = rollString
        except Exception as e:
            print(f"failed to build from composite roll '{key}'. Error: {e}")
            variables[key] = f"ERROR! {e}"
    return variables


variables = {
    "level": "4",
    "strength": "8",
    "dexterity": "14",
    "constitution": "12",
    "wisdom": "12",
    "charisma": "17",
    "intelligence": "10",
}

formulas = {
    "str": "(strength - 10) / 2",
    "dex": "(dexterity - 10) / 2",
    "con": "(constitution - 10) / 2",
    "wis": "(wisdom - 10) / 2",
    "int": "(intelligence - 10) / 2",
    "cha": "(charisma - 10) / 2",
    "prof": "proficiencybonus",
    "proficiencybonus": "((level - 1) / 4) + 2",
    "proficient": "proficiencybonus",
    "expert": "proficiencybonus * 2",
}

compositeRolls = {
    "dexteritysave": {
        "base": "1d20",
        "modifier": "dex",
        "proficiency": "proficient",
        "bonus": "2"
    },
    "dexteritycheck": {
        "base": "1d20",
        "modifier": "dex",
        "proficiency": "",
        "bonus": ""
    }
}

if __name__ == "__main__":
    import json
    runFormulas(variables, formulas)
    runCompositeRolls(variables, compositeRolls)
    print(json.dumps(variables, indent=4))