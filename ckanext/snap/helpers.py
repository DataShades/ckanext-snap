"""Template helpers of the snap plugin.

All non-private functions defined here are registered inside `tk.h` collection.
"""

from __future__ import annotations


def snap_hello() -> str:
    """Greet the user.

    Returns:
        greeting with the plugin name.
    """
    return "Hello, snap!"
