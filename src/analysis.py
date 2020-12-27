import os

from json import load
from pathlib import Path

def main():    
    first_analysis()


def first_analysis():
    os.chdir("./..")
    f = open("./data/logs.json")
    dict = load(f)
    print(dict["replay_list"][0]["wizard_name"])

def return_parent_path(import_path):
    path = Path(import_path)
    return path.parent

if __name__ == "__main__":
    main()