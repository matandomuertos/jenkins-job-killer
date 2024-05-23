import argparse

def parse_args():
    parser = argparse.ArgumentParser(prog='jjkiller', description='Jenkins jobs killer')
    parser.add_argument('-url', '--url', type=str, required=True, help='Specify URL')
    parser.add_argument('-u', '--user', type=str, required=True, help='Specify user')
    parser.add_argument('-p', '--password', type=str, required=True, help='Specify password or token')
    parser.add_argument('--queue', action='store_true', help='Cleans up queued builds')
    parser.add_argument('--version', action='store_true', help='Prints Jenkins version')
    parser.add_argument('--time-out', '-t', type=int, default=4, help='Set the timeout for builds that need to be stopped')
    parser.add_argument('--dry-run', action='store_true', help='Dry run mode')
    return parser.parse_args()