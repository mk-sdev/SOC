import re, os, csv
from datetime import datetime

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) '                # server IP or proxy
    r'\S+ \S+ '                    # identd / user
    r'\[(?P<timestamp>[^\]]+)\] '  # timestamp
    r'"(?P<method>\S+) '
    r'(?P<endpoint>\S+) '
    r'\S+" '
    r'(?P<status>\d{3}) '          # status code
    r'\S+ '
    r'"[^"]*" '
    r'"(?P<user_agent>[^"]+)"'
)

def parse_line(line: str):
    match = LOG_PATTERN.match(line)
    if not match:
        return None

    data = match.groupdict()

    # converting timestamps to a timestamp object
    data["timestamp"] = datetime.strptime(data["timestamp"], "%d/%b/%Y:%H:%M:%S %z")

    # search for client ip
    client_ip_match = re.search(r'"(?P<client_ip>\d+\.\d+\.\d+\.\d+)"$', line)
    if client_ip_match:
        data["ip"] = client_ip_match.group("client_ip")
    
    return {
        "ip": data["ip"],
        "timestamp": data["timestamp"],
        "status": int(data["status"]),
        "endpoint": data["endpoint"],
        "user_agent": data["user_agent"]
    }


OUTPUT_FILE = "/logs/parsed_logs.csv"

def save_to_csv(parsed_log):
    file_exists = os.path.exists(OUTPUT_FILE)

    with open(OUTPUT_FILE, mode='a', newline='') as file:
        print("opening file")
        writer = csv.DictWriter(file, fieldnames=["ip", "timestamp", "status", "endpoint", "user_agent"])

        if not file_exists:
            print("file not exist")
            writer.writeheader()
            
        writer.writerow(parsed_log)