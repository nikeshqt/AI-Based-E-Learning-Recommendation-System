"""006_add_admin_and_audit_schema

Revision ID: 006_add_admin_and_audit_schema
Revises: 005_add_course_lessons_schema
Create Date: 2026-09-29 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '006_add_admin_and_audit_schema'
down_revision = '005_add_course_lessons_schema'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add role, is_active, and last_login to users table
    op.add_column('users', sa.Column('role', sa.String(), nullable=False, server_default='student'))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()))
    op.add_column('users', sa.Column('last_login', sa.DateTime(timezone=True), nullable=True))

    # Add is_active to courses table
    op.add_column('courses', sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()))

    # Create admin_activity_logs table
    op.create_table(
        'admin_activity_logs',
        sa.Column('log_id', sa.String(), nullable=False, primary_key=True),
        sa.Column('admin_id', sa.String(), sa.ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('target_type', sa.String(), nullable=True),
        sa.Column('target_id', sa.String(), nullable=True),
        sa.Column('details', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('ix_admin_activity_logs_admin_id', 'admin_activity_logs', ['admin_id'])
    op.create_index('ix_admin_activity_logs_action', 'admin_activity_logs', ['action'])
    op.create_index('ix_admin_activity_logs_created_at', 'admin_activity_logs', ['created_at'])


def downgrade() -> None:
    op.drop_index('ix_admin_activity_logs_created_at', table_name='admin_activity_logs')
    op.drop_index('ix_admin_activity_logs_action', table_name='admin_activity_logs')
    op.drop_index('ix_admin_activity_logs_admin_id', table_name='admin_activity_logs')
    op.drop_table('admin_activity_logs')
    op.drop_column('courses', 'is_active')
    op.drop_column('users', 'last_login')
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'role')
