"""Week helpers shared across screens and the API client.

Goals and analyses are keyed by ``week_start_date``, which must always be the
Monday of the week. These helpers keep that math (and its display formatting) in
one place instead of being re-derived per screen.
"""

from datetime import date, timedelta


def monday_of(d: date) -> date:
    """Return the Monday of the week containing ``d``."""
    return d - timedelta(days=d.weekday())


def week_range_text(monday: date) -> str:
    """Human-readable Mon–Sun range, e.g. 'Jul 14 – Jul 20, 2026'."""
    end = monday + timedelta(days=6)
    s = monday.strftime('%b %d').replace(' 0', ' ')
    e = end.strftime('%b %d, %Y').replace(' 0', ' ')
    return f"{s} – {e}"
