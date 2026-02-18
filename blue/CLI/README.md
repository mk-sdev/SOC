# SOC CLI Documentation

#### ```soc``` is a command-line interface for SOC analysts operating inside the blue container. It provides alert inspection capabilities and IP-based access control management.

### Overview
The CLI supports:
- IP blacklisting
- IP rate limiting
- Viewing controlled IPs
- Inspecting and managing alerts stored in /logs/alerts.json

The CLI is implemented using click library and operates directly on the shared alerts file.

### Usage
```
soc [COMMAND] [OPTIONS]
```

Get help:
```
soc --help
soc <command> --help
```
## IP Access Control Commands
These commands interact with the ```IpAccessPolicy ```component.

### Block an IP
```
soc block <ip>
```
Adds an IP address to the blacklist.
### Unblock an IP
```
soc unblock <ip>
```
Removes an IP address from the blacklist.

### Apply rate limiting
```
soc limit <ip>
```
Applies rate limiting to the specified IP.
### Remove rate limiting
```
soc unlimit <ip>
```
Removes rate limiting from the specified IP.
### Show controlled IPs
```
soc show [OPTIONS]
```
Options:
- ```-b, --blocked``` - show only blacklisted IPs
- ```-l, --limited``` - show only rate-limited IPs
- ```-a, --all``` - show both
If no option is provided, both lists are displayed.

## Alert inspection
### Basic usage
```
soc inspect
```
Displays interactive alert viewer (default: only opened alerts).
### Inspect specific alert
```
soc inspect <id>
```
Filters and opens a single alert by ID.
### Filtering Options
```
soc inspect [OPTIONS]
```
#### Filters
- ```--ip <ip>``` - filter by IP address

- ```--type <TYPE>``` - filter by alert type (```BLACKLISTED_IP```, ```BRUTE_FORCE```, ```SUSPICIOUS_USER_AGENT```, ```SQL_INJECTION```, ```LFI```)

- ```--since <date>``` - start time (e.g., ```2026-01-01``` or ```2026-01-01T00:00:00```)

- ```--until <date>``` - end time

- ```--status [opened|closed|all]``` - filter by alert status (default: opened)

- ```--newest``` - sort from newest to oldest

## Interactive alert viewer
After filtering, alerts are displayed in an interactive interface.

Each alert is shown as formatted JSON.
### Controls

| Key | Action |
|-----|--------|
| `c` | Mark alert as closed |
| `o` | Reopen alert |
| `m` | Add comment message |
| `f` | Mark as false positive (closes alert) |
| `t` | Mark as true positive (removes false positive flag) |
| `p` | Previous alert |
| `n` | Next alert |
| `g` | Go to alert by ID |
| `h` | Show help |
| `q` | Quit viewer |

### Example screenshot:
[![image.png](https://i.postimg.cc/1tyr8LGt/image.png)](https://postimg.cc/1gYqT7Yh)