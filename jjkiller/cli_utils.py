import argparse

def parse_args():
    parser = argparse.ArgumentParser(prog='jjkiller', description='Jenkins jobs killer')
    parser.add_argument('-url', '--url', type=str, required=True, help='Specify Jenkins server URL')
    parser.add_argument('-u', '--user', type=str, required=True, help='Specify Jenkins user')
    parser.add_argument('-p', '--password', type=str, required=True, help='Specify Jenkins password or token')
    parser.add_argument('--queue', action='store_true', help='Clean up queued builds')
    parser.add_argument('--jenkins-version', action='store_true', help='Print Jenkins server version')
    parser.add_argument('--version', action='store_true', help='Print jjkiller version and exit')
    parser.add_argument('--time-out', '-t', type=int, default=4, help='Set timeout for stopping builds in hours (default: 4)')
    parser.add_argument('--dry-run', action='store_true', help='Run in dry mode (no actions will be taken)')
    return parser.parse_args()
