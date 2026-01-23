FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN apt-get update \
    && apt-get install -y curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pandas watchdog

RUN chmod +x collector/collect.sh \
    && chmod +x alerting/block_ip.sh \
    && chmod +x watcher.py \
    && chmod +x start.sh

CMD ["./start.sh"]
