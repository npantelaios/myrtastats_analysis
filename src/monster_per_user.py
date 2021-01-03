import os 
import sys, getopt

from json import loads, dump
import csv
import datetime 


def main(argv: list) -> None:
    # move to parent directory to have access to /db/ folder
    os.chdir("./..") 
    in_file = "users/"
    out_file = "users/"
    csv_top100 = "db_top/"
    try:
      opts, _ = getopt.getopt(argv,"hi:o:c:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('monsters_per_user.py -i <inputfile> -o <outputfile> -c <csv_top100>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('monsters_per_user.py -i <inputfile> -o <outputfile> -c <csv_top100>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            in_file = arg
        elif opt in ("-o", "--ofile"):
            out_file = arg
        elif opt in ("-c"):
            csv_top100 = arg
    print('Input file is: ', in_file)
    print('Output file is: ', out_file)

    # get latest top 100 csv file
    parse_battles_csvs(in_file, out_file)
    return 

#   0,         1,   2, 3, 4, 5, 6,   7,   8,   9,     10,    11,    12,    13,    14,    15,    16,        17,      18,        19,        20
# battle_#,win_loss,p1,p2,p3,p4,p5,first,last,leader,banned,opp_p1,opp_p2,opp_p3,opp_p4,opp_p5,opp_first,opp_last,opp_leader,opp_banned,date_added
def parse_battles_csvs(in_file: str, out_file: str) -> None:
    num_battles = 0
    for user_dir in os.listdir(in_file):
        monster_dict = {}
        battle_file = in_file + user_dir + '/' + "battles.csv"
        if not os.path.exists(battle_file):
            continue
        f = open(battle_file, 'rt', encoding='utf8')
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            if r == 0:
                continue
            user_won = row[1]
            # user
            for _, col in enumerate(row[2:7]):
                if not (col in monster_dict):
                    monster_dict[col] = set_default_dictionary()
                # monster_dict.setdefault(col, default_dict)
                monster_dict[col]["pick"] += 1
                if user_won:
                    monster_dict[col]["win"] += 1
            # first-last-leader-banned
            if not (row[7] == 'None'):
                monster_dict[row[7]]["first"] += 1
                if user_won:
                    monster_dict[row[7]]["1p-win"] += 1
            if not (row[8] == 'None'):
                monster_dict[row[8]]["last"] += 1
                if user_won:
                    monster_dict[row[8]]["5p-win"] += 1                
            monster_dict[row[9]]["leader"] += 1
            monster_dict[row[10]]["banned"] += 1
            # opponent
            for _, col in enumerate(row[11:16]):
                if not (col in monster_dict):
                    monster_dict[col] = set_default_dictionary()
                # monster_dict.setdefault(col, default_dict)
                monster_dict[col]["opp_pick"] += 1
                if user_won:
                    monster_dict[col]["opp_win"] += 1
            # first-last-leader-banned
            if not (row[16] == 'None'):
                monster_dict[row[16]]["opp_first"] += 1
                if not user_won:
                    monster_dict[row[16]]["opp_1p-win"] += 1
            if not (row[17] == 'None'):
                monster_dict[row[17]]["opp_last"] += 1
                if not user_won:
                    monster_dict[row[17]]["opp_5p-win"] += 1        
            # TODO: check if leader or banned is None -> maybe ot needed n=because renamed to NF_*..
            monster_dict[row[18]]["opp_leader"] += 1
            monster_dict[row[19]]["opp_banned"] += 1
            num_battles = r
        # user - perc
        for key in monster_dict:
            monster_dict[key]["pick_perc"] = monster_dict[key]["pick"] / num_battles * 100
            if monster_dict[key]["pick"] > 0:            
                monster_dict[key]["win_perc"] = monster_dict[key]["win"] / monster_dict[key]["pick"] * 100
                monster_dict[key]["leader_perc"] = monster_dict[key]["leader"] / monster_dict[key]["pick"] * 100
                monster_dict[key]["banned_perc"] = monster_dict[key]["banned"] / monster_dict[key]["pick"] * 100
                monster_dict[key]["first-perc"] = monster_dict[key]["first"] / monster_dict[key]["pick"] * 100
                monster_dict[key]["last-perc"] = monster_dict[key]["last"] / monster_dict[key]["pick"] * 100
            if monster_dict[key]["first"] > 0:
                monster_dict[key]["1p-win-perc"] = monster_dict[key]["1p-win"] / monster_dict[key]["first"] * 100
            if monster_dict[key]["last"] > 0:
                monster_dict[key]["5p-win-perc"] = monster_dict[key]["5p-win"] / monster_dict[key]["last"] * 100
        # opponent - perc
        for key in monster_dict:
            monster_dict[key]["opp_pick_perc"] = monster_dict[key]["opp_pick"] / num_battles * 100
            if monster_dict[key]["opp_pick"] > 0:
                monster_dict[key]["opp_win_perc"] = monster_dict[key]["opp_win"] / monster_dict[key]["opp_pick"] * 100
                monster_dict[key]["opp_leader_perc"] = monster_dict[key]["opp_leader"] / monster_dict[key]["opp_pick"] * 100
                monster_dict[key]["opp_banned_perc"] = monster_dict[key]["opp_banned"] / monster_dict[key]["opp_pick"] * 100
                monster_dict[key]["opp_first-perc"] = monster_dict[key]["opp_first"] / monster_dict[key]["opp_pick"] * 100
                monster_dict[key]["opp_last-perc"] = monster_dict[key]["opp_last"] / monster_dict[key]["opp_pick"] * 100
            if monster_dict[key]["opp_first"] > 0:
                monster_dict[key]["opp_1p-win-perc"] = monster_dict[key]["opp_1p-win"] / monster_dict[key]["opp_first"] * 100
            if monster_dict[key]["opp_last"] > 0:
                monster_dict[key]["opp_5p-win-perc"] = monster_dict[key]["opp_5p-win"] / monster_dict[key]["opp_last"] * 100
        # TODO: delete all NF_* keys from monster_dict
        f.close()
        json_file = out_file + user_dir + '/' + "battles.json"
        with open(json_file, 'w') as outfile:
            dump(monster_dict, outfile, indent=4)
    return 

def set_default_dictionary() -> dict:
    default_dict = {
        "pick": 0,
        "pick-perc": 0,
        "win": 0,
        "win-perc": 0,
        "leader": 0,
        "leader-perc": 0,
        "banned": 0,
        "banned-perc": 0,
        "first": 0,
        "first-perc": 0,
        "last": 0,
        "last-perc": 0,
        "1p-win": 0,
        "1p-win-perc": 0,
        "5p-win": 0,
        "5p-win-perc": 0,
        "user": "<--",
        "enemy": "-->",
        "opp_pick": 0,
        "opp_pick-perc": 0,
        "opp_win": 0,
        "opp_win-perc": 0,
        "opp_leader": 0,
        "opp_leader-perc": 0,
        "opp_banned": 0,
        "opp_banned-perc": 0,
        "opp_first": 0,
        "opp_first-perc": 0,
        "opp_last": 0,
        "opp_last-perc": 0,
        "opp_1p-win": 0,
        "opp_1p-win-perc": 0,
        "opp_5p-win": 0,
        "opp_5p-win-perc": 0,
    }
    return default_dict.copy()


def json_2_df(in_file: str, out_file: str, file_type: str) -> None:
    with open(in_file) as json_file: 
        df = pd.read_json(json_file)
    if(file_type == "a"):
        df = df.T.astype({
            "pick": int, 
            "win": int, 
            "leader": int, 
            "first": int, 
            "last": int, 
            "banned": int, 
            "1p-win": int, 
            "5p-win": int,
            })
    elif file_type == "b":
        df = df.astype({
            "server_id": int, 
            "rtpvp_score": int, 
            "win_count": int, 
            "lose_count": int, 
            "draw_count": int, 
            "rank": int, 
            "total_battles": int, 
            })
    elif file_type == "c":
        df = df.T.astype(          )
    df.to_csv(out_file)
    return

if __name__ == "__main__":
    main(sys.argv[1:])