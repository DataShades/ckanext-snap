from __future__ import annotations

import copy
import datetime
from typing import Any

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped

from ckan.lib.dictization import table_dictize
from ckan.model.types import make_uuid

from .base import Base, now


class Snapshot(Base):  # type: ignore
    """Model with details or something."""

    __table__ = sa.Table(
        "snap_snapshot",
        Base.metadata,
        sa.Column("id", sa.UnicodeText, primary_key=True, default=make_uuid),
        sa.Column("target_type", sa.UnicodeText, nullable=False),
        sa.Column("target_id", sa.UnicodeText, nullable=False, index=True),
        sa.Column("created_at", sa.DateTime(True), nullable=False, default=now),
        sa.Column("name", sa.UnicodeText, nullable=False, default=now),
        sa.Column("data", JSONB, default=dict),
        sa.Column("plugin_data", JSONB, default=dict),
    )

    id: Mapped[str]

    target_type: Mapped[str]
    target_id: Mapped[str]
    created_at: Mapped[datetime.datetime]
    name: Mapped[str]

    data: Mapped[dict[str, Any]]
    plugin_data: Mapped[dict[str, Any]]

    def dictize(self, context: Any) -> dict[str, Any]:
        result = table_dictize(self, context)

        result["data"] = copy.deepcopy(result["data"])

        plugin_data = result.pop("plugin_data")
        if context.get("include_plugin_data"):
            result["plugin_data"] = copy.deepcopy(plugin_data)

        return result


    @classmethod
    def by_target(cls, target_type: str, target_id: str) -> sa.sql.Select:
        return sa.select(cls).where(
            cls.target_id == target_id,
            cls.target_type == target_type,
        )

