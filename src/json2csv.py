# Python program to convert 
# JSON file to CSV 
import os 

import json 
import csv 
import pandas as pd

def json2df() -> None:
    os.chdir("./..")
    with open('db/data.json') as json_file: 
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
    df.to_csv('db/data.csv')
    return

def json2csv() -> None:
    os.chdir("./..") 
    # Opening JSON file and loading the data 
    # into the variable data
    with open('db/data.json') as json_file: 
        data = json.load(json_file) 
    
    employee_data = data
    
    # now we will open a file for writing 
    data_file = open('db/data.csv', 'w') 
    
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

if __name__ == "__main__":
    json2df()