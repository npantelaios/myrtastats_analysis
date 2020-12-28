from io import FileIO
import os

from json import load
from pathlib import Path

def main() -> None:
    os.chdir("./..")
    mapping_file = "mapping/mapping.txt"    
    corresp_dict = make_correspondence(mapping_file)
    logs_file = "data/full_log.txt"
    monster_choices(logs_file, corresp_dict)


def monster_choices(file: str, corresp_dict: dict) -> None:
    f = open(file).read()
    split_phrase = "API Command: getRankerRtpvpReplayList"
    print(len(f.split(split_phrase)))
    for each in f.split(split_phrase)[18:]:
        each = each.split("Response:")[1]
        json_each = json.loads(each)
    return

def make_correspondence(file: str) -> dict:
    corresp_dict = {}
    f = open(file).read().splitlines()
    cnt = 0
    for each in f:
        if not each:
            cnt += 1
            continue
        id = each.split(":")[0]
        monster = each.split(":")[1].translate({ord(i): None for i in ', \''})
        corresp_dict[monster] = id
    return corresp_dict

def monster_matcher(corresp_dict: dict, id: int) -> str:
    res = next((key for key in corresp_dict if corresp_dict[key] == id), None) 
    return res

if __name__ == "__main__":
    main()