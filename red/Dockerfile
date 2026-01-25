FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN apt-get update \
    && apt-get install -y curl \
    && apt-get clean \
    && apt-get install -y nmap \
    && rm -rf /var/lib/apt/lists/*

RUN chmod +x attack_all.sh \
    && chmod +x traffic_simulator.sh \
    && chmod +x attacks/*.sh

CMD ["tail", "-f", "/dev/null"]