class IpAccessPolicy:
    _instance = None  # variable containing the only one instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_data()
        return cls._instance

    def _init_data(self):
        self.blacklist_path = "/app/access_control/blacklist.txt"
        self.rate_limit_path = "/app/access_control/rate_limit.txt"

        self._blacklisted_ips = self._load_file(self.blacklist_path)
        self._rate_limited_ips = self._load_file(self.rate_limit_path)

    # ---------- CHECKS ----------

    def is_blacklisted(self, ip):
        return ip in self._blacklisted_ips

    def is_rate_limited(self, ip):
        return ip in self._rate_limited_ips

    # ---------- LOAD ----------

    def _load_file(self, path):
        try:
            with open(path) as f:
                return set(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            return set()

    # ---------- BLACKLIST ----------

    def block_address(self, ip):
        if ip not in self._blacklisted_ips:
            self._blacklisted_ips.add(ip)
            with open(self.blacklist_path, "a") as f:
                f.write(ip + "\n")

    def unblock_address(self, ip):
        if ip in self._blacklisted_ips:
            self._blacklisted_ips.remove(ip)
            self._rewrite_file(self.blacklist_path, self._blacklisted_ips)

    # ---------- RATE LIMIT ----------

    def apply_rate_limit(self, ip):
        if ip not in self._rate_limited_ips:
            self._rate_limited_ips.add(ip)
            with open(self.rate_limit_path, "a") as f:
                f.write(ip + "\n")

    def remove_rate_limit(self, ip):
        if ip in self._rate_limited_ips:
            self._rate_limited_ips.remove(ip)
            self._rewrite_file(self.rate_limit_path, self._rate_limited_ips)

    # ---------- SAVE ----------

    def _rewrite_file(self, path, data_set):
        with open(path, "w") as f:
            for ip in data_set:
                f.write(ip + "\n")
