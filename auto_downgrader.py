import json # to read and write json files (duh)
import os # for filesystem and commands

def main():
    with open("settings.json", "r") as file:
        settings: dict = json.load(file)
    
    # check custom levels dir for new maps
    with open(settings["customLevelsDir"] + "/maps.json", "r") as file:
        checked_maps: list[str] = json.load(file)

    for file_name in os.listdir(settings["customLevelsDir"]):
        if file_name == "maps.json": continue
        if file_name[:4] == "(DG)": continue 
        if not (file_name in checked_maps):
            os.system(f"python downgrader.py '{settings['customLevelsDir']}/{file_name}'")
            # checked_maps.append(file_name)
    
    # save the maps.json again now that it got changed
    with open(settings["customLevelsDir"] + "/maps.json", "w") as file:
        json.dump(checked_maps, file)

if __name__ == "__main__":
    main()