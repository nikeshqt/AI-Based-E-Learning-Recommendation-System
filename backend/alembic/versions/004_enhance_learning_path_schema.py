"""004_enhance_learning_path_schema

Revision ID: 004_enhance_learning_path_schema
Revises: 003_add_skill_gap_schema
Create Date: 2026-09-27 18:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '004_enhance_learning_path_schema'
down_revision = '003_add_skill_gap_schema'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enhance learning_paths table
    op.add_column('learning_paths', sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'))
    op.add_column('learning_paths', sa.Column('overall_readiness', sa.Float(), nullable=True, server_default='0.0'))
    op.add_column('learning_paths', sa.Column('total_duration_hours', sa.Float(), nullable=True, server_default='0.0'))
    op.add_column('learning_paths', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
    op.create_index('ix_learning_paths_is_active', 'learning_paths', ['is_active'])

    # Enhance learning_path_items table
    op.add_column('learning_path_items', sa.Column('order_index', sa.Integer(), nullable=True, server_default='1'))
    op.add_column('learning_path_items', sa.Column('stage_name', sa.String(), nullable=True))
    op.add_column('learning_path_items', sa.Column('stage_description', sa.Text(), nullable=True))
    op.add_column('learning_path_items', sa.Column('target_skill', sa.String(), nullable=True))
    op.add_column('learning_path_items', sa.Column('skill_gap', sa.Float(), nullable=True, server_default='0.0'))
    op.add_column('learning_path_items', sa.Column('current_mastery', sa.Float(), nullable=True, server_default='0.0'))
    op.add_column('learning_path_items', sa.Column('target_mastery', sa.Float(), nullable=True, server_default='0.0'))
    op.add_column('learning_path_items', sa.Column('priority_score', sa.Float(), nullable=True, server_default='0.0'))
    op.add_column('learning_path_items', sa.Column('reason', sa.Text(), nullable=True))
    op.add_column('learning_path_items', sa.Column('status', sa.String(), nullable=True, server_default='AVAILABLE'))
    op.add_column('learning_path_items', sa.Column('estimated_duration_hours', sa.Float(), nullable=True, server_default='0.0'))


def downgrade() -> None:
    op.drop_index('ix_learning_paths_is_active', table_name='learning_paths')
    op.drop_column('learning_paths', 'created_at')
    op.drop_column('learning_paths', 'total_duration_hours')
    op.drop_column('learning_paths', 'overall_readiness')
    op.drop_column('learning_paths', 'is_active')

    op.drop_column('learning_path_items', 'estimated_duration_hours')
    op.drop_column('learning_path_items', 'status')
    op.drop_column('learning_path_items', 'reason')
    op.drop_column('learning_path_items', 'priority_score')
    op.drop_column('learning_path_items', 'target_mastery')
    op.drop_column('learning_path_items', 'current_mastery')
    op.drop_column('learning_path_items', 'skill_gap')
    op.drop_column('learning_path_items', 'target_skill')
    op.drop_column('learning_path_items', 'stage_description')
    op.drop_column('learning_path_items', 'stage_name')
    op.drop_column('learning_path_items', 'order_index')
