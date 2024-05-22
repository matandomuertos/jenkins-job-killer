import jenkins

def server_connection(url, user, passwd):
    return jenkins.Jenkins(url, username=user, password=passwd)