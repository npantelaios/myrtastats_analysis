from io import FileIO
import os
from math import ceil 

from json import loads, dump ,load
from pathlib import Path

MIN_SCORE = 700

monster_dict = {}
none_monsters_dict = {}
corresp_dict = {}
total_battles = 0
total_battles_duplicate = 0
replay_rids = []

def main() -> None:
    os.chdir("./..")
    # load monster-monster_id correspondence 
    mapping_file = "mapping/mapping.txt"    
    make_correspondence(mapping_file)
    # initialize monster_dict with zeros(0)
    # init_monster_dict() # run ONLY the first time
    # load previous monster_dict from /db/data.json
    load_previous()
    # TODO: make input file argument[0] from command 
    # TODO: make output file argument[1] from command
    # CHANGE THIS LINE FOR OTHER FILE PARSE
    # logs_file = "data/full_log.txt"
    logs_file = "data/full_log_6_0_mb.txt"
    monster_choices(logs_file)
    return

def make_correspondence(file: str) -> None:
    global corresp_dict
    corresp_dict = {}
    f = open(file).read().splitlines()
    cnt = 0
    for each in f:
        if not each:
            cnt += 1
            continue
        id = each.split(":")[0]
        monster = each.split(":")[1].translate({ord(i): None for i in ', \'\"'})
        corresp_dict[monster] = id
    return

def init_monster_dict() -> None:
    init_stats = {
                'pick': 0, 
                'pick-perc': 0, 
                'win': 0,
                'win-perc': 0,
                'leader': 0,
                'leader-perc': 0,
                'first': 0,
                'first-perc': 0, 
                'last': 0, 
                'last-perc': 0,
                'banned': 0,
                'banned-perc': 0,
                '1p-win': 0,
                '5p-win': 0,
                '1p-win-perc': 0,
                '5p-win-perc': 0,
                }
    for key in corresp_dict:
        if not key:
            continue
        monster_dict[key] = init_stats.copy()
    return

def load_previous() -> None:
    global monster_dict
    global none_monsters_dict
    global replay_rids
    with open('db/data.json') as f:
        monster_dict = load(f)
    with open('db/not_found.json') as f:
        none_monsters_dict = load(f)
    with open('db/rids.txt') as f:
        rids = f.read().splitlines()
    for rid in rids:
        replay_rids.append(int(rid))
    return

def monster_choices(file: str) -> None:
    global total_battles
    global replay_rids
    f = open(file).read()
    split_phrase = "API Command: getRankerRtpvpReplayList"
    for each in f.split(split_phrase)[18:]:
        each = each.split("Response:")[1]
        each = each.split("API Command:")[0]
        json_each = loads(each)
        for battle in json_each['ranker_replay_list']: 
            rid = battle['replay_rid_ref']
            opp_first_pick = bool(battle['first_slot_id'] - 1)
            if rid not in replay_rids:
                replay_rids.append(rid)
                opp_won_battle = bool(battle['win_lose'] -1)
                if (battle['rtpvp_score'] > MIN_SCORE) & (battle['opp_rtpvp_score'] > MIN_SCORE):
                    total_battles += 1
                    get_picks(battle['pick_info'], (not opp_won_battle), (not opp_first_pick))
                    get_picks(battle['opp_pick_info'], opp_won_battle, opp_first_pick)
            global total_battles_duplicate
            total_battles_duplicate += 1
    monsters_found_overall = 0
    for _, monster_values in monster_dict.items():
        monsters_found_overall += monster_values["pick"]
    monsters_not_found_overall = sum(none_monsters_dict.values())
    monsters_overall = monsters_found_overall + monsters_not_found_overall
    # adjust for 10 units per battle(on average)
    total_battles_overall = ceil(monsters_overall / 10)
    # fix pick-percentages baes on total battles since the beginning and not only for latest batch
    fix_pick_perc(total_battles_overall)
    print("Total battles added = %d" % total_battles)
    print("Total battles parsed including duplicate = %d" % total_battles_duplicate)
    print("Total not found %d out of %d monsters" % (monsters_not_found_overall, monsters_overall))
    with open('db/data.json', 'w') as outfile:
        dump(monster_dict, outfile, indent=4)
    with open('db/not_found.json', 'w') as outfile:
        dump(none_monsters_dict, outfile, indent=4)
    with open('db/rids.txt', 'w') as filehandle:
        for listitem in replay_rids:
            filehandle.write('%d\n' % listitem)
    # DEBUG: print seara info
    # print(monster_dict["Seara"])
    return

