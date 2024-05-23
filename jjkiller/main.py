import jenkins
from jjkiller.cli_utils import parse_args
from jjkiller.jenkins_utils import server_connection
from jjkiller.queue_utils import queued_builds, kill_job
from jjkiller.builds_utils import running_builds, kill_build

def main():
    args = parse_args()

    if args.version:
        print("0.0.2")
        exit()

    if args.dry_run:
        print("Running in dry mode, nothing will be stopped or cancelled")

    try:
        server = server_connection(args.url, args.user, args.password)
    except jenkins.JenkinsException as e:
        print(f"Error: {e}")

    print("Successfully logged as", server.get_whoami()['id'])

    if args.jenkins_version:
        print("Jenkins server version:", server.get_version())

    queue_list = []
    if args.queue:
        queued_builds(server,args.time_out, queue_list)

    if queue_list and not args.dry_run:
        kill_job(server, queue_list)

    build_list = []
    running_builds(server, args.time_out, build_list)

    if build_list and not args.dry_run:
        kill_build(server, build_list)

if __name__ == "__main__":
    main()