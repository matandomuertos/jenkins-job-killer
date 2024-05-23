from datetime import datetime

def get_running_time(timestamp_ms):
    timestamp_sec = timestamp_ms / 1000
    timestamp_datetime = datetime.fromtimestamp(timestamp_sec)
    current_datetime = datetime.now()
    duration_seconds = (current_datetime - timestamp_datetime).total_seconds()
    hours = int(duration_seconds // 3600)
    minutes = int((duration_seconds % 3600) // 60)
    return f"{hours:02}:{minutes:02}"

def timeout(object_time, killtime):
    hours, minutes = map(int, object_time.split(':'))
    return hours >= killtime