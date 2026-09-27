"""002_add_skill_assessment_schema

Revision ID: 002_add_skill_assessment_schema
Revises: 001_initial_postgres_schema
Create Date: 2026-09-26 02:10:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '002_add_skill_assessment_schema'
down_revision = '001_initial_postgres_schema'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'assessment_questions',
        sa.Column('question_id', sa.String(), nullable=False, primary_key=True),
        sa.Column('assessment_id', sa.String(), sa.ForeignKey('assessments.assessment_id', ondelete='CASCADE'), nullable=False),
        sa.Column('domain', sa.String(), nullable=False),
        sa.Column('difficulty', sa.String(), nullable=False),
        sa.Column('prompt', sa.Text(), nullable=False),
        sa.Column('code_snippet', sa.Text(), nullable=True),
        sa.Column('options', sa.JSON(), nullable=False),
        sa.Column('correct_answer', sa.String(), nullable=False),
        sa.Column('explanation', sa.Text(), nullable=False),
        sa.Column('skill_measured', sa.String(), nullable=False),
    )
    op.create_index('ix_assessment_questions_domain', 'assessment_questions', ['domain'])
    op.create_index('ix_assessment_questions_skill_measured', 'assessment_questions', ['skill_measured'])

    op.create_table(
        'assessment_attempts',
        sa.Column('attempt_id', sa.String(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.String(), sa.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False),
        sa.Column('assessment_id', sa.String(), sa.ForeignKey('assessments.assessment_id', ondelete='CASCADE'), nullable=False),
        sa.Column('total_questions', sa.Integer(), nullable=False),
        sa.Column('answered_questions', sa.Integer(), nullable=False),
        sa.Column('correct_answers', sa.Integer(), nullable=False),
        sa.Column('incorrect_answers', sa.Integer(), nullable=False),
        sa.Column('overall_score', sa.Float(), nullable=False),
        sa.Column('topic_scores', sa.JSON(), nullable=False),
        sa.Column('difficulty_performance', sa.JSON(), nullable=False),
        sa.Column('skill_proficiency', sa.JSON(), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_assessment_attempts_user_id', 'assessment_attempts', ['user_id'])

    op.create_table(
        'assessment_answers',
        sa.Column('answer_id', sa.String(), nullable=False, primary_key=True),
        sa.Column('attempt_id', sa.String(), sa.ForeignKey('assessment_attempts.attempt_id', ondelete='CASCADE'), nullable=False),
        sa.Column('question_id', sa.String(), sa.ForeignKey('assessment_questions.question_id', ondelete='CASCADE'), nullable=False),
        sa.Column('selected_option', sa.String(), nullable=False),
        sa.Column('is_correct', sa.Boolean(), nullable=False),
    )
    op.create_index('ix_assessment_answers_attempt_id', 'assessment_answers', ['attempt_id'])


def downgrade() -> None:
    op.drop_table('assessment_answers')
    op.drop_table('assessment_attempts')
    op.drop_table('assessment_questions')
