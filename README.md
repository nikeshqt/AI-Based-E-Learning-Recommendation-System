# AI-Based E-Learning Recommendation System

> **College Final Year Project** — Personalized, Adaptive, and Data-Driven E-Learning Platform powered by a Hybrid AI Recommendation Engine, Skill Gap Matrix, Prerequisite-Aware Pathways, and AI Tutor Assistance.

---

## 📌 Project Overview

The **AI-Based E-Learning Recommendation System** is an intelligent learning management system (LMS) designed to solve content discovery friction and skill mismatch for students. By analyzing student career goals, skill assessment performance, and active gaps, the platform generates personalized course recommendations, orders learning modules based on prerequisite dependencies, tracks lesson completion progress, and provides context-aware AI Tutoring.

---

## 🚀 Key Features

1. **PostgreSQL Persistence & JWT Authentication**: Secure, schema-validated student profiles, course enrollments, assessment attempts, and progress records.
2. **40-Question Technical Skill Assessment System**: Evaluates proficiency across 8 key technical domains (Python, Networking, Linux, Cybersecurity, AI/ML, SQL, Web Dev, Cloud).
3. **Real-Time Skill Gap Analysis**: Calculates quantitative skill deficits between current student mastery and target career goal requirements.
4. **Hybrid AI Recommendation Engine**: Combines TF-IDF vector similarity, cosine distance matching, and explainable rationale generation.
5. **Prerequisite-Aware Personalized Learning Path**: Dynamically orders courses into progressive stages (Foundation, Core Mastery, Advanced Specialization) ensuring prerequisite skills are learned first.
6. **Simple Course Reader & Progress Tracking**: Interactive course reader with module/lesson navigation, estimated duration badges, and automatic progress percentage calculation $(\frac{\text{completed\_lessons}}{\text{total\_lessons}} \times 100)$.
7. **Contextual AI Tutor Assistant**: Quick educational explanations, code examples, bullet summaries, and review quizzes for any course lesson.

---

## 🛠️ Technology Stack

- **Frontend**: React 19, TypeScript, Vite, Tailwind CSS, Lucide Icons
- **Backend**: Python 3.13, FastAPI, Pydantic v2, Uvicorn
- **Database / ORM**: PostgreSQL, SQLAlchemy 2.0 (AsyncIO), Alembic migrations, SQLite fallback engine
- **Machine Learning / RecSys**: Scikit-Learn (TF-IDF Vectorizer & Cosine Similarity), NumPy

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    A["React + TypeScript Frontend UI"] -->|HTTP / REST API (JWT)| B["FastAPI Backend Server"]
    B --> C["PostgreSQL Persistent Database"]
    B --> D["Hybrid AI Recommendation Engine"]
    D --> E["TF-IDF Vectorizer & Cosine Similarity"]
    B --> F["Skill Gap Matrix Service"]
    B --> G["Personalized Learning Path Engine"]
    B --> H["AI Tutor Educational Assistant"]
