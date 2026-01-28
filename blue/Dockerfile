FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN apt-get update \
    && apt-get install -y curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir watchdog click

RUN chmod +x collector/collect.sh \
    && chmod +x alerting/block_ip.sh \
    && chmod +x watcher.py \
    && chmod +x CLI/main.py \
    && chmod +x start.sh

RUN echo "alias soclog='python3 /app/CLI/main.py'" >> /root/.bashrc

CMD ["./start.sh"]
