import sys
import subprocess

def process_arguments():
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        subprocess.call(["python", "entry.py"])
    else:
        subprocess.call(["python", "agg.py"])

process_arguments()
