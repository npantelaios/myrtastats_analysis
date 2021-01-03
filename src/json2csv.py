# Python program to convert 
# JSON file to CSV 
import os 

import glob
import csv
import json 
import csv 
import pandas as pd
from xlsxwriter.workbook import Workbook

int_columns = [1,3,5,7,9,11,13,14]
float_columns = [2,4,6,8,10,12,15,16]

def main() -> None:
    # move to parent directory to have access to /db/ folder
    os.chdir("./..") 
    in_file = 'db/data.json'
    out_file = 'db/data.csv'
    json_2_df(in_file, out_file)
    add_to_start_of_file(out_file, 'monster_name')
    csv_2_xlsx()

def json_2_df(in_file: str, out_file: str) -> None:
    with open(in_file) as json_file: 
        df = pd.read_json(json_file)
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

def csv_2_xlsx() -> None:
    for csvfile in glob.glob(os.path.join('./db', '*.csv')):
        workbook = Workbook(csvfile[:-4] + '.xlsx')
        worksheet = workbook.add_worksheet()
        with open(csvfile, 'rt', encoding='utf8') as f:
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
    print("\n.json to .csv and to .xlsx : Completed")

if __name__ == "__main__":
    main()