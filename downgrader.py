import json # for parsing the difficulty.dat files
import os # get files
import sys # for cli arguments
import shutil # for duplicating folder

def downgrade(beatmap: dict):
    # if "_songName" is a key the file being edited is the info.dat, for the map metadata
    # Add "(downgraded)" to the song name that it can be recognized ingame
    if "_songName" in beatmap:
        beatmap["_songName"] += " (downgraded)"
        return beatmap

    if not ("version" in beatmap): return
    v2_map: dict = {
        "_version": "2.0.0",
        "_notes": [],
        "_obstacles": [],
        "_events": [],
    }

    # notes and bombs are in two different arrays but are in one in the old format
    if "colorNotes" in beatmap:
        for note in beatmap["colorNotes"]:
            v2_map["_notes"].append({
                "_time": note["b"],
                "_lineIndex": note["x"],
                "_lineLayer": note["y"],
                "_type": note["c"],
                "_cutDirection": note["d"],
            })
    if "bombNotes" in beatmap:
        for bomb in beatmap["bombNotes"]:
            v2_map["_notes"].append({
                "_time": bomb["b"],
                "_lineIndex": bomb["x"],
                "_lineLayer": bomb["y"],
                "_type": 3,
            })
    
    # Walls
    if "obstacles" in beatmap:
        for wall in beatmap["obstacles"]:
            # the old version cannot handle such a wall, converting that would result in a possibly
            # unavoidable obstacle
            if wall["y"] < 2 and wall["h"] < 2: continue

            v2_map["_obstacles"].append({
                "_time": wall["b"],
                "_lineIndex": wall["x"],
                "_type": round(wall["y"]*0.5), # maps [0, 1, 2] to [0, 1, 1]
                "_duration": wall["d"],
                "_width": wall["w"],
            })

    # basic beatmap events
    if beatmap["basicBeatmapEvents"]:
        for event in beatmap["basicBeatmapEvents"]:
            v2_map["_events"].append({
                "_time": event["b"],
                "_type": event["et"],
                "_value": event["i"],
            })

    return v2_map


def main():
    if len(sys.argv) != 2:
        print("Usage: downgrader <absolute beatmap folder path>")
        exit()

    beatmap_folder_path: str = sys.argv[1]
    while "\\" in beatmap_folder_path: beatmap_folder_path = beatmap_folder_path.replace("\\", "/")

    if beatmap_folder_path[-1] == "/": beatmap_folder_path = beatmap_folder_path[:-1]
    
    parent_folder: str = "/".join(beatmap_folder_path.split("/")[:-1])
    folder_name: str = beatmap_folder_path.split("/")[-1]
    new_folder: str = parent_folder + "/" + "(DG) " + folder_name
    shutil.copytree(beatmap_folder_path, new_folder, dirs_exist_ok=True)

    file_names: list[str] = os.listdir(beatmap_folder_path)

    print("Downgrading difficulties..")
    for file_name in file_names:
        if file_name.split(".")[-1] == "dat":
            downgraded: dict = {}
            with open(new_folder + "/" + file_name, "r") as file:
                downgraded = downgrade(json.load(file))
                if not downgraded: 
                    print("Couldn't downgrade " + file_name + " (maybe its already on V2?)")
                    print("Stopping downgrading..")
                    shutil.rmtree(new_folder)
                    break

            with open(new_folder + "/" + file_name, "w") as file:
                json.dump(downgraded, file)
            
            print("Downgraded " + file_name + "!")



if __name__ == "__main__":
    main()

