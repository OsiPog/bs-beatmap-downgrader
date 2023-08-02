import json # to read and write json files (duh)
import os # for filesystem and commands
import shutil # for folder deletion

def main():
    with open("settings.json", "r") as file:
        settings: dict = json.load(file)
    
    # check custom levels dir for new maps
    with open(settings["customLevelsDir"] + "/maps.json", "r") as file:
        checked_maps: list[str] = json.load(file)

    file_names: str = os.listdir(settings["customLevelsDir"])
    for file_name in file_names:
        if file_name == "maps.json": continue
        if file_name[:4] == "(DG)": continue 
        if not (file_name in checked_maps):
            os.system(f"python downgrader.py '{settings['customLevelsDir']}/{file_name}'")
            checked_maps.append(file_name)

    # go through checked_maps to see if it contains anything thats not in the folder anymore 
    for checked_map in checked_maps.copy():
        if not (checked_map in file_names): checked_maps.remove(checked_map)

    # save the maps.json again now that it got changed
    with open(settings["customLevelsDir"] + "/maps.json", "w") as file:
        json.dump(checked_maps, file)

if __name__ == "__main__":
    main()