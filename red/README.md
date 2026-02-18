# Attack Simulation Toolkit
### Overview

This directory provides a set of Bash scripts designed to simulate common web attack patterns against the Nginx service and normal HTTP traffic. The primary purpose of these scripts is:

- Security testing

- Log generation for SIEM testing

- Blue team / red team exercises

- Detection rule validation

- Lab environments and training

## 1. Blacklisted IP simulation


Simulates a request coming from a blacklisted IP address.

#### Usage

```
black_list.sh [IP]
```
If no IP is provided, it is set to ```1.2.3.4``` by default

## 2. Brute force simulation

Simulates a brute-force attack by sending multiple login attempts from the same IP.

#### Usage
```
brute_force.sh [IP]
```
If no IP is provided, a random one is generated.

## 3. Local file inclusion (LFI)

Simulates a Local File Inclusion attack. Sends a request to: ```/index.php?page=../../../../etc/passwd```

#### Usage
```
lfi.sh [IP]
```
If no IP is provided, a random one is generated.

## 4. Network scan simulation

Simulates a network reconnaissance scan using nmap.

#### Usage
```
scan.sh
```

## 5. SQL injection simulation

Simulates a SQL injection attempt. Sends a request to: ```/index.php?id=1' OR '1'='1```

#### Usage
```
sqli.sh [IP]
```
If no IP is provided, a random one is generated.


## Run all attacks at once

This script orchestrates attack execution.

#### Usage

Run all attacks:
```
./run_all.sh   # assuming you are inside /app directory
```

Run specific attacks:
```
./run_all.sh --brute
./run_all.sh --lfi
./run_all.sh --scan
./run_all.sh --sqli
./run_all.sh --black
```

If no flags are provided, all attacks are executed sequentially.

## Normal traffic generator

Generates continuous benign traffic to simulate real users.

#### Usage
````
./normal_traffic.sh   # assuming you are inside /app directory
````

Stop with:
```
CTRL+C
```
#### Behavior

Randomly selects endpoints:

```/```, ```/login```, ```/index.php```, ```/about```, ```/contact```, ```/products```

Generates random IPv4 addresses. Sleeps between 0.5 and 3 seconds between requests. Runs forever unless stopped by the user.
