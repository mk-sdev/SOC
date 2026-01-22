import re
import pandas as pd

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) '                # IP
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


def parse_line(line: str) -> pd.DataFrame | None:
    match = LOG_PATTERN.match(line)
    if not match:
        return None

    data = match.groupdict()

    # Konwersje typów
    data["status"] = int(data["status"])
    data["timestamp"] = pd.to_datetime(
        data["timestamp"],
        format="%d/%b/%Y:%H:%M:%S %z",
        errors="coerce"
    )

    return pd.DataFrame([{
        "ip": data["ip"],
        "timestamp": data["timestamp"],
        "status": data["status"],
        "endpoint": data["endpoint"],
        "user_agent": data["user_agent"]
    }])

OUTPUT_FILE = "/logs/parsed_logs.csv"

def save_to_csv(df):
    df.to_csv(
        OUTPUT_FILE,
        mode="a",
        header=not pd.io.common.file_exists(OUTPUT_FILE),
        index=False
    )
