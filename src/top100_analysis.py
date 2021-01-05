import os 
import sys, getopt

from json import loads, dump
from datetime import datetime

def main(argv: list) -> None:
    os.chdir("./..")
    in_file = "data/full_log_6_0_mb.txt"
    # out_file = "db_top/top100_season15_normal.json" #"data/full_log_6_0_mb.txt" ENTRY: 4
    # out_file = "db_top/top100_season15_sl.json" # "data/full_log_6_0_mb.txt" ENTRY: 1-3, 5-8
    out_file = "db_top/"   
    try:
      opts, _ = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('top100_analysis.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('top100_analysis.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            in_file = arg
        elif opt in ("-o", "--ofile"):
            out_file = arg
    # print('Input file is: ', in_file)
    # print('Output file is: ', out_file)

    ts = datetime.now()
    out_file += "top100_" + str(ts.year) + '_' + str(ts.month) + '_' + str(ts.day) + '_' + str(ts.hour) + '_' + str(ts.minute) + '_' + str(ts.second) + ".json"
    top100_grab(in_file, out_file)

    print("Top100 analysis: Completed")
    print("--------------------")                

def top100_grab(in_file: str, out_file: str) -> None:
    f = open(in_file).read()
    split_phrase = "API Command: RTPvPWorldRanking"
    latest = f.split(split_phrase)[-1]
    latest = latest.split("Response:")[1]
    latest = latest.split("API Command:")[0]
    json_all = loads(latest)
    json_others = json_all['world_ranking']
    for i, each in enumerate(json_others):
        wins = each['win_count']
        losses = each['lose_count']
        draws = each['draw_count']
        total_battles = wins + losses + draws
        json_others[i]['total_battles'] = total_battles
        json_others[i]['win-perc'] = wins / total_battles
        del json_others[i]['channel_uid']
        del json_others[i]['id'] 
        del json_others[i]['wizard_id'] 
        del json_others[i]['wizard_level'] 
        del json_others[i]['rtpvp_rating_id']
    with open(out_file, 'w') as outfile:
        dump(json_others, outfile, indent=4, ensure_ascii=False)

if __name__ == "__main__":
   main(sys.argv[1:])