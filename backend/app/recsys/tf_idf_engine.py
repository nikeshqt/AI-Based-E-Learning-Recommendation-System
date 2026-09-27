import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.schemas.course import CourseResponse
from app.schemas.user import UserResponse


class HybridAIRecommendationEngine:
    """Multi-Factor AI Recommendation Engine using TF-IDF, Cosine Similarity, Skill Gap Analysis,

    Career Goal Alignment, Assessment Performance, and Learning History filtering.
    """

    def __init__(
        self,
        weight_tfidf: float = 0.35,
        weight_skill: float = 0.25,
        weight_goal: float = 0.20,
        weight_difficulty: float = 0.10,
        weight_prereq: float = 0.10,
    ):
        self.w_tfidf = weight_tfidf
        self.w_skill = weight_skill
        self.w_goal = weight_goal
        self.w_diff = weight_difficulty
        self.w_prereq = weight_prereq

    def _build_course_document(self, course: CourseResponse) -> str:
        """Construct a dense text representation for TF-IDF vectorization."""
        skills_str = " ".join(course.skills_taught)
        prereq_str = " ".join(course.prerequisites)
        return (
            f"{course.title} {course.description} {course.category} "
            f"{course.difficulty_level} {skills_str} {prereq_str}"
        )

    def _build_user_document(self, user: UserResponse) -> str:
        """Construct a text document representing learner preferences and career goals."""
        if not user:
            return "Cybersecurity Analyst visual beginner"

        skills_list = getattr(user, "skills", []) or []
        user_skills_str = " ".join([s.skill_name for s in skills_list])
        goal = getattr(user, "learning_goal", "Cybersecurity Analyst")
        style = getattr(user, "preferred_learning_style", "visual")
        level = getattr(user, "skill_level", "beginner")

        return f"{goal} {style} {level} {user_skills_str}"

    def compute_tfidf_similarities(
        self, user: UserResponse, courses: List[CourseResponse]
    ) -> np.ndarray:
        """Compute TF-IDF vector representations and Cosine Similarity scores."""
        if not courses:
            return np.array([])

        course_docs = [self._build_course_document(c) for c in courses]
        user_doc = self._build_user_document(user)

        all_docs = course_docs + [user_doc]
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(all_docs)

        # Separate course vectors and user query vector
        course_vectors = tfidf_matrix[:-1]
        user_vector = tfidf_matrix[-1:]

        similarities = cosine_similarity(user_vector, course_vectors)[0]
        return similarities

    def compute_skill_matching_score(self, user: UserResponse, course: CourseResponse) -> float:
        """Calculate skill match score based on target skills and current user mastery."""
        skills_list = getattr(user, "skills", []) or [] if user else []
        user_skill_names = {s.skill_name.lower(): s.mastery_score for s in skills_list}
        taught_skills = [s.lower() for s in course.skills_taught]

        if not taught_skills:
            return 0.5

        # Measure how many taught skills address user's goals or unmastered domains
        matching_count = 0
        for skill in taught_skills:
            mastery = user_skill_names.get(skill, 0.0)
            # High score if course teaches a skill user needs (mastery < 0.8)
            if mastery < 0.8:
                matching_count += 1

        return matching_count / len(taught_skills)

    def compute_goal_alignment_score(self, user: UserResponse, course: CourseResponse) -> float:
        """Calculate keyword and domain alignment with explicit career goals."""
        goal_str = getattr(user, "learning_goal", "Cybersecurity Analyst") or "Cybersecurity Analyst" if user else "Cybersecurity Analyst"
        goal_words = set(goal_str.lower().split())
        course_text = (course.title + " " + course.category + " " + " ".join(course.skills_taught)).lower()

        matches = sum(1 for word in goal_words if len(word) > 2 and word in course_text)
        return min(1.0, matches / max(1, len(goal_words)))

    def compute_difficulty_adaptation_score(
        self, user: UserResponse, course: CourseResponse, avg_quiz_score: float = 0.75
    ) -> float:
        """Adapt recommendation scoring based on user assessment performance and self-reported level."""
        diff = course.difficulty_level.lower()
        level_str = getattr(user, "skill_level", "beginner") or "beginner" if user else "beginner"

        if avg_quiz_score >= 0.8 or level_str.lower() == "advanced":
            if diff == "advanced":
                return 1.0
            elif diff == "intermediate":
                return 0.8
            else:
                return 0.5
        elif avg_quiz_score <= 0.5 or level_str.lower() == "beginner":
            if diff == "beginner":
                return 1.0
            elif diff == "intermediate":
                return 0.6
            else:
                return 0.2
        else:
            # Intermediate learner
            if diff == "intermediate":
                return 1.0
            elif diff == "beginner":
                return 0.8
            else:
                return 0.7

    def compute_prerequisite_score(self, user: UserResponse, course: CourseResponse) -> float:
        """Evaluate whether learner meets course prerequisite thresholds."""
        if not course.prerequisites:
            return 1.0

        skills_list = getattr(user, "skills", []) or [] if user else []
        user_skills = {s.skill_name.lower(): s.mastery_score for s in skills_list}
        met_count = 0
        for prereq in course.prerequisites:
            mastery = user_skills.get(prereq.lower(), 0.0)
            if mastery >= 0.6:
                met_count += 1

        return met_count / len(course.prerequisites)

    def rank_courses(
        self,
        user: UserResponse,
        courses: List[CourseResponse],
        completed_course_ids: Optional[List[str]] = None,
        avg_quiz_score: float = 0.75,
    ) -> List[Tuple[CourseResponse, float, Dict[str, Any]]]:
        """Filter learning history, compute multi-factor scores, and rank courses."""
        completed_set = set(completed_course_ids or [])
        # Filter out 100% completed courses from recommendation pool
        candidate_courses = [c for c in courses if c.course_id not in completed_set]

        if not candidate_courses:
            return []

        tfidf_scores = self.compute_tfidf_similarities(user, candidate_courses)

        ranked_results = []
        for i, course in enumerate(candidate_courses):
            s_tfidf = float(tfidf_scores[i]) if i < len(tfidf_scores) else 0.0
            s_skill = self.compute_skill_matching_score(user, course)
            s_goal = self.compute_goal_alignment_score(user, course)
            s_diff = self.compute_difficulty_adaptation_score(user, course, avg_quiz_score)
            s_prereq = self.compute_prerequisite_score(user, course)

            # Combined Multi-Factor Formula
            final_score = (
                self.w_tfidf * s_tfidf
                + self.w_skill * s_skill
                + self.w_goal * s_goal
                + self.w_diff * s_diff
                + self.w_prereq * s_prereq
            )
            # Ensure score bounded between 0.0 and 1.0
            final_score = float(np.clip(final_score, 0.0, 1.0))

            explanation_metadata = {
                "tfidf_similarity": round(s_tfidf, 3),
                "skill_match_score": round(s_skill, 3),
                "goal_alignment_score": round(s_goal, 3),
                "difficulty_adapt_score": round(s_diff, 3),
                "prerequisite_satisfaction": round(s_prereq, 3),
            }

            ranked_results.append((course, final_score, explanation_metadata))

        # Sort descending by final score
        ranked_results.sort(key=lambda x: x[1], reverse=True)
        return ranked_results


rec_engine = HybridAIRecommendationEngine()
