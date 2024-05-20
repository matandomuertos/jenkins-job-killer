import jenkins
import argparse
from urllib.parse import urlparse
from datetime import datetime
from tabulate import tabulate

def main():
  args = parse_args()
  try:
    server = server_connection(args.url, args.user, args.password)
  except jenkins.JenkinsException as e:
    print(f"Error: {e}")

  print("Sucessfully logged as", server.get_whoami()['id'])

  if args.queue:
    print_queue(server.get_queue_info())

  if args.version:
    print("Jenkins server version:", server.get_version())

  buildlist = []
  running_builds(server, args.time_out, buildlist)

  if buildlist:
    if args.dry_run:
      print("Running in dry mode, nothing will be stopped")
    else:
      kill_build(server, buildlist)

def parse_args():
  parser = argparse.ArgumentParser(prog='jjkiller', description='Jenkins jobs killer')
  parser.add_argument('-url', '--url', type=str, required=True, help='Specify URL')
  parser.add_argument('-u', '--user', type=str, required=True, help='Specify user')
  parser.add_argument('-p', '--password', type=str, required=True, help='Specify password or token')
  parser.add_argument('--queue', action='store_true', help='Prints list of current queued jobs')
  parser.add_argument('--version', action='store_true', help='Prints Jenkins version')
  parser.add_argument('--time-out','-t', type=int, default=4, help='Set the timeout for builds that need to be stopped')
  parser.add_argument('--dry-run', action='store_true', help='Dry run mode')
  return parser.parse_args()

def server_connection(url,user,passwd):
  return jenkins.Jenkins(url, username=user, password=passwd)

def print_queue(queue_info):
  if queue_info:
    print("QUEUE:")
    table_data = []
    for i in queue_info:
      table_data.append([i['id'], i['stuck'], i['why']])
    print(tabulate(table_data, headers=["Job ID", "isStuck", "Why"], tablefmt="grid"))
  else:
    print('The queue is empty')

def running_builds(server, killtime, buildlist):
  running_builds = server.get_running_builds()
  if running_builds:
    table_data = []
    for i in running_builds:
      build_name = parse_build_url(i['url'])
      build_info = server.get_build_info(build_name, i["number"])
      build_time = get_build_running_time(build_info['timestamp'])
      if timeout(build_time, killtime):
        table_data.append([i['url'], i['node'], build_time])
        buildlist.append([build_name, i["number"]])
    if buildlist:
      print("BUILDS TO BE STOPPED:")
      print(tabulate(table_data, headers=["Build URL", "Node", "Time running (hh/mm)"], tablefmt="grid"))
    else:
      print(f"There are not builds running for over {killtime} hours")
  else:
    print("There are no builds running")

def kill_build(server,buildlist):
  if buildlist:
    for i in buildlist:
      print(f"Killing build {i[0]}/{i[1]}")
      server.stop_build(i[0], i[1])

def parse_build_url(build_url):
  parsed_url = urlparse(build_url)
  path_parts = parsed_url.path.split('/')
  cleaned_path = [part for part in path_parts if part != 'job' and part != '' and not part.isdigit()]
  cleaned_path = [part.replace('%20', ' ') if part != '' else part for part in cleaned_path]
  cleaned_path = [part.replace('%252', '%2') if part != '' else part for part in cleaned_path]
  return '/'.join(cleaned_path)

def get_build_running_time(timestamp_ms):
  timestamp_sec = timestamp_ms / 1000
  timestamp_datetime = datetime.fromtimestamp(timestamp_sec)
  current_datetime = datetime.now()
  duration_seconds = (current_datetime - timestamp_datetime).total_seconds()
  hours = int(duration_seconds // 3600)
  minutes = int((duration_seconds % 3600) // 60)
  return f"{hours:02}:{minutes:02}"

def timeout(build_time, killtime):
  hours, minutes = map(int, build_time.split(':'))
  if hours >= killtime:
    return 1
  else:
    return 0

if __name__ == "__main__":
  main()