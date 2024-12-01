"""Create something table.

Revision ID: cc1a832108c5
Revises:
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision = "cc1a832108c5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "snap_snapshot",
        sa.Column("id", sa.UnicodeText, primary_key=True),
        sa.Column("target_type", sa.UnicodeText, nullable=False),
        sa.Column("target_id", sa.UnicodeText, nullable=False, index=True),
        sa.Column("created_at", sa.DateTime(True), nullable=False, server_default=sa.func.now()),
        sa.Column("name", sa.UnicodeText, nullable=False, server_default=sa.func.now()),
        sa.Column("data", JSONB, server_default="{}"),
        sa.Column("plugin_data", JSONB, server_default="{}"),
        sa.Index("ix_snap_snapshot_created_at_desc", sa.column("created_at").desc()),
    )


def downgrade():
    op.drop_table("snap_snapshot")
