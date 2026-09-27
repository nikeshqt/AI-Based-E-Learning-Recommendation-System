import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.core.database import AsyncSessionLocal
from app.core.question_bank import TECHNICAL_QUESTION_BANK
from app.models.learning import AssessmentModel
from app.models.assessment import AssessmentQuestionModel, AssessmentAttemptModel, AssessmentAnswerModel
from app.models.skill import SkillModel, UserSkillModel
from app.models.user import UserModel, ProfileModel
from app.schemas.assessment import (
    AssessmentSchema,
    QuestionPublicSchema,
    AssessmentSubmitRequest,
    AssessmentResultResponse,
    AssessmentAttemptHistoryResponse,
)


class AssessmentService:
    """Service handling assessment retrieval, question bank seeding, scoring, and skill aggregation."""

    DEFAULT_ASSESSMENT_ID = "asm_tech_eval_01"

    async def seed_assessment_questions_if_empty(self) -> None:
        """Ensure default assessment and 40 technical questions are seeded in PostgreSQL."""
        async with AsyncSessionLocal() as session:
            try:
                # Check or create default assessment
                stmt_asm = select(AssessmentModel).where(AssessmentModel.assessment_id == self.DEFAULT_ASSESSMENT_ID)
                res_asm = await session.execute(stmt_asm)
                asm_obj = res_asm.scalar_one_or_none()

                if not asm_obj:
                    asm_obj = AssessmentModel(
                        assessment_id=self.DEFAULT_ASSESSMENT_ID,
                        course_id="crs_sec_03",
                        title="Comprehensive Technical Skill Assessment",
                        max_score=100.0,
                    )
                    session.add(asm_obj)
                    await session.commit()

                # Check existing questions
                stmt_q = select(AssessmentQuestionModel).where(AssessmentQuestionModel.assessment_id == self.DEFAULT_ASSESSMENT_ID)
                res_q = await session.execute(stmt_q)
                existing_qs = res_q.scalars().all()

                if len(existing_qs) < len(TECHNICAL_QUESTION_BANK):
                    existing_ids = {q.question_id for q in existing_qs}
                    for q_data in TECHNICAL_QUESTION_BANK:
                        if q_data["question_id"] not in existing_ids:
                            q_obj = AssessmentQuestionModel(
                                question_id=q_data["question_id"],
                                assessment_id=self.DEFAULT_ASSESSMENT_ID,
                                domain=q_data["domain"],
                                difficulty=q_data["difficulty"],
                                prompt=q_data["prompt"],
                                code_snippet=q_data.get("code_snippet"),
                                options=q_data["options"],
                                correct_answer=q_data["correct_answer"],
                                explanation=q_data["explanation"],
                                skill_measured=q_data["skill_measured"],
                            )
                            session.add(q_obj)
                    await session.commit()
            except Exception as err:
                await session.rollback()
                print(f"[AssessmentService] Seed error: {err}")

    async def get_available_assessments(self) -> List[AssessmentSchema]:
        """Retrieve available technical assessments."""
        await self.seed_assessment_questions_if_empty()
        async with AsyncSessionLocal() as session:
            try:
                stmt = select(AssessmentModel)
                res = await session.execute(stmt)
                assessments = res.scalars().all()
                if assessments:
                    return [
                        AssessmentSchema(
                            assessment_id=a.assessment_id,
                            course_id=a.course_id,
                            title=a.title,
                            description="Comprehensive evaluation across 8 technical domains.",
                            total_questions=40,
                            time_limit_minutes=45,
                        )
                        for a in assessments
                    ]
            except Exception:
                pass

        return [
            AssessmentSchema(
                assessment_id=self.DEFAULT_ASSESSMENT_ID,
                course_id="crs_sec_03",
                title="Comprehensive Technical Skill Assessment",
                description="Comprehensive evaluation across 8 technical domains.",
                total_questions=40,
                time_limit_minutes=45,
            )
        ]

    async def get_questions_for_student(self, assessment_id: str) -> List[QuestionPublicSchema]:
        """Retrieve questions for student with correct answers and explanations stripped."""
        await self.seed_assessment_questions_if_empty()
        async with AsyncSessionLocal() as session:
            try:
                stmt = select(AssessmentQuestionModel).where(
                    AssessmentQuestionModel.assessment_id == assessment_id
                )
                res = await session.execute(stmt)
                questions = res.scalars().all()
                if questions:
                    return [
                        QuestionPublicSchema(
                            question_id=q.question_id,
                            assessment_id=q.assessment_id,
                            domain=q.domain,
                            difficulty=q.difficulty,
                            prompt=q.prompt,
                            code_snippet=q.code_snippet,
                            options=q.options,
                            skill_measured=q.skill_measured,
                        )
                        for q in questions
                    ]
            except Exception:
                pass

        # Fallback to in-memory question bank if DB query fails
        return [
            QuestionPublicSchema(
                question_id=q["question_id"],
                assessment_id=assessment_id,
                domain=q["domain"],
                difficulty=q["difficulty"],
                prompt=q["prompt"],
                code_snippet=q.get("code_snippet"),
                options=q["options"],
                skill_measured=q["skill_measured"],
            )
            for q in TECHNICAL_QUESTION_BANK
        ]

    async def submit_assessment(
        self, user_id: str, assessment_id: str, payload: AssessmentSubmitRequest
    ) -> AssessmentResultResponse:
        """Evaluate submitted answers, update PostgreSQL user_skills, and persist attempt history."""
        await self.seed_assessment_questions_if_empty()

        # Fetch questions with correct answers from DB or fallback
        q_dict: Dict[str, Dict[str, Any]] = {}
        async with AsyncSessionLocal() as session:
            try:
                stmt = select(AssessmentQuestionModel).where(
                    AssessmentQuestionModel.assessment_id == assessment_id
                )
                res = await session.execute(stmt)
                db_qs = res.scalars().all()
                for q in db_qs:
                    q_dict[q.question_id] = {
                        "question_id": q.question_id,
                        "domain": q.domain,
                        "difficulty": q.difficulty,
                        "correct_answer": q.correct_answer,
                        "skill_measured": q.skill_measured,
                    }
            except Exception:
                pass

        if not q_dict:
            for q in TECHNICAL_QUESTION_BANK:
                q_dict[q["question_id"]] = q

        total_questions = len(q_dict)
        answers_map = {a.question_id: a.selected_option for a in payload.answers}

        correct_count = 0
        incorrect_count = 0
        answered_count = len(answers_map)

        topic_totals: Dict[str, int] = {}
        topic_correct: Dict[str, int] = {}
        diff_totals: Dict[str, int] = {}
        diff_correct: Dict[str, int] = {}
        skill_totals: Dict[str, int] = {}
        skill_correct: Dict[str, int] = {}

        answer_records: List[Dict[str, Any]] = []

        for q_id, q_info in q_dict.items():
            domain = q_info["domain"]
            difficulty = q_info["difficulty"]
            skill = q_info["skill_measured"]

            topic_totals[domain] = topic_totals.get(domain, 0) + 1
            diff_totals[difficulty] = diff_totals.get(difficulty, 0) + 1
            skill_totals[skill] = skill_totals.get(skill, 0) + 1

            selected = answers_map.get(q_id, "")
            is_correct = False
            if selected:
                # Check exact match or option text match
                target_correct = str(q_info["correct_answer"]).strip()
                selected_clean = str(selected).strip()
                if selected_clean == target_correct or target_correct in selected_clean:
                    is_correct = True

            if is_correct:
                correct_count += 1
                topic_correct[domain] = topic_correct.get(domain, 0) + 1
                diff_correct[difficulty] = diff_correct.get(difficulty, 0) + 1
                skill_correct[skill] = skill_correct.get(skill, 0) + 1
            elif selected:
                incorrect_count += 1

            if selected:
                answer_records.append({
                    "question_id": q_id,
                    "selected_option": selected,
                    "is_correct": is_correct,
                })

        overall_score = round((correct_count / max(1, total_questions)) * 100.0, 1)

        topic_scores = {
            dom: round((topic_correct.get(dom, 0) / count) * 100.0, 1)
            for dom, count in topic_totals.items()
        }

        difficulty_performance = {
            diff: round((diff_correct.get(diff, 0) / count) * 100.0, 1)
            for diff, count in diff_totals.items()
        }

        skill_proficiency: Dict[str, str] = {}
        assessed_skill_scores: Dict[str, float] = {}

        for skill_name, count in skill_totals.items():
            score_pct = round((skill_correct.get(skill_name, 0) / count) * 100.0, 1)
            assessed_skill_scores[skill_name] = score_pct / 100.0  # Normalized 0.0 - 1.0

            if score_pct >= 85.0:
                prof_label = "Advanced"
            elif score_pct >= 70.0:
                prof_label = "Proficient"
            elif score_pct >= 40.0:
                prof_label = "Developing"
            else:
                prof_label = "Beginner"

            skill_proficiency[skill_name] = f"{prof_label} ({int(score_pct)}%)"

        # Update PostgreSQL user_skills with non-downgrading aggregation strategy
        now_utc = datetime.now(timezone.utc)
        attempt_id = f"att_{uuid.uuid4().hex[:8]}"

        async with AsyncSessionLocal() as session:
            try:
                async with session.begin():
                    # 1. Update user profile skill_level
                    stmt_prof = select(ProfileModel).where(ProfileModel.user_id == user_id)
                    res_prof = await session.execute(stmt_prof)
                    profile = res_prof.scalar_one_or_none()
                    if profile:
                        if overall_score >= 75.0:
                            profile.skill_level = "advanced"
                        elif overall_score >= 50.0:
                            profile.skill_level = "intermediate"
                        else:
                            profile.skill_level = "beginner"

                    # 2. Persist skill mastery updates using max(existing, new) aggregation
                    stmt_us = select(UserSkillModel).options(selectinload(UserSkillModel.skill)).where(UserSkillModel.user_id == user_id)
                    res_us = await session.execute(stmt_us)
                    existing_user_skills = res_us.scalars().all()
                    existing_map = {us.skill.skill_name.lower(): us for us in existing_user_skills if us.skill}

                    for skill_name, new_mastery in assessed_skill_scores.items():
                        skill_key = skill_name.lower()
                        # Fetch or create skill definition entity
                        stmt_sk = select(SkillModel).where(SkillModel.skill_name == skill_name)
                        res_sk = await session.execute(stmt_sk)
                        sk_obj = res_sk.scalar_one_or_none()

                        if not sk_obj:
                            sk_obj = SkillModel(
                                skill_id=f"sk_{uuid.uuid4().hex[:6]}",
                                skill_name=skill_name,
                                category="Domain Skill",
                                description=f"{skill_name} Technical Skill",
                            )
                            session.add(sk_obj)
                            await session.flush()

                        if skill_key in existing_map:
                            us_obj = existing_map[skill_key]
                            # Preserves stronger demonstrated mastery strategy
                            us_obj.mastery_score = max(us_obj.mastery_score or 0.0, new_mastery)
                            us_obj.last_evaluated = now_utc
                        else:
                            new_us = UserSkillModel(
                                id=f"usk_{uuid.uuid4().hex[:8]}",
                                user_id=user_id,
                                skill_id=sk_obj.skill_id,
                                mastery_score=new_mastery,
                                last_evaluated=now_utc,
                            )
                            session.add(new_us)

                    # 3. Create AssessmentAttemptRecord
                    attempt_obj = AssessmentAttemptModel(
                        attempt_id=attempt_id,
                        user_id=user_id,
                        assessment_id=assessment_id,
                        total_questions=total_questions,
                        answered_questions=answered_count,
                        correct_answers=correct_count,
                        incorrect_answers=incorrect_count,
                        overall_score=overall_score,
                        topic_scores=topic_scores,
                        difficulty_performance=difficulty_performance,
                        skill_proficiency=skill_proficiency,
                        started_at=now_utc,
                        submitted_at=now_utc,
                    )
                    session.add(attempt_obj)
                    await session.flush()

                    for a_rec in answer_records:
                        ans_obj = AssessmentAnswerModel(
                            answer_id=f"ans_{uuid.uuid4().hex[:8]}",
                            attempt_id=attempt_id,
                            question_id=a_rec["question_id"],
                            selected_option=a_rec["selected_option"],
                            is_correct=a_rec["is_correct"],
                        )
                        session.add(ans_obj)

                    await session.commit()
            except Exception as err:
                await session.rollback()
                print(f"[AssessmentService] Submit Error: {err}")

        return AssessmentResultResponse(
            attempt_id=attempt_id,
            assessment_id=assessment_id,
            user_id=user_id,
            total_questions=total_questions,
            answered_questions=answered_count,
            correct_answers=correct_count,
            incorrect_answers=incorrect_count,
            overall_score=overall_score,
            topic_scores=topic_scores,
            difficulty_performance=difficulty_performance,
            skill_proficiency=skill_proficiency,
            submitted_at=now_utc,
        )

    async def get_user_history(self, user_id: str) -> AssessmentAttemptHistoryResponse:
        """Retrieve all assessment submission attempts for authenticated student."""
        async with AsyncSessionLocal() as session:
            try:
                stmt = (
                    select(AssessmentAttemptModel)
                    .where(AssessmentAttemptModel.user_id == user_id)
                    .order_by(AssessmentAttemptModel.submitted_at.desc())
                )
                res = await session.execute(stmt)
                attempts = res.scalars().all()
                if attempts:
                    res_list = [
                        AssessmentResultResponse(
                            attempt_id=a.attempt_id,
                            assessment_id=a.assessment_id,
                            user_id=a.user_id,
                            total_questions=a.total_questions,
                            answered_questions=a.answered_questions,
                            correct_answers=a.correct_answers,
                            incorrect_answers=a.incorrect_answers,
                            overall_score=a.overall_score,
                            topic_scores=a.topic_scores,
                            difficulty_performance=a.difficulty_performance,
                            skill_proficiency=a.skill_proficiency,
                            submitted_at=a.submitted_at or datetime.now(timezone.utc),
                        )
                        for a in attempts
                    ]
                    return AssessmentAttemptHistoryResponse(
                        user_id=user_id,
                        total_attempts=len(res_list),
                        attempts=res_list,
                    )
            except Exception:
                pass

        return AssessmentAttemptHistoryResponse(user_id=user_id, total_attempts=0, attempts=[])

    async def get_latest_user_result(self, user_id: str, assessment_id: str) -> Optional[AssessmentResultResponse]:
        """Retrieve the latest assessment submission attempt for authenticated student."""
        async with AsyncSessionLocal() as session:
            try:
                stmt = (
                    select(AssessmentAttemptModel)
                    .where(
                        AssessmentAttemptModel.user_id == user_id,
                        AssessmentAttemptModel.assessment_id == assessment_id,
                    )
                    .order_by(AssessmentAttemptModel.submitted_at.desc())
                )
                res = await session.execute(stmt)
                latest = res.scalars().first()
                if latest:
                    return AssessmentResultResponse(
                        attempt_id=latest.attempt_id,
                        assessment_id=latest.assessment_id,
                        user_id=latest.user_id,
                        total_questions=latest.total_questions,
                        answered_questions=latest.answered_questions,
                        correct_answers=latest.correct_answers,
                        incorrect_answers=latest.incorrect_answers,
                        overall_score=latest.overall_score,
                        topic_scores=latest.topic_scores,
                        difficulty_performance=latest.difficulty_performance,
                        skill_proficiency=latest.skill_proficiency,
                        submitted_at=latest.submitted_at or datetime.now(timezone.utc),
                    )
            except Exception:
                pass

        return None


assessment_service = AssessmentService()
