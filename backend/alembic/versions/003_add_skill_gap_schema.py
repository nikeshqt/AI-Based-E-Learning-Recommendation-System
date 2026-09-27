"""003_add_skill_gap_schema

Revision ID: 003_add_skill_gap_schema
Revises: 002_add_skill_assessment_schema
Create Date: 2026-09-26 02:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '003_add_skill_gap_schema'
down_revision = '002_add_skill_assessment_schema'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'goal_required_skills',
        sa.Column('id', sa.String(), nullable=False, primary_key=True),
        sa.Column('goal_name', sa.String(), nullable=False),
        sa.Column('skill_name', sa.String(), nullable=False),
        sa.Column('target_mastery', sa.Float(), nullable=False),
        sa.Column('importance', sa.Float(), nullable=True, default=1.0),
        sa.Column('is_prerequisite', sa.Boolean(), nullable=True, default=False),
    )
    op.create_index('ix_goal_required_skills_goal_name', 'goal_required_skills', ['goal_name'])
    op.create_index('ix_goal_required_skills_skill_name', 'goal_required_skills', ['skill_name'])


def downgrade() -> None:
    op.drop_table('goal_required_skills')
