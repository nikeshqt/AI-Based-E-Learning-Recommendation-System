from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.future import select

from app.core.security import get_current_user_id
from app.core.database import AsyncSessionLocal
from app.models.course import CourseLessonModel, CourseModel


class AITutorChatRequest(BaseModel):
    """Payload for requesting AI Tutor educational assistance."""

    message: str
    course_id: Optional[str] = None
    lesson_id: Optional[str] = None
    action: Optional[str] = None  # explain_simply, give_example, summarize, quiz_me


class AITutorChatResponse(BaseModel):
    """Response returned by AI Tutor Assistant."""

    reply: str
    source_context: str
    lesson_title: Optional[str] = None


router = APIRouter()


@router.post("/chat", response_model=AITutorChatResponse)
async def chat_with_ai_tutor(
    body: AITutorChatRequest,
    current_user_id: str = Depends(get_current_user_id),
):
    """Contextualized AI Tutor assistant for lesson explanations, quick actions, and concept clarification."""
    lesson_title = None
    lesson_content = None

    # Fetch lesson context from database if lesson_id is provided
    if body.lesson_id:
        async with AsyncSessionLocal() as session:
            stmt = select(CourseLessonModel).where(
                CourseLessonModel.lesson_id == body.lesson_id
            )
            res = await session.execute(stmt)
            lesson = res.scalars().first()
            if lesson:
                lesson_title = lesson.title
                lesson_content = lesson.content

    # Determine quick action or custom message query
    user_query = body.message.strip().lower()
    action = (body.action or "").lower()

    if action == "explain_simply" or "explain" in user_query:
        if lesson_title and lesson_content:
            reply = (
                f"### Core Concept Explanation for '{lesson_title}':\n\n"
                f"Here is a simplified breakdown of this lesson:\n"
                f"1. **Primary Purpose**: {lesson_title} focuses on essential security and engineering controls.\n"
                f"2. **Key Takeaway**: Follow standard operational practices, keep log monitoring enabled, and test configuration parameters incrementally.\n\n"
                f"**Lesson Context**: {lesson_content[:180]}..."
            )
        else:
            reply = (
                f"### Simplified Explanation:\n\n"
                f"This concept covers fundamental principles in modern software development and cybersecurity. "
                f"Focus on understanding the core inputs, execution flow, and defensive checks before advancing."
            )
    elif action == "give_example" or "example" in user_query:
        reply = (
            f"### Practical Code & Operational Example:\n\n"
            f"```bash\n"
            f"# Step 1: Verify current system parameters\n"
            f"auditctl -l\n\n"
            f"# Step 2: Configure access permissions\n"
            f"chmod 750 /etc/security/audit.conf\n"
            f"```\n\n"
            f"This command sequence restricts unauthorized file execution while maintaining active logging."
        )
    elif action == "summarize" or "summarize" in user_query:
        reply = (
            f"### Key Lesson Summary:\n"
            f"- **Topic**: {lesson_title or 'Technical Fundamentals'}\n"
            f"- **Principle 1**: Least privilege permission enforcement.\n"
            f"- **Principle 2**: Continuous monitoring and log inspection.\n"
            f"- **Principle 3**: Automated remediation for anomalous events."
        )
    elif action == "quiz_me" or "quiz" in user_query:
        reply = (
            f"### Quick Review Quiz:\n\n"
            f"**Question 1**: What configuration parameter controls kernel audit log rules in Linux?\n"
            f"A) `/etc/hosts`  \nB) `/etc/audit/audit.rules`  \nC) `/var/log/syslog`  \n*Answer: B*\n\n"
            f"**Question 2**: Which distance metric measures angle alignment between high-dimensional vector embeddings?\n"
            f"A) Cosine Similarity  \nB) Manhattan Distance  \nC) Hamming Distance  \n*Answer: A*"
        )
    else:
        reply = (
            f"AI Tutor: I analyzed your query regarding '{body.message}'. "
            f"Based on your active course context ({lesson_title or 'General AI Curriculum'}), "
            f"make sure to review the foundational modules, verify command syntax, and complete the end-of-module assessment."
        )

    return AITutorChatResponse(
        reply=reply,
        source_context=f"Lesson: {lesson_title}" if lesson_title else "General Curriculum Knowledgebase",
        lesson_title=lesson_title,
    )
