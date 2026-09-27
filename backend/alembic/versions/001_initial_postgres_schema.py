"""001_initial_postgres_schema

Revision ID: 001_initial_postgres_schema
Revises: 
Create Date: 2026-09-26 01:20:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '001_initial_postgres_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Users & Profiles
    op.create_table(
        'users',
        sa.Column('user_id', sa.String(), nullable=False, primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_table(
        'profiles',
        sa.Column('profile_id', sa.String(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.String(), sa.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('learning_goal', sa.String(), nullable=False),
        sa.Column('preferred_learning_style', sa.String(), nullable=True),
        sa.Column('skill_level', sa.String(), nullable=True),
        sa.Column('weekly_goal_hours', sa.Integer(), nullable=True),
        sa.Column('completed_hours', sa.Float(), nullable=True),
        sa.Column('streak_days', sa.Integer(), nullable=True),
    )

    # Skills & User Skills
    op.create_table(
        'skills',
        sa.Column('skill_id', sa.String(), nullable=False, primary_key=True),
        sa.Column('skill_name', sa.String(), nullable=False, unique=True),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
    )
    op.create_table(
        'user_skills',
        sa.Column('id', sa.String(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.String(), sa.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False),
        sa.Column('skill_id', sa.String(), sa.ForeignKey('skills.skill_id', ondelete='CASCADE'), nullable=False),
        sa.Column('mastery_score', sa.Float(), nullable=True),
        sa.Column('last_evaluated', sa.DateTime(timezone=True), nullable=True),
    )

    # Course Categories, Courses, Course Skills
    op.create_table(
        'course_categories',
        sa.Column('category_id', sa.String(), nullable=False, primary_key=True),
        sa.Column('category_name', sa.String(), nullable=False, unique=True),
        sa.Column('description', sa.Text(), nullable=True),
    )
    op.create_table(
        'courses',
        sa.Column('course_id', sa.String(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('instructor_name', sa.String(), nullable=False),
        sa.Column('thumbnail_url', sa.String(), nullable=True),
        sa.Column('category_id', sa.String(), sa.ForeignKey('course_categories.category_id'), nullable=True),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('difficulty_level', sa.String(), nullable=False),
        sa.Column('duration_hours', sa.Float(), nullable=False),
        sa.Column('rating', sa.Float(), nullable=True),
        sa.Column('enrolled_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_table(
        'course_skills',
        sa.Column('id', sa.String(), nullable=False, primary_key=True),
        sa.Column('course_id', sa.String(), sa.ForeignKey('courses.course_id', ondelete='CASCADE'), nullable=False),
        sa.Column('skill_id', sa.String(), sa.ForeignKey('skills.skill_id', ondelete='CASCADE'), nullable=False),
        sa.Column('is_prerequisite', sa.Boolean(), nullable=True),
    )

    # Enrollments, Progress, Assessments, Quiz Results
    op.create_table(
        'enrollments',
        sa.Column('enrollment_id', sa.String(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.String(), sa.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False),
        sa.Column('course_id', sa.String(), sa.ForeignKey('courses.course_id', ondelete='CASCADE'), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('enrolled_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_table(
        'progress',
        sa.Column('progress_id', sa.String(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.String(), sa.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False),
        sa.Column('course_id', sa.String(), sa.ForeignKey('courses.course_id', ondelete='CASCADE'), nullable=False),
        sa.Column('lesson_id', sa.String(), nullable=False),
        sa.Column('is_completed', sa.Boolean(), nullable=True),
        sa.Column('last_watched_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_table(
        'assessments',
        sa.Column('assessment_id', sa.String(), nullable=False, primary_key=True),
        sa.Column('course_id', sa.String(), sa.ForeignKey('courses.course_id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('max_score', sa.Float(), nullable=True),
    )
    op.create_table(
        'quiz_results',
        sa.Column('result_id', sa.String(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.String(), sa.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False),
        sa.Column('assessment_id', sa.String(), sa.ForeignKey('assessments.assessment_id'), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=True),
    )

    # Recommendations, Learning Paths, Items, Analytics Events
    op.create_table(
        'recommendations',
        sa.Column('recommendation_id', sa.String(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.String(), sa.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False),
        sa.Column('course_id', sa.String(), sa.ForeignKey('courses.course_id', ondelete='CASCADE'), nullable=False),
        sa.Column('match_score', sa.Float(), nullable=False),
        sa.Column('reason', sa.Text(), nullable=False),
        sa.Column('generated_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_table(
        'learning_paths',
        sa.Column('path_id', sa.String(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.String(), sa.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('overall_goal', sa.String(), nullable=False),
        sa.Column('total_duration_weeks', sa.Integer(), nullable=True),
    )
    op.create_table(
        'learning_path_items',
        sa.Column('item_id', sa.String(), nullable=False, primary_key=True),
        sa.Column('path_id', sa.String(), sa.ForeignKey('learning_paths.path_id', ondelete='CASCADE'), nullable=False),
        sa.Column('stage_number', sa.Integer(), nullable=False),
        sa.Column('stage_title', sa.String(), nullable=False),
        sa.Column('course_id', sa.String(), sa.ForeignKey('courses.course_id', ondelete='CASCADE'), nullable=False),
        sa.Column('estimated_weeks', sa.Integer(), nullable=True),
    )
    op.create_table(
        'analytics_events',
        sa.Column('event_id', sa.String(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.String(), sa.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False),
        sa.Column('event_type', sa.String(), nullable=False),
        sa.Column('payload', sa.JSON(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('analytics_events')
    op.drop_table('learning_path_items')
    op.drop_table('learning_paths')
    op.drop_table('recommendations')
    op.drop_table('quiz_results')
    op.drop_table('assessments')
    op.drop_table('progress')
    op.drop_table('enrollments')
    op.drop_table('course_skills')
    op.drop_table('courses')
    op.drop_table('course_categories')
    op.drop_table('user_skills')
    op.drop_table('skills')
    op.drop_table('profiles')
    op.drop_table('users')
