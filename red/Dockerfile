FROM debian:bullseye-slim

WORKDIR /app

COPY . .

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl nmap bash \
    && rm -rf /var/lib/apt/lists/* \
    && chmod +x run_all.sh traffic_simulator.sh attacks/*.sh \
    && useradd -m -s /bin/bash red_team \
    && chown -R red_team:red_team /app

ENV PATH="/app/attacks:${PATH}"

USER red_team

CMD ["tail", "-f", "/dev/null"]
