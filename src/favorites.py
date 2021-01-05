import os 
import sys, getopt

from json import loads
import csv
import datetime 

corresp_dict = {}
duplicate_battles = 0
battles_added = 0 

def main(argv: list) -> None:
    # move to parent directory to have access to /db/ folder
    os.chdir("./..") 
    in_file = "data/full_log_6_0_mb.txt"
    out_file = "users/"
    csv_top100 = "db_top/"
    try:
      opts, _ = getopt.getopt(argv,"hi:o:c:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('favorites.py -i <inputfile> -o <outputfile> -c <csv_top100>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('favorites.py -i <inputfile> -o <outputfile> -c <csv_top100>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            in_file = arg
        elif opt in ("-o", "--ofile"):
            out_file = arg
        elif opt in ("-c"):
            csv_top100 = arg
    # print('Input file is: ', in_file)
    # print('Output file is: ', out_file)

    # get latest top 100 csv file
    csv_top100 = get_latest_top100_csv(csv_top100)
    # create user dir if not exists
    create_dir(out_file)
    # load monster-monster_id correspondence 
    mapping_file = "mapping/mapping.txt"    
    make_correspondence(mapping_file)
    # parse file
    parse_file(in_file, out_file, csv_top100)
    return 

def get_latest_top100_csv(directory: str) -> str:
    files = sorted(os.listdir(directory), reverse=True)
    for file in files:
        if file.endswith(".csv"):
            return directory + file

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

def parse_file(in_file: str, out_file: str, csv_top100: str) -> None:
    global duplicate_battles
    global battles_added
    f = open(in_file).read()
    split_phrase = "API Command: getRtpvpReplayList"
    # split on getRtpvpReplayList
    # for each one (1 user):
    for each in f.split(split_phrase)[1:]:
        each = each.split("Response:")[1]
        each = each.split("API Command:")[0]
        json_each = loads(each)
        if json_each["replay_list"] == []:
            continue
        name = json_each["replay_list"][0]["wizard_name"]
        folder_name = out_file + name + '/'
        # create directory (if doesnt exist)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # check top100.csv to see if users exists on top100
        first_row, player_row = check_user_top100(name, csv_top100)
        if not player_row:
            continue
        first_row.append("timestamp")
        player_row.append(datetime.datetime.now())  
        # if exists add on "general.csv" the line + timestamp
        general_file = folder_name + "general.csv"
        if os.path.exists(general_file):
            with open(general_file, 'a+') as f:
                write = csv.writer(f)                 
                write.writerow(player_row)
        else:
            with open(general_file, 'a+') as f:
                write = csv.writer(f) 
                write.writerow(first_row)
                write.writerow(player_row)
        # create battles.csv for user if doesnt exist
        columns = create_columns()
        battle_file = folder_name + "battles.csv"
        if not os.path.exists(battle_file):
            with open(battle_file, 'a+') as f:
                write = csv.writer(f)                 
                write.writerow(columns)
        # for every replay
        # add an entry on battles.csv as a new line (INCLUDE BATTLE No. ID)
        for battle in json_each["replay_list"]:
            battle_info = []
            with open(battle_file, 'r') as f:
                all_lines = f.read().splitlines()
                battle_cnt = len(all_lines) - 1
            battle_info.append(battle_cnt)
            opp_won_battle = bool(battle['win_lose'] -1)
            opp_first_pick = bool(battle['first_slot_id'] - 1)
            m1 = ""
            m5 = ""
            l = ""
            b = ""
            opp_m1 = ""
            opp_m5 = ""
            opp_l = ""
            opp_b = ""
            battle_info.append(not opp_won_battle)
            # favorite user part
            leader_slot = battle["pick_info"]["leader_slot_id"]
            banned_slot = battle["pick_info"]["banned_slot_ids"][0]
            for unit in battle["pick_info"]["unit_list"]:
                monster_id = unit["unit_master_id"]
                monster_name = monster_matcher(monster_id)
                if monster_name == None:
                    monster_name = 'NF_' + str(monster_id)
                battle_info.append(monster_name)
                if unit["pick_slot_id"] == 1:
                    m1 = monster_name
                if unit["pick_slot_id"] == 5:
                    m5 = monster_name
                if unit["pick_slot_id"] == leader_slot:
                    l = monster_name
                if unit["pick_slot_id"] == banned_slot:
                    b = monster_name
            if opp_first_pick:
                battle_info.append('None')
                battle_info.append(m5)
            else:
                battle_info.append(m1)
                battle_info.append('None')
            battle_info.append(l)
            battle_info.append(b)
            # opponent part
            leader_slot = battle["opp_pick_info"]["leader_slot_id"]
            banned_slot = battle["opp_pick_info"]["banned_slot_ids"][0]
            for unit in battle["opp_pick_info"]["unit_list"]:
                monster_id = unit["unit_master_id"]
                monster_name = monster_matcher(monster_id)
                if monster_name == None:
                    monster_name = 'NF_' + str(monster_id)
                battle_info.append(monster_name)
                if unit["pick_slot_id"] == 1:
                    opp_m1 = monster_name
                if unit["pick_slot_id"] == 5:
                    opp_m5 = monster_name
                if unit["pick_slot_id"] == leader_slot:
                    opp_l = monster_name
                if unit["pick_slot_id"] == banned_slot:
                    opp_b = monster_name
            if opp_first_pick:
                battle_info.append(opp_m1)
                battle_info.append('None')
            else:
                battle_info.append('None')
                battle_info.append(opp_m5)
            battle_info.append(opp_l)
            battle_info.append(opp_b)
            battle_info.append(battle["date_add"])
            battle_exists = False
            with open(battle_file, 'r') as f:
                all_lines = f.read().splitlines()
                for line in all_lines[-100:]:
                    if battle_info[2:] == line.split(',')[2:]:
                       battle_exists = True
                       break
            if not battle_exists:
                battles_added += 1
                with open(battle_file, 'a') as f:
                    write = csv.writer(f) 
                    write.writerow(battle_info)
            else:
                duplicate_battles += 1
    print("For each favorite USER")
    print("Total duplicate battles: %d" % duplicate_battles)
    print("Total battles added: %d" % battles_added)
    print("Added replays: Completed")
    print("--------------------")                

def create_columns() -> list:
    list_names = [
        "battle_#",
        "win_loss",
        "p1",
        "p2",
        "p3",
        "p4",
        "p5",
        "first",
        "last",
        "leader",
        "banned",
        "opp_p1",
        "opp_p2",
        "opp_p3",
        "opp_p4",
        "opp_p5",
        "opp_first",
        "opp_last",
        "opp_leader",
        "opp_banned",
        "date_added",
    ]
    return list_names

def check_user_top100(name: str, csv_file: str) -> (list, list):
    first_row = ""
    info_row = ""
    with open(csv_file, 'rt', encoding='utf8') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            if r == 0:
                first_row = row
            if row[3] == name:
                info_row = row
    return first_row, info_row

def create_dir(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def monster_matcher(id: int) -> str:
    res = next((key for key in corresp_dict if corresp_dict[key] == str(id)), None) 
    return res

if __name__ == "__main__":
    main(sys.argv[1:])