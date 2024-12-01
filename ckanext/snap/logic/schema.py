from __future__ import annotations

from ckan import types
from ckan.logic.schema import validator_args


@validator_args
def snapshot_create(
    not_empty: types.Validator,
    unicode_safe: types.Validator,
    not_missing: types.Validator,
    ignore_missing: types.Validator,
    convert_to_json_if_string: types.Validator,
    dict_only: types.Validator,
) -> types.Schema:
    """Schema for snap_snapshot_create action."""
    return {
        "target_type": [not_empty, unicode_safe],
        "target_id": [not_empty, unicode_safe],
        "data": [not_missing, convert_to_json_if_string, dict_only],
        "name": [ignore_missing, unicode_safe],
    }


@validator_args
def snapshot_delete(
    not_empty: types.Validator,
    unicode_safe: types.Validator,
) -> types.Schema:
    """Schema for snap_snapshot_delete action."""
    return {
        "id": [not_empty, unicode_safe],
    }


@validator_args
def snapshot_update(
    convert_to_json_if_string: types.Validator,
    dict_only: types.Validator,
    not_empty: types.Validator,
    unicode_safe: types.Validator,
    not_missing: types.Validator,
    ignore_missing: types.Validator,
) -> types.Schema:
    """Schema for snap_snapshot_delete action."""
    return {
        "id": [not_empty, unicode_safe],
        "name": [ignore_missing, unicode_safe],
        "data": [ignore_missing, convert_to_json_if_string, dict_only],
    }


@validator_args
def snapshot_show(
    not_empty: types.Validator,
    unicode_safe: types.Validator,
) -> types.Schema:
    """Schema for snap_snapshot_show action."""
    return {
        "id": [not_empty, unicode_safe],
    }


@validator_args
def snapshot_list(
    not_empty: types.Validator,
    unicode_safe: types.Validator,
    int_validator: types.Validator,
    default: types.ValidatorFactory,
) -> types.Schema:
    """Schema for snap_snapshot_list action."""
    return {
        "target_type": [not_empty, unicode_safe],
        "target_id": [not_empty, unicode_safe],
        "start": [default(0), int_validator],
        "rows": [default(10), int_validator],
    }


@validator_args
def snapshot_restore(
    not_empty: types.Validator,
    unicode_safe: types.Validator,
) -> types.Schema:
    """Schema for snap_snapshot_restore action."""
    return {
        "id": [not_empty, unicode_safe],
    }
