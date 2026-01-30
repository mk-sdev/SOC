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

RUN useradd -m -s /bin/bash red_team && \
    chown -R red_team:red_team /app

USER red_team

CMD ["tail", "-f", "/dev/null"]
