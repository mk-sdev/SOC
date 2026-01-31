import click, json
from datetime import datetime
from pathlib import Path
from alert_viewer import alert_viewer

def inspect(ip, type, since, until, newest, status, id):
    '''
    Filters the alerts
    '''
    log_path = Path("/logs/alerts.json")
    if not log_path.exists():
        click.echo("No alerts found.")
        return

    try:
        with open(log_path) as f:
            alerts = json.load(f)
    except Exception as e:
        click.echo(f"There are no logs to inspect")
        return

    # convert to datetime objects for filtering by time range
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

    # filtering
    filtered = []
    for a in alerts:
        if "closed" in a and status == 'opened':
            continue

        if "closed" not in a and status == 'closed':
            continue

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

    # if log_id is provided, filter for only that alert
    if id is not None:
        filtered = [a for a in filtered if str(a.get("id")) == id]
        if not filtered:
            click.echo(f"No alert found with ID: {id}")
            return

    if not filtered:
        click.echo("No matching alerts.")
        return

    # sorting
    if newest:
        filtered = sorted(filtered, key=lambda x: datetime.fromisoformat(x.get("timestamp")), reverse=True)
    else:
        filtered = sorted(filtered, key=lambda x: datetime.fromisoformat(x.get("timestamp")))

    alert_viewer(filtered)


