export interface AdminActivityItem {
  log_id: string;
  admin_id?: string;
  admin_name?: string;
  admin_email?: string;
  action: string;
  target_type?: string;
  target_id?: string;
  details?: string;
  timestamp: string;
}

export interface AdminDashboardStats {
  total_students: number;
  active_students: number;
  total_courses: number;
  total_enrollments: number;
  courses_completed: number;
  avg_course_progress: number;
  assessment_completion_rate: number;
  recent_activity: AdminActivityItem[];
  enrollment_trends: { date: string; enrollments: number }[];
  goal_distribution: { name: string; value: number }[];
}

export interface AdminStudentListItem {
  user_id: string;
  full_name: string;
  email: string;
  career_goal: string;
  skill_level: string;
  role: string;
  is_active: boolean;
  created_at?: string;
  last_login?: string;
  assessment_status: string; // 'Completed' | 'Not Completed'
  assessment_score?: number;
  enrolled_courses_count: number;
  overall_progress: number;
}

export interface AdminStudentListResponse {
  total: number;
  students: AdminStudentListItem[];
}

export interface StudentProfileSection {
  user_id: string;
  full_name: string;
  email: string;
  career_goal: string;
  preferred_learning_style: string;
  skill_level: string;
  is_active: boolean;
  role: string;
  registration_date?: string;
  last_login?: string;
}

export interface StudentAssessmentSection {
  completed: boolean;
  overall_score?: number;
  topic_scores: Record<string, number>;
  difficulty_performance: Record<string, number>;
  skill_proficiency: Record<string, string>;
  total_questions: number;
  correct_answers: number;
  submitted_at?: string;
}

export interface StudentSkillGapSection {
  skill: string;
  current_mastery: number;
  target_mastery: number;
  gap: number;
  priority: number;
  category: string;
}

export interface StudentRecommendationSection {
  course_id: string;
  title: string;
  match_score: number;
  recommendation_reason: string;
  target_skill_gap?: string;
}

export interface StudentLearningPathStage {
  stage_number: number;
  stage_title: string;
  course_id: string;
  course_title: string;
  status: string;
  target_skill?: string;
}

export interface StudentLearningPathSection {
  path_id?: string;
  title?: string;
  overall_readiness: number;
  is_active: boolean;
  stages: StudentLearningPathStage[];
}

export interface StudentCourseProgressSection {
  course_id: string;
  course_title: string;
  category: string;
  enrollment_date?: string;
  progress_percentage: number;
  completed_lessons: number;
  total_lessons: number;
  completion_status: string;
  last_activity?: string;
}

export interface AdminStudentDetailResponse {
  profile: StudentProfileSection;
  assessment: StudentAssessmentSection;
  skill_gaps: StudentSkillGapSection[];
  recommendations: StudentRecommendationSection[];
  learning_path?: StudentLearningPathSection;
  course_progress: StudentCourseProgressSection[];
}

export interface AdminCourseItem {
  course_id: string;
  title: string;
  description: string;
  instructor_name: string;
  category: string;
  difficulty_level: string;
  duration_hours: number;
  rating: number;
  enrolled_count: number;
  is_active: boolean;
  prerequisites: string[];
  skills_taught: string[];
  modules_count: number;
  lessons_count: number;
  created_at?: string;
}

export interface AdminCourseCreatePayload {
  title: string;
  description: string;
  category: string;
  difficulty_level: string;
  duration_hours: number;
  instructor_name: string;
  prerequisites: string[];
  skills_taught: string[];
}

export interface AdminProgressItem {
  enrollment_id: string;
  student_id: string;
  student_name: string;
  student_email: string;
  course_id: string;
  course_title: string;
  progress_percentage: number;
  completed_lessons: number;
  total_lessons: number;
  started_date?: string;
  last_activity?: string;
  status: string;
}

export interface AdminAnalyticsResponse {
  student_analytics: {
    total_students: number;
    new_registrations: number;
    active_students: number;
    assessment_completion_rate: number;
  };
  course_analytics: {
    total_courses: number;
    most_enrolled_courses: { course_id: string; title: string; enrollments: number }[];
    most_completed_courses: { course_id: string; title: string; completions: number }[];
    average_completion_percentage: number;
  };
  learning_analytics: {
    average_student_progress: number;
    active_learners_count: number;
    completed_courses_count: number;
    incomplete_learning_paths_count: number;
  };
  skill_analytics: {
    most_common_skill_gaps: { skill: string; avg_gap: number; current_mastery: number }[];
    skill_distribution: { skill: string; average_mastery: number }[];
    career_goal_distribution: { career_goal: string; student_count: number }[];
  };
}
