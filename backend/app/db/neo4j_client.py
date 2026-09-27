from neo4j import AsyncGraphDatabase
from app.core.config import settings


class Neo4jClient:
    """Async Neo4j Graph Database connector stub for Skill Trees & Prerequisite graph."""

    def __init__(self):
        self.driver = None

    async def connect(self):
        """Initialize graph database connection."""
        self.driver = AsyncGraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
        )

    async def close(self):
        """Close graph connection."""
        if self.driver:
            await self.driver.close()

    async def query_prerequisites(self, course_id: str) -> list[str]:
        """Cypher query stub for fetching course skill prerequisites."""
        # Query stub implementation
        return []


neo4j_client = Neo4jClient()
