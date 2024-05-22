from tabulate import tabulate
from .common_utils import get_running_time, timeout

def queued_builds(server, killtime, queue_list):
    queued_builds = server.get_queue_info()
    print(queued_builds)
    if not queued_builds:
        print("The queue is empty")
        return

    table_data = []

    for build in queued_builds:
        queued_since = get_running_time(build["inQueueSince"])
        if timeout(queued_since, killtime):
            table_data.append([build['id'], build['why'], queued_since])
            queue_list.append(build['id'])

    if queue_list:
        print("QUEUED BUILDS TO BE CANCELLED:")
        print(tabulate(table_data, headers=["Job ID", "Why", "Time queued (hh/mm)"], tablefmt="grid"))
    else:
        print(f"There are no builds queued for over {killtime} hours.")

def kill_job(server, queue_list):
    if queue_list:
        for i in queue_list:
            print(f"Killing build {i}")
            server.cancel_queue(i)