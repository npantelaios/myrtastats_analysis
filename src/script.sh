python monsters_analysis.py -i data/full_log_6_0_mb.txt -a db/data.json -b db/not_found.json -c db/rids.txt
python json2csv.py -i db/data.json -o db/data.csv -t "a"
python top100_analysis.py -i data/full_log_6_0_mb.txt -o db/top100.json
python json2csv.py -i db/top100.json -o db/top100.csv -t "b"
