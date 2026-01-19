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

    def detect_bruteforce(self):
        failed = self.buffer[
            (self.buffer["endpoint"] == "/login") &
            (self.buffer["status"] >= 400)
        ]

        grouped = failed.groupby("ip")

        for ip, group in grouped:
            if len(group) < 10:
                continue

            time_diff = group["timestamp"].max() - group["timestamp"].min()

            if time_diff <= pd.Timedelta(minutes=2):
                self.raise_alert("BRUTE_FORCE", ip)

    def detect_blacklisted_ip(self, df):
        for ip in df["ip"].unique():
            if ip in self.blacklist:
                self.raise_alert("BLACKLISTED_IP", ip)

    def detect_traffic_spike(self):
        now = pd.Timestamp.utcnow()

        last_minute = self.buffer[
            self.buffer["timestamp"] >= now - pd.Timedelta(minutes=1)
        ]

        prev_minute = self.buffer[
            (self.buffer["timestamp"] >= now - pd.Timedelta(minutes=2)) &
            (self.buffer["timestamp"] < now - pd.Timedelta(minutes=1))
        ]

        if len(prev_minute) > 0 and len(last_minute) > 10 * len(prev_minute):
            self.raise_alert("TRAFFIC_SPIKE", "GLOBAL")

    def detect_500_spike(self):
        errors = self.buffer[self.buffer["status"] >= 500]

        if len(errors) >= 5:
            self.raise_alert("SERVER_ERROR_SPIKE", "GLOBAL")

    def detect_suspicious_ua(self, df):
        suspicious = ["sqlmap", "nikto", "nmap", "curl"]

        for _, row in df.iterrows():
            ua = row["user_agent"]
            for pattern in suspicious:
                if pattern.lower() in ua.lower():
                    self.raise_alert("SUSPICIOUS_USER_AGENT", row["ip"])


