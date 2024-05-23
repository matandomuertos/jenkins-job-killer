import jenkins
from tabulate import tabulate
from urllib.parse import urlparse
from .common_utils import get_running_time, timeout

def running_builds(server, killtime, buildlist):
    running_builds = get_running_builds(server)
    
    if not running_builds:
        print("There are no builds running.")
        return
    
    table_data = []
    
    for build in running_builds:
        build_url, build_node, build_time, build_name, build_number = parse_build_data(build, server)
        if timeout(build_time, killtime):
            table_data.append([build_url, build_node, build_time])
            buildlist.append([build_name, build_number])
    
    if buildlist:
        print("BUILDS TO BE STOPPED:")
        print(tabulate(table_data, headers=["Build URL", "Node", "Time running (hh/mm)"], tablefmt="grid"))
    else:
        print(f"There are no builds running for over {killtime} hours.")

def get_running_builds(server, max_retries: int = 10):
    for attempt in range(max_retries):
        try:
            return server.get_running_builds()
        except jenkins.JenkinsException as e:
            print(f"Error: {e}. Retrying... ({attempt + 1}/{max_retries})")
    print(f"Failed to get the running builds after {max_retries} retries.")
    exit()

def parse_build_data(build, server):
    build_name = parse_build_url(build['url'])
    build_info = server.get_build_info(build_name, build["number"])
    build_time = get_running_time(build_info['timestamp'])
    return build['url'], build['node'], build_time, build_name, build["number"]

def parse_build_url(build_url):
    parsed_url = urlparse(build_url)
    path_parts = parsed_url.path.split('/')
    cleaned_path = [part for part in path_parts if part != 'job' and part != '' and not part.isdigit()]
    cleaned_path = [part.replace('%20', ' ') if part != '' else part for part in cleaned_path]
    cleaned_path = [part.replace('%252', '%2') if part != '' else part for part in cleaned_path]
    return '/'.join(cleaned_path)

def kill_build(server, buildlist):
    if buildlist:
        for i in buildlist:
            print(f"Killing build {i[0]}/{i[1]}")
            server.stop_build(i[0], i[1])