import re, json
from datetime import datetime, timedelta
import urllib.parse
from ip_access_policy import IpAccessPolicy

class Detector:

    def __init__(self):
        self.brute_dict = {}  
        self.ip_policy = IpAccessPolicy()
        self.n = 0 # incremental alert log ID

    def run_all(self, log):
        self.detect_brute_force(log)
        self.detect_blacklisted_ip(log)
        self.detect_suspicious_ua(log)
        self.detect_sqli(log)
        self.detect_lfi(log)

    def detect_blacklisted_ip(self, log):
        ip = log["ip"]
        if self.ip_policy.is_blacklisted(ip):
            self.raise_alert("BLACKLISTED_IP",ip)

    def detect_brute_force(self, log):
        is_failed = log["endpoint"] == "/login" and log["status"] >= 400
        ip = log["ip"]

        if is_failed:
            timestamp = log["timestamp"]
            if ip not in self.brute_dict:
                self.brute_dict[ip] = []
            self.brute_dict[ip].append(timestamp)

            # delete old logs which are older than 10 minutes
            self.brute_dict[ip] = [t for t in self.brute_dict[ip] if t >= timestamp - timedelta(minutes=10)]

            allowed_attempts = 5 if self.ip_policy.is_rate_limited(ip) else 10

            # check for at least 10 or 5 failed attempts over last 2 minutes
            if len(self.brute_dict[ip]) == allowed_attempts:
                first_attempt_time = self.brute_dict[ip][0]
                last_attempt_time = self.brute_dict[ip][-1]

                # if the time between the 1st and 2nd try is shorter than 2 minutes
                if last_attempt_time - first_attempt_time <= timedelta(minutes=2):
                    self.raise_alert("BRUTE_FORCE", ip)

    def detect_suspicious_ua(self, log): 
        suspicious = ["sqlmap", "nikto", "nmap"]
        ua = log["user_agent"] 
        for pattern in suspicious: 
            if pattern.lower() in ua.lower(): 
                self.raise_alert("SUSPICIOUS_USER_AGENT", log["ip"])

    def detect_sqli(self, log):
        suspicious_patterns = [
        r"(\%27|\')\s*OR\s*1=1",        # ' OR 1=1
        r"(\%27|\')\s*AND\s*1=1",       # ' AND 1=1
        r"(\%27|\')\s*--",               # ' --
        r"(\%27|\')\s*UNION",            # ' UNION
        r"SELECT\s+\*",                  # SELECT *
        r"DROP\s+TABLE",                 # DROP TABLE
        r"INSERT\s+INTO",                # INSERT INTO
        r"\bEXEC\b",                     # EXEC (np. dla MSSQL)
        r"(\%27|\')\s*FROM",             # ' FROM
        r"(\%27|\')\s*LIKE",             # ' LIKE
        r"(\%27|\')\s*GROUP\s+BY",       # ' GROUP BY
        r"(\%27|\')\s*HAVING",           # ' HAVING
        r"\s*SELECT\s+\*\s+FROM\s+.*\s+WHERE",  # SELECT * FROM ... WHERE
        r"\s*UNION\s+SELECT\s+\*",       # UNION SELECT *
        r"(\%27|\')\s*ORDER\s+BY",       # ' ORDER BY
        r"(\%27|\')\s*JOIN",             # ' JOIN
        r"(\%27|\')\s*DROP\s+COLUMNS",   # ' DROP COLUMNS
        r"(\%27|\')\s*EXCEPT",           # ' EXCEPT
        r"(\%27|\')\s*=\s*1",            # ' = 1 (częste w prostych atakach)
        r"(\%27|\')\s*LIKE\s*'%'",       # ' LIKE '%'
    ]

        endpoint = log["endpoint"]
    
    # decode the URL
        decoded_endpoint = urllib.parse.unquote(endpoint)
    
        print("Decoded endpoint:", decoded_endpoint)

    # match the patterns
        for pattern in suspicious_patterns:
            if re.search(pattern, decoded_endpoint, re.IGNORECASE):
                print(f"Detected SQL Injection pattern: {pattern}")
                self.raise_alert("SQL_INJECTION", log["ip"])
                break

    def detect_lfi(self, log):
        # list of suspected LFI injection attempt patterns
        suspicious_patterns = [
            r"\.\./",                        
            r"etc/passwd",                   
            r"etc/hosts",                    
            r"(\.\./)+",                     
            r"etc/shadow",                   
            r"(\.\./){3,}",                  
            r"(\.\./){2,}etc",               
            r"(\.\./){2,}proc",              
            r"\.\./etc",                     
            r"(\.\./)+\.php",                
        ]

        endpoint = log["endpoint"]
        decoded_endpoint = urllib.parse.unquote(endpoint)

        for pattern in suspicious_patterns:
            if re.search(pattern, decoded_endpoint, re.IGNORECASE):
                self.raise_alert("LFI", log["ip"])
                break

    def raise_alert(self, alert_type, ip):
        timestamp = datetime.now().isoformat()
        alert = {
            "id": self.n,
            "timestamp": timestamp,
            "alert_type": alert_type,
            "ip": ip
        }
        self.n+=1
        print(f"\n[!] {alert}")

        log_path = "/logs/alerts.json"

        try:
            with open(log_path, "r") as f:
                alerts = json.load(f)
        except json.JSONDecodeError:
            alerts = []


        alerts.append(alert)

        with open(log_path, "w") as f:
            json.dump(alerts, f, indent=4)
