import os 
import sys, getopt

def main(argv: list) -> None:
    # move to parent directory to have access to /db/ folder
    os.chdir("./..") 
    in_file = 'users/'
    out_file = 'users/'
    try:
      opts, _ = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
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
    print('Input file is: ', in_file)
    print('Output file is: ', out_file)
    parse_file(in_file, out_file)


def parse_file(in_file: str, out_file: str) -> None:
    f = open(in_file).read()
    split_phrase = "API Command: getRtpvpReplayList"
    # split on getRtpvpReplayList
    # for each one (1 user):

    # create directory (if doesnt exist)

    # check top100.csv to see if users exists on top100
    # if exists add on "general.csv" the line + timestamp
    # if not -> do nothing

    # for every replay
    # add an entry on battles.csv as a new line (INCLUDE BATTLE No. ID)
    
if __name__ == "__main__":
    main(sys.argv[1:])