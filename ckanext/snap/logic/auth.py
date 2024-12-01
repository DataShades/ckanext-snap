from __future__ import annotations

from typing import Any

from ckan import authz, types


def snap_snapshot_create(context: types.Context, data_dict: dict[str, Any]):
    """Only sysadmin can create snapshot."""
    return authz.is_authorized("sysadmin", context, data_dict)


def snap_snapshot_update(context: types.Context, data_dict: dict[str, Any]):
    """Only sysadmin can update snapshot."""
    return authz.is_authorized("sysadmin", context, data_dict)


def snap_snapshot_delete(context: types.Context, data_dict: dict[str, Any]):
    """Only sysadmin can delete snapshot."""
    return authz.is_authorized("sysadmin", context, data_dict)


def snap_snapshot_show(context: types.Context, data_dict: dict[str, Any]):
    """Only sysadmin can show snapshot."""
    return authz.is_authorized("sysadmin", context, data_dict)


def snap_snapshot_list(context: types.Context, data_dict: dict[str, Any]):
    """Only sysadmin can list snapshot."""
    return authz.is_authorized("sysadmin", context, data_dict)


def snap_snapshot_restore(context: types.Context, data_dict: dict[str, Any]):
    """Only sysadmin can restore snapshot."""
    return authz.is_authorized("sysadmin", context, data_dict)
