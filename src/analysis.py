import os

from json import load
from pathlib import Path

def main() -> None:    
    dict = first_analysis()
    user_choices(dict)
    # monster_choices(dict)

def first_analysis() -> None:
    os.chdir("./..")
    f = open("./data/getRtpvpReplayList.json")
    initial_dict = load(f)
    return initial_dict 

def user_choices(initial_dict: dict) -> None:
    user_dict = {}
    for each in initial_dict["replay_list"]:
        print(each["wizard_name"])
        name = each["wizard_name"]
        if not (name in user_dict.keys()): 
            # if initial_dict[each["wizard_name"]] does not exist: initiate
            user_dict[name] = initiate_user_entry(each)
            print("first for %s" % name)
        else:
            # else add to it
            user_dict[name] = add_to_user_entry(each, name, user_dict[name])
            print("update for %s" % name)
    print(user_dict)
    return

def initiate_user_entry(each: dict) -> dict:
    is_draw = False
    if (each["win_lose"] < 1) | (each["win_lose"] > 2):
        each["win_lose"] = 2
        is_draw = True
    lost = each["win_lose"] - 1
    new_dict = {}
    new_dict["rank"] = each["rank"]
    new_dict["server_id"] = each["server_id"]
    new_dict["country"] = each["country"]
    new_dict["wizard_name"] = each["wizard_name"]
    new_dict["rtpvp_score"] = each["rtpvp_score"]
    new_dict["win_count"] = int(not bool(lost))
    new_dict["lose_count"] = lost - int(is_draw)
    new_dict["draw_count"] = 0 + int(is_draw)
    new_dict["total_matches"] = 1
    new_dict["win_percent"] = new_dict["win_count"]/new_dict["total_matches"]
    return new_dict

def add_to_user_entry(each: dict, name: str, user_dict: dict) -> dict:
    is_draw = False
    if (each["win_lose"] < 1) | (each["win_lose"] > 2):
        each["win_lose"] = 2
        is_draw = True
    lost = each["win_lose"] - 1
    new_dict = {}
    new_dict["rank"] = each["rank"]
    new_dict["server_id"] = user_dict["server_id"]
    new_dict["country"] = user_dict["country"]
    new_dict["wizard_name"] = user_dict["wizard_name"]
    new_dict["rtpvp_score"] = each["rtpvp_score"]
    new_dict["win_count"] = user_dict["win_count"] + int(not bool(lost))
    new_dict["lose_count"] = user_dict["lose_count"] + lost - int(is_draw)
    new_dict["draw_count"] = user_dict["draw_count"] + int(is_draw)
    new_dict["total_matches"] = user_dict["total_matches"] + 1
    new_dict["win_percent"] = new_dict["win_count"]/new_dict["total_matches"]
    return new_dict

if __name__ == "__main__":
    main()