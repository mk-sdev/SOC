FROM python:3.12-slim

WORKDIR /app

COPY /soc_container .

RUN apt-get update \
    && apt-get install -y curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pandas watchdog streamlit

RUN chmod +x collector/collect.sh \
    && chmod +x attack_simulator.sh \
    && chmod +x alerting/block_ip.sh \
    && chmod +x watcher.py

CMD ["tail", "-f", "/dev/null"]
