from datetime import UTC, datetime

def time_ago(dt: datetime):
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)

    now = datetime.now(UTC)
    diff = now - dt
    seconds = diff.total_seconds()

    if seconds < 60:
        return "Just now"

    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"

    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"

    elif seconds < 604800:
        days = int(seconds // 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"

    return dt.strftime("%d %b %Y")