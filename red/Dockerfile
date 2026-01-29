FROM debian:bullseye-slim

WORKDIR /app

COPY . .

RUN apt-get update \
    && apt-get install -y curl nmap bash \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN chmod +x run_all.sh \
    && chmod +x traffic_simulator.sh \
    && chmod +x attacks/*.sh

CMD ["tail", "-f", "/dev/null"]
