FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir pandas watchdog streamlit

RUN chmod +x collector/collect.sh \
    && chmod +x attack_simulator.sh \
    && chmod +x alerting/block_ip.sh

CMD ["tail", "-f", "/dev/null"]
