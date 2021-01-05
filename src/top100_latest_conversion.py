import os 
import sys, getopt

from shutil import copyfile

def main(argv: list) -> None:
    os.chdir("./..")
    in_file = ""
    try:
      opts, _ = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        print('top100_analysis.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('top100_analysis.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            in_file = arg

    rename_latest_top100_file(in_file)
    print("Top100 latest file conversion: Completed")
    print("--------------------")                

def rename_latest_top100_file(top100_folder: str) -> None:
    latest_top100_file = sorted(os.listdir(top100_folder), reverse=True)
    for f in latest_top100_file:
        if f.endswith(".csv"):
            latest_top100_file = top100_folder + f
    dst = latest_top100_file.split('top100_')[0] + "top100.csv"
    copyfile(latest_top100_file, dst)
    return 

if __name__ == "__main__":
   main(sys.argv[1:])