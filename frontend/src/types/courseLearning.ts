export interface EnrollmentResponse {
  enrollment_id: string;
  user_id: string;
  course_id: string;
  status: string;
  progress_percentage: number;
  enrolled_at: string;
  completed_at?: string;
}

export interface LessonPublicSchema {
  lesson_id: string;
  module_id: string;
  course_id: string;
  title: string;
  description?: string;
  content?: string;
  order_index: number;
  estimated_duration_minutes: number;
  is_completed: boolean;
}

export interface ModulePublicSchema {
  module_id: string;
  course_id: string;
  title: string;
  order_index: number;
  lessons: LessonPublicSchema[];
}

export interface CourseLearningResponse {
  course_id: string;
  title: string;
  category: string;
  difficulty_level: string;
  duration_hours: number;
  status: string;
  progress_percentage: number;
  completed_lessons_count: number;
  total_lessons_count: number;
  modules: ModulePublicSchema[];
}

export interface LessonCompleteResponse {
  lesson_id: string;
  course_id: string;
  is_completed: boolean;
  progress_percentage: number;
  course_completed: boolean;
  status: string;
}

export interface ContinueLearningResponse {
  has_active_course: boolean;
  course_id?: string;
  course_title?: string;
  progress_percentage?: number;
  next_lesson_id?: string;
  next_lesson_title?: string;
  estimated_duration_minutes?: number;
}

export interface DashboardStatsResponse {
  completed_courses_count: number;
  in_progress_courses_count: number;
  continue_learning?: ContinueLearningResponse;
}
