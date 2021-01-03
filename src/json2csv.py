# Python program to convert 
# JSON file to CSV 
import os 
import sys, getopt

import glob
import csv
import json 
import pandas as pd
from xlsxwriter.workbook import Workbook

int_columns = []
float_columns = []

def main(argv: list) -> None:
    # move to parent directory to have access to /db/ folder
    os.chdir("./..") 
    in_file = 'db/data.json'
    out_file = 'db/data.csv'
    file_type = ''
    try:
      opts, _ = getopt.getopt(argv,"hi:o:t:",["ifile=","ofile=","type="])
    except getopt.GetoptError:
        print('json2csv.py -i <inputfile> -o <outputfile> -t <type>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('json2csv.py -i <inputfile> -o <outputfile> -t <type>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            in_file = arg
        elif opt in ("-o", "--ofile"):
            out_file = arg
        elif opt in ("-t", "--type"):
            file_type = arg
    print('Input file is: ', in_file)
    print('Output file is: ', out_file)

    distinguish_file_type(file_type)

    if file_type == "b":
        in_file = in_file + sorted(os.listdir(in_file))[-1]
        out_file = in_file.split('.')[0] + ".csv"
    json_2_df(in_file, out_file, file_type)
    if file_type == "a":
        add_to_start_of_file(out_file, 'monster_name')
    elif file_type == "b":
        add_to_start_of_file(out_file, '#')
    csv_2_xlsx(out_file)

    print(".json to .csv and to .xlsx : Completed\n")

def distinguish_file_type(file_type: str):
    global int_columns, float_columns
    if file_type == "a":
        int_columns = [1,3,5,7,9,11,13,14]
        float_columns = [2,4,6,8,10,12,15,16]
    elif file_type == "b":
        int_columns = [1,4,5,6,7,8,9]
        float_columns = [10]  
    elif file_type == "c":
        int_columns = []
        float_columns = [] 

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

def json2csv(in_file: str, out_file: str) -> None:
    # Opening JSON file and loading the data 
    # into the variable data
    with open(in_file) as json_file: 
        data = json.load(json_file) 
    
    employee_data = data
    
    # now we will open a file for writing 
    data_file = open(out_file, 'w') 
    
    # create the csv writer object 
    csv_writer = csv.writer(data_file) 
    
    # Counter variable used for writing  
    # headers to the CSV file 
    count = 0
    
    for emp in employee_data: 
        if count == 0: 
    
            # Writing headers of CSV file 
            header = emp.keys() 
            csv_writer.writerow(header) 
            count += 1
    
        # Writing data of CSV file 
        csv_writer.writerow(emp.values()) 
    
    data_file.close() 

def add_to_start_of_file(filename, added_part):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(added_part + content)

def csv_2_xlsx(out_file) -> None:
    # for csvfile in glob.glob(os.path.join('./db', '*.csv')):
    csv_file = out_file
    workbook = Workbook(csv_file[:-4] + '.xlsx')
    worksheet = workbook.add_worksheet()
    with open(csv_file, 'rt', encoding='utf8') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                if r == 0:
                    worksheet.write(r, c, col)
                    continue
                if c in int_columns:
                    col = int(col)
                elif c in float_columns:
                    col = float(col)
                worksheet.write(r, c, col)
    workbook.close()

if __name__ == "__main__":
    main(sys.argv[1:])