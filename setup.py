import json # to create settings.json and maps.json
import os # for filesystem

def main():
    print("Welcome to the Beat Saber Beatmap Downgrader Auto-downgrade setup wizard!")
    print("Your Beat Saber install directory is needed. You can find that folder when you right click on Beat Saber in Steam, then on 'Properties' and 'installed Files'. After that click on 'Browse' and your file explorer will open.")
    while True:
        directory: str = input("Beat Saber install directory: ")
        try:
            files: list[str] = os.listdir(directory)
            if not "Beat Saber.exe" in files: raise Exception("")
            break
        except:
            print("Something went wrong. Is that the right directory?")
    while True:
        decision: str = input("Do you want to try converting all your maps now? (Y/n): ")
        if (decision == "Y"):
            convert_all = True
            break
        if (decision == "n"):
            convert_all = False
            break
    
    # for cross platform
    while "\\" in directory: directory = directory.replace("\\", "/")
    if directory[-1] == "/": directory = directory[:-1]

    # make settings.json
    custom_levels_dir: str = directory + "/Beat Saber_Data/CustomLevels"
    with open("settings.json", "w") as file:
        json.dump({ "customLevelsDir": custom_levels_dir})
    
    # the maps json that keeps track of already converted maps
    with open(custom_levels_dir + "/" + "maps.json", "w") as file:
        if convert_all:
            json.dump([], file)
        else:
            maps = []
            content = os.listdir(custom_levels_dir)
            for file in content:
                if file[0:4] != "(DG)": maps.append(file)
            json.dump(maps, file)
    
    # run auto_downgrader if user wants to downgrade all now
    if convert_all: os.system("python auto_downgrader.py")

    print("Setup done! You can now run auto_downgrader.py anytime you added a new song that needs to be converted.")


if __name__ == "__main__":
    main()