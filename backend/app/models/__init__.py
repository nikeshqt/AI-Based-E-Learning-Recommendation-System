from app.core.database import Base
from app.models.user import UserModel, ProfileModel
from app.models.skill import SkillModel, UserSkillModel, GoalRequiredSkillModel
from app.models.course import (
    CourseCategoryModel,
    CourseModel,
    CourseSkillModel,
    CourseModuleModel,
    CourseLessonModel,
)
from app.models.learning import EnrollmentModel, ProgressModel, AssessmentModel, QuizResultModel
from app.models.assessment import AssessmentQuestionModel, AssessmentAttemptModel, AssessmentAnswerModel
from app.models.recommendation import RecommendationModel, LearningPathModel, LearningPathItemModel
from app.models.interaction import AnalyticsEventModel
from app.models.admin_log import AdminActivityLogModel

__all__ = [
    "Base",
    "UserModel",
    "ProfileModel",
    "SkillModel",
    "UserSkillModel",
    "GoalRequiredSkillModel",
    "CourseCategoryModel",
    "CourseModel",
    "CourseSkillModel",
    "CourseModuleModel",
    "CourseLessonModel",
    "EnrollmentModel",
    "ProgressModel",
    "AssessmentModel",
    "QuizResultModel",
    "AssessmentQuestionModel",
    "AssessmentAttemptModel",
    "AssessmentAnswerModel",
    "RecommendationModel",
    "LearningPathModel",
    "LearningPathItemModel",
    "AnalyticsEventModel",
    "AdminActivityLogModel",
]
