"""Config getters of snap plugin."""

from __future__ import annotations

import functools

import ckan.plugins.toolkit as tk

TRACKED_ACTIONS = "ckanext.snap.tracked_actions"
RESTORABLE_TYPES = "ckanext.snap.restorable_types"


def tracked_actions() -> dict[str, dict[str, str]]:
    """Actions that automatically create a snapshot for their result."""
    return _parse_actions(tuple(tk.config[TRACKED_ACTIONS]))


def restorable_types() -> dict[str, str]:
    """Types of snapshot target than can restore their previous state."""
    return _parse_types(tuple(tk.config[RESTORABLE_TYPES]))


@functools.lru_cache(1)
def _parse_actions(items: list[str]):
    result: dict[str, dict[str, str]] = {}

    for item in items:
        action, target_type, target_id = (item.split(":") + ["", ""])[:3]

        if not target_type:
            target_type = action.rsplit("_", 1)[0]

        if not target_id:
            target_id = "id"

        result[action] = {"type": target_type, "id": target_id}

    return result


@functools.lru_cache(1)
def _parse_types(items: list[str]):
    result: dict[str, str] = {}

    for item in items:
        target_type, action = (item.split(":") + [""])[:2]

        if not action:
            action = target_type + "_update"

        result[target_type] = action

    return result
