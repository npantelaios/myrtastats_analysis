python monsters_analysis.py -i data/full_log_6_0_mb.txt -a db/data.json -b db/not_found.json -c db/rids.txt
python json2csv.py -i db/data.json -o db/data.csv -t "a"
python top100_analysis.py -i data/full_log_6_0_mb.txt -o db_top/
python json2csv.py -i db_top/ -o db_top/ -t "b"
python favorites.py -i data/full_log_6_0_mb.txt -o users/ -c db_top/
