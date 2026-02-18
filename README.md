# SOC Simulation Environment

#### This project simulates a basic Security Operations Center environment using Docker containers. It is designed to demonstrate offensive (red team) activity against a web service and defensive (blue team) detection and analysis.

### Architecture overview

The environment consists of three containers:

**Nginx container** – Generates access and error logs.

**Red team container** – Executes offensive scripts targeting the Nginx service.

**Blue team container** – Monitors logs, detects suspicious activity, and generates alerts.

The simulation models the full cycle:

- Attack execution

- Log generation

- Log collection and parsing

- Alert generation and analyst interaction

### Usage

Start the environment:
```
docker compose up
```

Access the blue team container:
```
docker exec -it blue bash
```

Access the red team container:
```
docker exec -it red bash
```

## Logs directory (/logs)

This directory is mounted as a shared volume between the Nginx and blue team containers.

#### Files

- ```access.log``` – Nginx access log.

- ```error.log``` – Nginx error log.

- ```collected.log``` – Copy of access.log used for analysis.

- ```parsed_logs.csv``` – Log entries extracted and structured in CSV format.

- ```alerts.json``` – Alerts generated out of suspicious entries from parsed_logs.csv, enriched with additional metadata. Intended for SOC analysts and may be modified during investigation workflows.

#### Maintenance

- ```clear_logs.sh``` – Script to clear all files in the ./logs directory.

- See ```/logs/clear_logs.sh``` for detailed documentation.

## Red team container (/red)

This container simulates attacker behavior against the Nginx service.

#### Included attack techniques

- Brute-force login attempts

- Local File Inclusion

- Network scanning using Nmap

- SQL injection attempts

It also includes:

- A script for executing all attack techniques at once

- A script for generating benign traffic to simulate legitimate user activity

For additional details, visit ```/red/README.md```

## Blue team container (/blue)

This container simulates defensive SOC operations.

#### Capabilities

- Background processes continuously monitor Nginx logs

- Logs are parsed and analyzed for indicators of suspicious behavior

- Alerts are generated and stored in structured format

#### SOC analyst CLI

The blue team container includes a ```soc``` CLI tool designed for SOC analysts. It enables:

- Managing access control lists

- Inspecting alert logs

- Closing alerts

- Marking alerts as false positives

- Commenting alerts

For detailed CLI documentation, see: ```/blue/CLI/README.md```

---

#### Known issues
- SQL injection detection mechanism doesn't work properly, probably due to incomplete regex rules.
- After log files are truncated, new entries do not appear; restarting blue container fixes this issue.