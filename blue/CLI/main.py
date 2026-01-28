#!/usr/bin/env python3

import sys
from pathlib import Path

# dodaj katalog nadrzędny do sys.path, żeby Python znalazł ip_access_policy.py
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Teraz import działa
from ip_access_policy import IpAccessPolicy

import click

ip_policy = IpAccessPolicy()  # singleton

@click.group()
def soclog():
    """SOC log management CLI"""
    pass

# ---------- BLACKLIST ----------
@soclog.group()
def blacklist():
    """Manage blacklisted IPs"""
    pass

@blacklist.command()
@click.argument("ip")
def block(ip):
    """Add IP to blacklist"""
    ip_policy.block_address(ip)
    click.echo(f"Blocked IP: {ip}")

@blacklist.command()
@click.argument("ip")
def unblock(ip):
    """Remove IP from blacklist"""
    ip_policy.unblock_address(ip)
    click.echo(f"Unblocked IP: {ip}")

@blacklist.command("list")
def list_blacklist():
    """List all blacklisted IPs"""
    for ip in sorted(ip_policy._blacklisted_ips):
        click.echo(ip)

# ---------- RATE LIMIT ----------
@soclog.group()
def rate_limit():
    """Manage rate-limited IPs"""
    pass

@rate_limit.command("apply")
@click.argument("ip")
def apply(ip):
    """Apply rate limit to IP"""
    ip_policy.apply_rate_limit(ip)
    click.echo(f"Rate limit applied to: {ip}")

@rate_limit.command("remove")
@click.argument("ip")
def remove(ip):
    """Remove rate limit from IP"""
    ip_policy.remove_rate_limit(ip)
    click.echo(f"Rate limit removed from: {ip}")

@rate_limit.command("list")
def list_rate_limited():
    """List all rate-limited IPs"""
    for ip in sorted(ip_policy._rate_limited_ips):
        click.echo(ip)

# ---------- ALERTS / MONITOR ----------
@soclog.command()
@click.option("--ip", help="Filter by IP")
@click.option("--type", "alert_type", help="Filter by alert type")
@click.option("--since", help="Start time (ISO format)")
@click.option("--until", help="End time (ISO format)")
def monitor(ip, alert_type, since, until):
    """Monitor alerts / events"""
    # Tutaj w MVP wypiszemy wszystkie alerty z pliku JSON
    import json
    from pathlib import Path

    log_path = Path("alerts.json")
    if not log_path.exists():
        click.echo("No alerts found.")
        return

    with open(log_path) as f:
        alerts = json.load(f)

    # filtrowanie
    filtered = []
    for a in alerts:
        if ip and a.get("ip") != ip:
            continue
        if alert_type and a.get("alert_type") != alert_type:
            continue
        # opcjonalnie filtrowanie po czasie
        filtered.append(a)

    if not filtered:
        click.echo("No matching alerts.")
        return

    for a in filtered:
        click.echo(a)

if __name__ == "__main__":
    soclog()
