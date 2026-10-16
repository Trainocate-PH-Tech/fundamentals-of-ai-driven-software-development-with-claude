"""Category and Issue persistence; existing users are preserved."""
from alembic import op
import sqlalchemy as sa

revision = "0003_tracker"
down_revision = "0002_add_role_to_users"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("categories",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("length(trim(name)) > 0", name="ck_category_nonblank"))
    op.create_index("uq_categories_name_lower", "categories", [sa.text("lower(name)")], unique=True)
    op.create_table("issues",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("priority", sa.String(20), nullable=False),
        sa.Column("category_id", sa.String(36), sa.ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("assigned_user_id", sa.String(36), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("status IN ('open','in_progress','resolved','closed')", name="ck_issue_status"),
        sa.CheckConstraint("priority IN ('low','medium','high','critical')", name="ck_issue_priority"),
        sa.CheckConstraint("length(trim(title)) > 0", name="ck_issue_nonblank"))
    op.create_index("ix_issues_category_id", "issues", ["category_id"])
    op.create_index("ix_issues_assigned_user_id", "issues", ["assigned_user_id"])


def downgrade():
    op.drop_table("issues")
    op.drop_table("categories")