```

---

## 📊 Database Architecture

The core data model consists of 14 persistent entities:
- `users` — Learner authentication credentials & metadata.
- `profiles` — Target career goals, preferred learning styles, and skill levels.
- `skills` & `user_skills` — Master skill registry and student proficiency percentages.
- `courses`, `course_categories`, `course_skills` — Catalog metadata and skill tags.
- `course_modules` & `course_lessons` — Educational modules and structured lesson content.
- `enrollments` & `progress` — Student enrollment statuses, progress percentages, and lesson completions.
- `assessments`, `assessment_questions`, `assessment_attempts` — Quiz questions, answers, and scoring history.
- `learning_paths` & `learning_path_items` — Prerequisite-aware course roadmap stages.

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+
- Node.js 18+ and `npm`

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8085 --reload
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 🧪 Testing & Verification

### Running Backend Unit Tests (57 Tests)
```bash
cd backend
python -m pytest
```

### Running Frontend Production Build
```bash
cd frontend
npm run build
```

### Running Full 26-Step Live E2E College Demo Test
```bash
cd backend
python -m scripts.run_e2e_college_demo
```

---

## 🛡️ Role-Based Admin Dashboard

The application incorporates a secure **Role-Based Admin Console** allowing administrative oversight while maintaining strict student data isolation.

### 1. Admin Account Creation & Seeding
The backend automatically initializes an administrative user upon startup if not present, and also provides a standalone CLI script for developer management:

```bash
cd backend
python -m scripts.seed_admin
```

**Default Admin Credentials:**
- **Email:** `admin@elearning.io`
- **Password:** `Admin@12345`
- **Role:** `admin`

Passwords are securely hashed with `bcrypt`/`passlib`. Credentials and password hashes are never exposed in responses or audit logs.

### 2. Role-Based Access Control (RBAC)
- **Role Detection:** Determined strictly from database record and verified JWT payload (`role == "admin"`). Frontend role assertions are rejected.
- **Route Protection:** Normal student JWT tokens attempting to access `/api/v1/admin/*` or `/admin/*` receive **HTTP 403 Forbidden**.
- **Account Status Enforcement:** Deactivated student accounts have login rejected and active sessions revoked.
- **Audit Trails:** Administrative operations (logins, student status changes, course modifications, progress corrections) are immutably logged to `admin_activity_logs`.

---

## 📝 API Endpoints Overview

| Module | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| **Auth** | `POST /api/v1/auth/register` | Register new student account | Public |
| | `POST /api/v1/auth/login` | Login & receive JWT access token (with role) | Public |
| | `GET /api/v1/auth/me` | Fetch authenticated profile | Authenticated |
| **Assessments** | `GET /api/v1/assessments/{id}/questions` | Fetch sanitized 40 assessment questions | Student |
| | `POST /api/v1/assessments/{id}/submit` | Submit answers & calculate skill scores | Student |
| **Skill Gaps** | `GET /api/v1/skill-gaps` | Fetch active skill gap deficits | Student |
| **Recommendations** | `GET /api/v1/recommendations/personalized` | Get AI recommendations with explanations | Student |
| **Learning Path** | `POST /api/v1/learning-paths/generate` | Generate prerequisite-aware course roadmap | Student |
| **Learning Progress** | `POST /api/v1/courses/{id}/enroll` | Enroll in a course | Student |
| | `GET /api/v1/courses/{id}/learning` | Fetch course reader modules and lessons | Student |
| | `POST /api/v1/courses/{id}/lessons/{lesson_id}/complete` | Mark lesson complete & update progress % | Student |
| | `GET /api/v1/learning/continue` | Fetch active course & next incomplete lesson | Student |
| | `GET /api/v1/learning/dashboard-stats` | Fetch completed/in-progress course stats | Student |
| **AI Tutor** | `POST /api/v1/ai-tutor/chat` | Query contextualized AI Tutor assistant | Student |
| **Admin** | `GET /api/v1/admin/dashboard` | High-level system KPI metrics & trends | **Admin Only** |
| | `GET /api/v1/admin/students` | Filterable, searchable student directory | **Admin Only** |
| | `GET /api/v1/admin/students/{id}` | 360° student assessment, gap, path & progress | **Admin Only** |
| | `PATCH /api/v1/admin/students/{id}/status` | Activate or deactivate student account | **Admin Only** |
| | `GET /api/v1/admin/courses` | Course catalog with enrolled & status data | **Admin Only** |
| | `POST /api/v1/admin/courses` | Create new course with modules/skills | **Admin Only** |
| | `PUT /api/v1/admin/courses/{id}` | Update existing course attributes | **Admin Only** |
| | `PATCH /api/v1/admin/courses/{id}/status` | Toggle course active status | **Admin Only** |
| | `GET /api/v1/admin/progress` | Supervise course completion across learners | **Admin Only** |
| | `PATCH /api/v1/admin/progress/{id}` | Audited administrative progress adjustment | **Admin Only** |
| | `GET /api/v1/admin/analytics` | Real PostgreSQL/SQLite system-wide metrics | **Admin Only** |
| | `GET /api/v1/admin/activity` | Filterable administrative audit trail | **Admin Only** |

---

## 🎓 Academic Scope & Limitations

This project is built specifically as a **College Final Year Project Demonstration**. It prioritizes functional stability, data-driven explainability, clean software architecture, and full test coverage over unnecessary enterprise microservices or external cloud dependencies.
