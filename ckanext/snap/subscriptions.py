from __future__ import annotations
from typing import Any
import ckan.plugins.toolkit as tk

from . import config


def make_snapshot_listener(sender: str, **kwargs: Any):
    info = config.tracked_actions().get(sender)
    if not info:
        return

    result = kwargs["result"]

    user = tk.get_action("get_site_user")({"ignore_auth": True}, {})

    tk.get_action("snap_snapshot_create")(
        {
            "ignore_auth": True,
            "user": user["name"],
        },
        {
            "target_type": info["type"],
            "target_id": result[info["id"]],
            "data": result,
        },
    )
