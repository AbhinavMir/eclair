import argparse
import subprocess

def process_arguments():
    parser = argparse.ArgumentParser(prog='eclair', description='A tool to create library wrappers for Blockchain Business Logic code.')

    subparsers = parser.add_subparsers(dest='command')
    init_parser = subparsers.add_parser('init', help='Initialize a new project')
    # Add more subparsers for different commands if needed

    args = parser.parse_args()

    if args.command == 'init':
        subprocess.call(["python", "src/entry.py"])
    else:
        subprocess.call(["python", "src/agg.py"])

if __name__ == '__main__':
    process_arguments()
