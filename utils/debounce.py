"""Debounce helper for UI event handlers.

On Android, a single physical tap dispatches a button's ``on_release`` twice
(~1 ms apart). For toggles this cancels itself out, and for actions it fires
duplicate API calls / double navigation. ``@debounce`` collapses repeat calls
that land within a short window into a single call.
"""

from functools import wraps
from time import time

# Two real taps are never closer than this; a double-fire is ~1 ms apart.
DEFAULT_WAIT = 0.15


def debounce(wait: float = DEFAULT_WAIT):
    """Ignore repeat calls of a bound method within ``wait`` seconds.

    The last-call timestamp is stored per instance and per method name, so
    different widgets and different handlers don't interfere with each other.
    Intended for Kivy ``on_release`` / ``on_press`` handlers.
    """

    def decorator(func):
        attr = f"_debounce_ts_{func.__name__}"

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            now = time()
            if now - getattr(self, attr, 0.0) < wait:
                return None
            setattr(self, attr, now)
            return func(self, *args, **kwargs)

        return wrapper

    return decorator
