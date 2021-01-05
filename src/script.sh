#!/bin/bash   
# SEASONS -> THIS CHANGES
SEASON15_SL1_INPUT="data/full_log_6_0_mb.txt"
SEASON15_SL2_INPUT="sw_exporter_logs/full_log.txt" # this maybe doesnt change
SEASON15_SL2_OUTPUT="output_s15_sl2/"

# all season monsters
DB="db/"
MONSTERS_ALL="db/monsters_all"
NOT_FOUND_ALL="db/not_found"
RIDS="db/rids.txt"
TOP100="top100/"
USERS_FOLDER="users/"

# where to copy the output folder
OTHER_GITHUB="/home/nikos/Documents/generalRepo/live_website_stats/data/"

mkdir -p "../$SEASON15_SL2_OUTPUT"
mkdir -p "../$SEASON15_SL2_OUTPUT$DB"
mkdir -p "../$SEASON15_SL2_OUTPUT$TOP100"
mkdir -p "../$SEASON15_SL2_OUTPUT$USERS_FOLDER"
python monsters_analysis.py -i "$SEASON15_SL2_INPUT" -a "$SEASON15_SL2_OUTPUT$MONSTERS_ALL.json" -b "$SEASON15_SL2_OUTPUT$NOT_FOUND_ALL.json" -c "$SEASON15_SL2_OUTPUT$RIDS"
python json2csv.py -i "$SEASON15_SL2_OUTPUT$MONSTERS_ALL.json" -o "$SEASON15_SL2_OUTPUT$MONSTERS_ALL.csv" -t "a"
python top100_analysis.py -i "$SEASON15_SL2_INPUT" -o "$SEASON15_SL2_OUTPUT$TOP100"
python json2csv.py -i "$SEASON15_SL2_OUTPUT$TOP100" -o "$SEASON15_SL2_OUTPUT$TOP100" -t "b"
python favorites.py -i "$SEASON15_SL2_INPUT" -o "$SEASON15_SL2_OUTPUT$USERS_FOLDER" -c "$SEASON15_SL2_OUTPUT$TOP100"
python top100_latest_conversion.py -i "$SEASON15_SL2_OUTPUT$TOP100"
python monster_per_user.py -i "$SEASON15_SL2_OUTPUT$USERS_FOLDER"

cp -r "../$SEASON15_SL2_OUTPUT" "$OTHER_GITHUB"

# python monsters_analysis.py -i data/full_log_6_0_mb.txt -a db/data.json -b db/not_found.json -c db/rids.txt
# python json2csv.py -i db/data.json -o db/data.csv -t "a"
# python top100_analysis.py -i data/full_log_6_0_mb.txt -o db_top/
# python json2csv.py -i db_top/ -o db_top/ -t "b"
# python favorites.py -i data/full_log_6_0_mb.txt -o users/ -c db_top/