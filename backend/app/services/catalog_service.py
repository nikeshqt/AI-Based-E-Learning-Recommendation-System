from typing import List, Optional
from app.schemas.course import CourseResponse, LessonSchema


class CatalogService:
    """Course Catalog Management Service providing course listings and lesson breakdowns."""

    def __init__(self):
        self._courses = [
            CourseResponse(
                course_id="crs_sec_04",
                title="Advanced Cybersecurity Analysis & Network Defense",
                description="Master Linux security auditing, network penetration testing, and threat vector analysis for Cybersecurity Analysts.",
                instructor_name="Sarah Jenkins, CISSP",
                thumbnail_url=None,
                category="Cybersecurity",
                difficulty_level="Intermediate",
                duration_hours=8.0,
                rating=4.95,
                enrolled_count=3120,
                prerequisites=["Linux", "Networking"],
                skills_taught=["Cybersecurity", "Linux", "Networking", "Penetration Testing"],
                lessons=[
                    LessonSchema(lesson_id="lsn_sec_1", title="Linux Kernel Hardening & Auditing", duration_minutes=45, is_completed=False),
                    LessonSchema(lesson_id="lsn_sec_2", title="Wireshark Packet Analysis & Intrusion Detection", duration_minutes=50, is_completed=False),
                    LessonSchema(lesson_id="lsn_sec_3", title="Python Automation for Threat Hunting", duration_minutes=60, is_completed=False),
                ],
            ),
            CourseResponse(
                course_id="crs_gnn_01",
                title="Graph Neural Networks for Recommendation Systems",
                description="Master LightGCN, PyTorch Geometric, and link prediction for collaborative filtering.",
                instructor_name="Dr. Elena Rostova",
                thumbnail_url=None,
                category="Artificial Intelligence",
                difficulty_level="Advanced",
                duration_hours=6.5,
                rating=4.9,
                enrolled_count=1420,
                prerequisites=["Python", "PyTorch"],
                skills_taught=["LightGCN", "PyTorch Geometric", "GNN"],
                lessons=[
                    LessonSchema(lesson_id="lsn_1", title="Bipartite Graphs & Embeddings", duration_minutes=25, is_completed=True),
                    LessonSchema(lesson_id="lsn_2", title="LightGCN Aggregation Layers", duration_minutes=40, is_completed=False),
                    LessonSchema(lesson_id="lsn_3", title="BPR Loss Optimization", duration_minutes=35, is_completed=False),
                ],
            ),
            CourseResponse(
                course_id="crs_qdrant_02",
                title="Production Vector Search with Qdrant & Milvus",
                description="Build fast ANN retrieval engines scaling to millions of embeddings.",
                instructor_name="Marcus Vance",
                thumbnail_url=None,
                category="Data Engineering",
                difficulty_level="Intermediate",
                duration_hours=4.0,
                rating=4.8,
                enrolled_count=2890,
                prerequisites=["Python"],
                skills_taught=["Qdrant", "HNSW", "ANN Search"],
                lessons=[
                    LessonSchema(lesson_id="lsn_10", title="HNSW Indexing Principles", duration_minutes=30, is_completed=True),
                    LessonSchema(lesson_id="lsn_11", title="Qdrant Payload Filtering", duration_minutes=45, is_completed=False),
                ],
            ),
            CourseResponse(
                course_id="crs_sasrec_03",
                title="SASRec: Sequential Recommendation with Self-Attention",
                description="Implement SASRec in PyTorch to predict learner next-item interactions.",
                instructor_name="Dr. Aris Thorne",
                thumbnail_url=None,
                category="Deep Learning",
                difficulty_level="Advanced",
                duration_hours=5.2,
                rating=4.95,
                enrolled_count=940,
                prerequisites=["PyTorch", "Transformers"],
                skills_taught=["SASRec", "Self-Attention", "PyTorch"],
                lessons=[
                    LessonSchema(lesson_id="lsn_20", title="Sequence Modeling for Learner Telemetry", duration_minutes=35, is_completed=False),
                ],
            ),
        ]
        self._course_map = {c.course_id: c for c in self._courses}

    async def list_courses(self, category: Optional[str] = None) -> List[CourseResponse]:
        """List courses, optionally filtered by category."""
        if not category:
            return self._courses
        return [c for c in self._courses if c.category.lower() == category.lower()]

    async def get_course(self, course_id: str) -> Optional[CourseResponse]:
        """Retrieve course details by course ID."""
        return self._course_map.get(course_id)


catalog_service = CatalogService()
