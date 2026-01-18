import pandas as pd


class Detector:

    def __init__(self):
        self.buffer = pd.DataFrame()
        self.blacklist = self.load_blacklist()

    def load_blacklist(self):
        try:
            with open("blacklist.txt") as f:
                return set(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            return set()

    def update_buffer(self, df: pd.DataFrame):
        self.buffer = pd.concat([self.buffer, df], ignore_index=True)
        self.buffer = self.buffer.sort_values("timestamp")

        # keep only last 10 minutes
        cutoff = pd.Timestamp.utcnow() - pd.Timedelta(minutes=10)
        self.buffer = self.buffer[self.buffer["timestamp"] >= cutoff]


    # DETECTIONS

    def detect_blacklisted_ip(self, df):
        for ip in df["ip"].unique():
            if ip in self.blacklist:
                self.raise_alert("BLACKLISTED_IP", ip)




