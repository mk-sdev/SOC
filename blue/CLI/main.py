#!/usr/bin/env python3

import sys
from pathlib import Path

import json
from datetime import datetime

# add parent directory so that Python could find ip_access_policy.py
sys.path.append(str(Path(__file__).resolve().parent.parent))

from ip_access_policy import IpAccessPolicy

import click

ip_policy = IpAccessPolicy()  # singleton

@click.group()
def soclog():
    """SOC log management CLI"""
    pass

# ---------- BLACKLIST ----------
@soclog.command(help="Add a specified IP address to the black list.")
@click.argument("ip")
def block(ip):
    ip_policy.block_address(ip)
    click.echo(f"Blocked IP: {ip}")
    
@soclog.command(help="Remove a specified IP address from the black list.")
@click.argument("ip")
def unblock(ip):
    ip_policy.unblock_address(ip)
    click.echo(f"Unblocked IP: {ip}")

# ---------- RATE LIMIT ----------
@soclog.command(help="Apply rate limiting to a specified IP address.")
@click.argument("ip")
def limit(ip):
    ip_policy.apply_rate_limit(ip)
    click.echo(f"Rate limit applied to: {ip}")

@soclog.command(help="Remove rate limiting to a specified IP address.")
@click.argument("ip")
def unlimit(ip):
    ip_policy.remove_rate_limit(ip)
    click.echo(f"Rate limit removed from {ip}")

# ------------- SHOW IPS --------------
@soclog.command(help='Show the list of black-listed or/and rate-limited IP addresses. If no option provided, shows both of them.')
@click.option('-b','--blocked', is_flag=True)
@click.option('-l','--limited', is_flag=True)
@click.option('-a','--all', is_flag=True)
def show(blocked, limited, all):
    if not (blocked or limited or all):
        all = True
    if blocked or all:
        click.echo("BLACK LISTED IP ADDRESSES:")
        for ip in sorted(ip_policy._blacklisted_ips):
            click.echo(ip)
    if limited or all:
        click.echo("RATE LIMITED IP ADDRESSES:")
        for ip in sorted(ip_policy._rate_limited_ips):
            click.echo(ip)


# ---------- ALERTS / MONITOR ----------
@soclog.command()
@click.option("--ip", help="Filter by IP")
@click.option("--type", type=click.Choice(["BLACKLISTED_IP", "BRUTE_FORCE", "SUSPICIOUS_USER_AGENT", "SQL_INJECTION", "LFI"]), help="Filter by alert type")
@click.option("--since", help="Start time, e.g., 2026-01-01 or 2026-01-01T00:00:00")
@click.option("--until", help="End time, e.g., 2026-01-01 or 2026-01-01T23:59:59")
@click.option("--newest", is_flag=True, help="Sort from the newest")
@click.argument("id", required=False, default=None)
def inspect(ip, type, since, until, newest, id):
    """Monitor alerts / events. You can provide a log ID to inspect a single alert."""
    log_path = Path("/logs/alerts.json")
    if not log_path.exists():
        click.echo("No alerts found.")
        return

    try:
        with open(log_path) as f:
            alerts = json.load(f)
    except Exception as e:
        click.echo(f"Error reading alerts file: {e}")
        return

    # Convert to datetime objects for filtering by time range
    try:
        if since:
            if "T" not in since:
                since = f"{since}T00:00:00"
            since = datetime.fromisoformat(since)
        if until:
            if "T" not in until:
                until = f"{until}T23:59:59"
            until = datetime.fromisoformat(until)
    except ValueError as e:
        click.echo(f"Invalid time format: {e}")
        return

    # Filtering
    filtered = []
    for a in alerts:
        # Filter by IP
        if ip and a.get("ip") != ip:
            continue

        # Filter by alert type
        if type and a.get("alert_type") != type:
            continue

        # Filter by time
        try:
            log_time = datetime.fromisoformat(a.get("timestamp"))
        except (ValueError, TypeError):
            continue

        if since and log_time < since:
            continue
        if until and log_time > until:
            continue

        filtered.append(a)

    # If log_id is provided, filter for only that alert
    if id is not None:
        filtered = [a for a in filtered if str(a.get("id")) == id]
        if not filtered:
            click.echo(f"No alert found with ID: {id}")
            return

    if not filtered:
        click.echo("No matching alerts.")
        return

    # Sorting
    if newest:
        filtered = sorted(filtered, key=lambda x: datetime.fromisoformat(x.get("timestamp")), reverse=True)
    else:
        filtered = sorted(filtered, key=lambda x: datetime.fromisoformat(x.get("timestamp")))

    # Display results
    for a in filtered:
        click.echo(json.dumps(a, indent=2))


if __name__ == "__main__":
    soclog()
