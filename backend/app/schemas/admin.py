from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime


class AdminActivityItem(BaseModel):
    log_id: str
    admin_id: Optional[str] = None
    admin_name: Optional[str] = None
    admin_email: Optional[str] = None
    action: str
    target_type: Optional[str] = None
    target_id: Optional[str] = None
    details: Optional[str] = None
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class AdminDashboardStats(BaseModel):
    total_students: int
    active_students: int
    total_courses: int
    total_enrollments: int
    courses_completed: int
    avg_course_progress: float
    assessment_completion_rate: float
    recent_activity: List[AdminActivityItem] = []
    enrollment_trends: List[Dict[str, Any]] = []
    goal_distribution: List[Dict[str, Any]] = []


class AdminStudentListItem(BaseModel):
    user_id: str
    full_name: str
    email: str
    career_goal: str
    skill_level: str
    role: str = "student"
    is_active: bool = True
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    assessment_status: str  # "Completed" or "Not Completed"
    assessment_score: Optional[float] = None
    enrolled_courses_count: int = 0
    overall_progress: float = 0.0

    model_config = ConfigDict(from_attributes=True)


class AdminStudentListResponse(BaseModel):
    total: int
    students: List[AdminStudentListItem]


class StudentProfileSection(BaseModel):
    user_id: str
    full_name: str
    email: str
    career_goal: str
    preferred_learning_style: str
    skill_level: str
    is_active: bool
    role: str
    registration_date: Optional[datetime] = None
    last_login: Optional[datetime] = None


class StudentAssessmentSection(BaseModel):
    completed: bool
    overall_score: Optional[float] = None
    topic_scores: Dict[str, float] = {}
    difficulty_performance: Dict[str, float] = {}
    skill_proficiency: Dict[str, str] = {}
    total_questions: int = 0
    correct_answers: int = 0
    submitted_at: Optional[datetime] = None


class StudentSkillGapSection(BaseModel):
    skill: str
    current_mastery: float
    target_mastery: float
    gap: float
    priority: float
    category: str


class StudentRecommendationSection(BaseModel):
    course_id: str
    title: str
    match_score: float
    recommendation_reason: str
    target_skill_gap: Optional[str] = None


class StudentLearningPathStage(BaseModel):
    stage_number: int
    stage_title: str
    course_id: str
    course_title: str
    status: str
    target_skill: Optional[str] = None


class StudentLearningPathSection(BaseModel):
    path_id: Optional[str] = None
    title: Optional[str] = None
    overall_readiness: float = 0.0
    is_active: bool = True
    stages: List[StudentLearningPathStage] = []


class StudentCourseProgressSection(BaseModel):
    course_id: str
    course_title: str
    category: str
    enrollment_date: Optional[datetime] = None
    progress_percentage: float = 0.0
    completed_lessons: int = 0
    total_lessons: int = 0
    completion_status: str = "ENROLLED"
    last_activity: Optional[datetime] = None


class AdminStudentDetailResponse(BaseModel):
    profile: StudentProfileSection
    assessment: StudentAssessmentSection
    skill_gaps: List[StudentSkillGapSection] = []
    recommendations: List[StudentRecommendationSection] = []
    learning_path: Optional[StudentLearningPathSection] = None
    course_progress: List[StudentCourseProgressSection] = []


class AdminStudentStatusUpdate(BaseModel):
    is_active: bool


class AdminCourseCreate(BaseModel):
    title: str
    description: str
    category: str
    difficulty_level: str
    duration_hours: float
    instructor_name: str
    prerequisites: List[str] = []
    skills_taught: List[str] = []


class AdminCourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty_level: Optional[str] = None
    duration_hours: Optional[float] = None
    instructor_name: Optional[str] = None
    prerequisites: Optional[List[str]] = None
    skills_taught: Optional[List[str]] = None
    is_active: Optional[bool] = None


class AdminCourseStatusUpdate(BaseModel):
    is_active: bool


class AdminCourseItem(BaseModel):
    course_id: str
    title: str
    description: str
    instructor_name: str
    category: str
    difficulty_level: str
    duration_hours: float
    rating: float = 5.0
    enrolled_count: int = 0
    is_active: bool = True
    prerequisites: List[str] = []
    skills_taught: List[str] = []
    modules_count: int = 0
    lessons_count: int = 0
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class AdminProgressItem(BaseModel):
    enrollment_id: str
    student_id: str
    student_name: str
    student_email: str
    course_id: str
    course_title: str
    progress_percentage: float
    completed_lessons: int
    total_lessons: int
    started_date: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    status: str


class AdminProgressUpdate(BaseModel):
    progress_percentage: Optional[float] = None
    status: Optional[str] = None
    reason: Optional[str] = "Administrative adjustment"


class StudentAnalyticsData(BaseModel):
    total_students: int
    new_registrations: int
    active_students: int
    assessment_completion_rate: float


class CourseAnalyticsData(BaseModel):
    total_courses: int
    most_enrolled_courses: List[Dict[str, Any]] = []
    most_completed_courses: List[Dict[str, Any]] = []
    average_completion_percentage: float = 0.0


class LearningAnalyticsData(BaseModel):
    average_student_progress: float = 0.0
    active_learners_count: int = 0
    completed_courses_count: int = 0
    incomplete_learning_paths_count: int = 0


class SkillAnalyticsData(BaseModel):
    most_common_skill_gaps: List[Dict[str, Any]] = []
    skill_distribution: List[Dict[str, Any]] = []
    career_goal_distribution: List[Dict[str, Any]] = []


class AdminAnalyticsResponse(BaseModel):
    student_analytics: StudentAnalyticsData
    course_analytics: CourseAnalyticsData
    learning_analytics: LearningAnalyticsData
    skill_analytics: SkillAnalyticsData
