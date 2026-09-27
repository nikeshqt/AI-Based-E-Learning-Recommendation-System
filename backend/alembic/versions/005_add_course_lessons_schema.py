"""005_add_course_lessons_schema

Revision ID: 005_add_course_lessons_schema
Revises: 004_enhance_learning_path_schema
Create Date: 2026-09-27 23:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '005_add_course_lessons_schema'
down_revision = '004_enhance_learning_path_schema'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create course_modules table
    op.create_table(
        'course_modules',
        sa.Column('module_id', sa.String(), nullable=False, primary_key=True),
        sa.Column('course_id', sa.String(), sa.ForeignKey('courses.course_id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('order_index', sa.Integer(), nullable=True, server_default='1'),
    )
    op.create_index('ix_course_modules_course_id', 'course_modules', ['course_id'])

    # Create course_lessons table
    op.create_table(
        'course_lessons',
        sa.Column('lesson_id', sa.String(), nullable=False, primary_key=True),
        sa.Column('module_id', sa.String(), sa.ForeignKey('course_modules.module_id', ondelete='CASCADE'), nullable=False),
        sa.Column('course_id', sa.String(), sa.ForeignKey('courses.course_id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=True, server_default='1'),
        sa.Column('estimated_duration_minutes', sa.Integer(), nullable=True, server_default='15'),
    )
    op.create_index('ix_course_lessons_course_id', 'course_lessons', ['course_id'])
    op.create_index('ix_course_lessons_module_id', 'course_lessons', ['module_id'])

    # Enhance enrollments table
    op.add_column('enrollments', sa.Column('progress_percentage', sa.Float(), nullable=True, server_default='0.0'))
    op.add_column('enrollments', sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column('enrollments', 'completed_at')
    op.drop_column('enrollments', 'progress_percentage')
    op.drop_index('ix_course_lessons_module_id', table_name='course_lessons')
    op.drop_index('ix_course_lessons_course_id', table_name='course_lessons')
    op.drop_table('course_lessons')
    op.drop_index('ix_course_modules_course_id', table_name='course_modules')
    op.drop_table('course_modules')
