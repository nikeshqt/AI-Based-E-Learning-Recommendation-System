import pytest
from datetime import datetime, timezone
from app.schemas.user import UserResponse, SkillMasterySchema
from app.schemas.course import CourseResponse, LessonSchema
from app.recsys.tf_idf_engine import HybridAIRecommendationEngine


@pytest.fixture
def sample_user():
    return UserResponse(
        user_id="usr_test_01",
        email="test.learner@ai-learning.io",
        full_name="Test Learner",
        learning_goal="Artificial Intelligence & Graph Neural Networks",
        preferred_learning_style="visual",
        skill_level="intermediate",
        skills=[
            SkillMasterySchema(
                skill_id="sk_py",
                skill_name="Python",
                mastery_score=0.90,
                last_evaluated=datetime.now(timezone.utc),
                category="Programming",
            ),
            SkillMasterySchema(
                skill_id="sk_pytorch",
                skill_name="PyTorch",
                mastery_score=0.85,
                last_evaluated=datetime.now(timezone.utc),
                category="Frameworks",
            ),
        ],
    )


@pytest.fixture
def sample_courses():
    return [
        CourseResponse(
            course_id="crs_gnn_01",
            title="Graph Neural Networks for Recommendation Systems",
            description="Master LightGCN, PyTorch Geometric, and link prediction for collaborative filtering.",
            instructor_name="Dr. Elena Rostova",
            category="Artificial Intelligence",
            difficulty_level="Advanced",
            duration_hours=6.5,
            rating=4.9,
            enrolled_count=1420,
            prerequisites=["Python", "PyTorch"],
            skills_taught=["LightGCN", "PyTorch Geometric", "GNN"],
            lessons=[],
        ),
        CourseResponse(
            course_id="crs_qdrant_02",
            title="Production Vector Search with Qdrant & Milvus",
            description="Build fast ANN retrieval engines scaling to millions of embeddings.",
            instructor_name="Marcus Vance",
            category="Data Engineering",
            difficulty_level="Intermediate",
            duration_hours=4.0,
            rating=4.8,
            enrolled_count=2890,
            prerequisites=["Python"],
            skills_taught=["Qdrant", "HNSW", "ANN Search"],
            lessons=[],
        ),
        CourseResponse(
            course_id="crs_basic_math_03",
            title="Basic Arithmetic for Absolute Beginners",
            description="Introductory elementary math for beginners.",
            instructor_name="John Doe",
            category="Mathematics",
            difficulty_level="Beginner",
            duration_hours=2.0,
            rating=4.2,
            enrolled_count=500,
            prerequisites=[],
            skills_taught=["Addition", "Subtraction"],
            lessons=[],
        ),
    ]


def test_tfidf_cosine_similarity(sample_user, sample_courses):
    engine = HybridAIRecommendationEngine()
    similarities = engine.compute_tfidf_similarities(sample_user, sample_courses)

    assert len(similarities) == len(sample_courses)
    # GNN course (Artificial Intelligence) should have highest cosine similarity to user's AI goal
    assert similarities[0] > similarities[2]


def test_skill_matching_score(sample_user, sample_courses):
    engine = HybridAIRecommendationEngine()
    score_gnn = engine.compute_skill_matching_score(sample_user, sample_courses[0])

    assert 0.0 <= score_gnn <= 1.0
    assert score_gnn > 0.0


def test_career_goal_alignment(sample_user, sample_courses):
    engine = HybridAIRecommendationEngine()
    score_ai_goal = engine.compute_goal_alignment_score(sample_user, sample_courses[0])
    score_math_goal = engine.compute_goal_alignment_score(sample_user, sample_courses[2])

    assert score_ai_goal > score_math_goal


def test_difficulty_adaptation(sample_user, sample_courses):
    engine = HybridAIRecommendationEngine()
    # High assessment score -> prefers Advanced / Intermediate course
    score_high_assessment = engine.compute_difficulty_adaptation_score(
        sample_user, sample_courses[0], avg_quiz_score=0.90
    )
    # Low assessment score -> prefers Beginner course
    score_low_assessment = engine.compute_difficulty_adaptation_score(
        sample_user, sample_courses[2], avg_quiz_score=0.40
    )

    assert score_high_assessment >= 0.8
    assert score_low_assessment >= 0.8


def test_prerequisite_score(sample_user, sample_courses):
    engine = HybridAIRecommendationEngine()
    # User has Python (0.90) and PyTorch (0.85) -> Prerequisites met
    prereq_score = engine.compute_prerequisite_score(sample_user, sample_courses[0])
    assert prereq_score == 1.0


def test_learning_history_filtering(sample_user, sample_courses):
    engine = HybridAIRecommendationEngine()
    # Mark course crs_gnn_01 as completed in user's learning history
    completed_ids = ["crs_gnn_01"]

    ranked = engine.rank_courses(
        sample_user, sample_courses, completed_course_ids=completed_ids
    )

    # crs_gnn_01 should be filtered out
    ranked_course_ids = [item[0].course_id for item in ranked]
    assert "crs_gnn_01" not in ranked_course_ids
    assert len(ranked) == 2


def test_end_to_end_recommendation_ranking_verification(sample_user, sample_courses):
    engine = HybridAIRecommendationEngine()
    ranked = engine.rank_courses(sample_user, sample_courses)

    assert len(ranked) == 3
    # Top course should be GNN course given user's goal 'Artificial Intelligence & Graph Neural Networks'
    top_course, top_score, meta = ranked[0]
    assert top_course.course_id == "crs_gnn_01"
    assert top_score > 0.6
    assert "tfidf_similarity" in meta
    assert "skill_match_score" in meta
    assert "goal_alignment_score" in meta
