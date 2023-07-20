import sys
import argparse
import subprocess
from entry import ProjectInitializer
from agg import FunctionAggregator

def process_arguments():
    parser = argparse.ArgumentParser(prog='eclair', description='A tool to create library wrappers for Blockchain Business Logic code.')

    subparsers = parser.add_subparsers(dest='command')
    init_parser = subparsers.add_parser('init', help='Initialize a new project')
    # Add more subparsers for different commands if needed

    args = parser.parse_args()

    if args.command == 'init':
        project = ProjectInitializer()
        project.initialize_project()
    else:
        function_aggregator = FunctionAggregator()
        function_aggregator.process_files()

if __name__ == '__main__':
    sys.exit(process_arguments())