def get_picks(battle: dict, won_battle: bool, picks_first: bool) -> None:
    battle_loop(battle['unit_list'], won_battle, picks_first)
    leader(battle['unit_list'], battle['leader_slot_id'])
    banned(battle['unit_list'], battle['banned_slot_ids'][0])

def battle_loop(unit_list: dict, won_battle: bool, picks_first: bool) -> None:
    for monster_data in unit_list:
        monster_id = monster_data['unit_master_id']
        monster_slot = monster_data['pick_slot_id']
        monster_name = monster_matcher(monster_id)
        if monster_name == None:
            global none_monsters_dict
            none_monsters_dict[monster_id] = none_monsters_dict.get(monster_id, 0) + 1
        else:
            global monster_dict
            monster_name = str(monster_name)
            monster_dict_base = monster_dict[monster_name]
            monster_dict_base['pick'] += 1
            # monster_dict[monster_name]['pick-perc'] = monster_dict[monster_name]['pick'] / total_battles * 100
            if won_battle:
                monster_dict[monster_name]['win'] += 1
            monster_dict[monster_name]['win-perc'] = monster_dict[monster_name]['win'] / monster_dict[monster_name]['pick'] * 100
            # check slot 1 only for the first pick player and slot 5 only for the second pick player
            if (monster_slot == 1) & picks_first:
                monster_dict[monster_name]['first'] += 1
                if won_battle:
                    # how many won as first pick / how many played as first pick
                    monster_dict[monster_name]['1p-win'] += 1
                monster_dict[monster_name]['1p-win-perc'] = monster_dict[monster_name]['1p-win'] / monster_dict[monster_name]['first'] * 100
            if (monster_slot == 5) & (not picks_first):
                monster_dict[monster_name]['last'] += 1
                if won_battle:
                    # how many won as last pick / how many played as last pick
                    monster_dict[monster_name]['5p-win'] += 1
                monster_dict[monster_name]['5p-win-perc'] = monster_dict[monster_name]['5p-win'] / monster_dict[monster_name]['last'] * 100
            monster_dict[monster_name]['first-perc'] = monster_dict[monster_name]['first'] / monster_dict[monster_name]['pick'] * 100
            monster_dict[monster_name]['last-perc'] = monster_dict[monster_name]['last'] / monster_dict[monster_name]['pick'] * 100
    return

def leader(unit_list: dict, leader_slot: int) -> None:
    for monster_data in unit_list:
        if monster_data['pick_slot_id'] == leader_slot:
            monster_name = monster_matcher(monster_data['unit_master_id'])
            if monster_name == None:
                continue
            monster_name = str(monster_name)
            monster_dict[monster_name]['leader'] += 1
            monster_dict[monster_name]['leader-perc'] = monster_dict[monster_name]['leader'] / monster_dict[monster_name]['pick'] * 100
    return 

def banned(unit_list: dict, banned_slot: int) -> None:
    for monster_data in unit_list:
        if monster_data['pick_slot_id'] == banned_slot:
            monster_name = monster_matcher(monster_data['unit_master_id'])
            if monster_name == None:
                continue
            monster_dict[monster_name]['banned'] += 1
            monster_dict[monster_name]['banned-perc'] = monster_dict[monster_name]['banned'] / monster_dict[monster_name]['pick'] * 100
    return

def monster_matcher(id: int) -> str:
    res = next((key for key in corresp_dict if corresp_dict[key] == str(id)), None) 
    return res

def fix_pick_perc(num_battles):
    for monster_name in monster_dict:
        monster_dict[monster_name]['pick-perc'] = monster_dict[monster_name]['pick'] / num_battles * 100

if __name__ == "__main__":
    main()