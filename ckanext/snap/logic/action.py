from __future__ import annotations

from typing import Any
import sqlalchemy as sa
import ckan.plugins.toolkit as tk
from ckan.logic import validate
from ckan.types import Context

from ckanext.snap.model import Snapshot
from ckanext.snap import config
from . import schema


@validate(schema.snapshot_create)
def snap_snapshot_create(context: Context, data_dict: dict[str, Any]):
    """Create snapshot object.

    Args:
        target_type (str): aliquam erat volutpat
        target_id: (str): nullam tempus
        data (dict[str, Any], optional): aliquam feugiat tellus ut neque

    Returns:
        details of the new snapshot object
    """
    tk.check_access("snap_snapshot_create", context, data_dict)

    sess = context["session"]
    obj = Snapshot(
        target_type=data_dict["target_type"],
        target_id=data_dict["target_id"],
        data=data_dict["data"],
    )
    sess.add(obj)
    sess.commit()

    return obj.dictize(context)


@validate(schema.snapshot_delete)
def snap_snapshot_delete(context: Context, data_dict: dict[str, Any]):
    """Delete snapshot object.

    Args:
        id: (str): nullam tempus

    Returns:
        details of the removed snapshot object
    """
    tk.check_access("snap_snapshot_delete", context, data_dict)

    sess = context["session"]
    obj = sess.get(Snapshot, data_dict["id"])
    if not obj:
        raise tk.ObjectNotFound("snapshot")

    sess.delete(obj)
    sess.commit()

    return obj.dictize(context)


@validate(schema.snapshot_show)
def snap_snapshot_show(context: Context, data_dict: dict[str, Any]):
    """Show snapshot object.

    Args:
        id: (str): nullam tempus

    Returns:
        details of the snapshot object
    """
    tk.check_access("snap_snapshot_show", context, data_dict)

    sess = context["session"]
    obj = sess.get(Snapshot, data_dict["id"])
    if not obj:
        raise tk.ObjectNotFound("snapshot")

    return obj.dictize(context)


@validate(schema.snapshot_list)
def snap_snapshot_list(context: Context, data_dict: dict[str, Any]) -> dict[str, Any]:
    """List snapshot objects.

    Args:
        target_type: (str): nullam tempus
        target_id: (str): nullam tempus
        rows: (int): nullam tempus
        start: (int): nullam tempus

    Returns:
        collection of snapshot objects
    """
    tk.check_access("snap_snapshot_show", context, data_dict)

    sess = context["session"]

    stmt = Snapshot.by_target(data_dict["target_type"], data_dict["target_id"])

    total_stmt = stmt.with_only_columns(sa.func.count())

    return {
        "count": sess.scalar(total_stmt),
        "results": [
            obj.dictize(context)
            for obj in sess.scalars(
                stmt.limit(data_dict["rows"])
                .offset(data_dict["start"])
                .order_by(Snapshot.created_at.desc())
            )
        ],
    }


@validate(schema.snapshot_restore)
def snap_snapshot_restore(context: Context, data_dict: dict[str, Any]):
    """Restore snapshot object.

    Args:
        id: (str): nullam tempus

    Returns:
        details of the restored object
    """
    tk.check_access("snap_snapshot_restore", context, data_dict)

    sess = context["session"]
    obj = sess.get(Snapshot, data_dict["id"])
    if not obj:
        raise tk.ObjectNotFound("snapshot")

    action_name = config.restorable_types().get(obj.target_type)
    if not action_name:
        raise tk.ValidationError(
            {"id": [f"Target type {obj.target_type} does not support restoration"]}
        )

    return tk.get_action(action_name)(tk.fresh_context(context), obj.data)
