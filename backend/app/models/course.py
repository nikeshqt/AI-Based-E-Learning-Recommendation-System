from sqlalchemy import Column, String, Float, Integer, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.database import Base


class CourseCategoryModel(Base):
    """Course Category entity stored in PostgreSQL course_categories table."""

    __tablename__ = "course_categories"

    category_id = Column(String, primary_key=True, index=True)
    category_name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)

    courses = relationship("CourseModel", back_populates="category_rel")


class CourseModel(Base):
    """Course catalog entity stored in PostgreSQL courses table."""

    __tablename__ = "courses"

    course_id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)
    instructor_name = Column(String, nullable=False)
    thumbnail_url = Column(String, nullable=True)
    category_id = Column(String, ForeignKey("course_categories.category_id"), nullable=True)
    category = Column(String, index=True, nullable=False)
    difficulty_level = Column(String, nullable=False)
    duration_hours = Column(Float, nullable=False)
    rating = Column(Float, default=5.0)
    enrolled_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    category_rel = relationship("CourseCategoryModel", back_populates="courses")
    course_skills = relationship("CourseSkillModel", back_populates="course", cascade="all, delete-orphan")
    enrollments = relationship("EnrollmentModel", back_populates="course", cascade="all, delete-orphan")
    modules = relationship("CourseModuleModel", back_populates="course", cascade="all, delete-orphan", order_by="CourseModuleModel.order_index")
    lessons = relationship("CourseLessonModel", back_populates="course", cascade="all, delete-orphan", order_by="CourseLessonModel.order_index")


class CourseModuleModel(Base):
    """Module grouping stored in PostgreSQL course_modules table."""

    __tablename__ = "course_modules"

    module_id = Column(String, primary_key=True, index=True)
    course_id = Column(String, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String, nullable=False)
    order_index = Column(Integer, default=1)

    course = relationship("CourseModel", back_populates="modules")
    lessons = relationship("CourseLessonModel", back_populates="module", cascade="all, delete-orphan", order_by="CourseLessonModel.order_index")


class CourseLessonModel(Base):
    """Educational lesson content stored in PostgreSQL course_lessons table."""

    __tablename__ = "course_lessons"

    lesson_id = Column(String, primary_key=True, index=True)
    module_id = Column(String, ForeignKey("course_modules.module_id", ondelete="CASCADE"), nullable=False, index=True)
    course_id = Column(String, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    order_index = Column(Integer, default=1)
    estimated_duration_minutes = Column(Integer, default=15)

    module = relationship("CourseModuleModel", back_populates="lessons")
    course = relationship("CourseModel", back_populates="lessons")


class CourseSkillModel(Base):
    """Prerequisite vs Taught skill mapping stored in PostgreSQL course_skills table."""

    __tablename__ = "course_skills"

    id = Column(String, primary_key=True, index=True)
    course_id = Column(String, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(String, ForeignKey("skills.skill_id", ondelete="CASCADE"), nullable=False)
    is_prerequisite = Column(Boolean, default=False)

    course = relationship("CourseModel", back_populates="course_skills")
    skill = relationship("SkillModel", back_populates="course_skills")
