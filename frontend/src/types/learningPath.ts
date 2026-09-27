import type { Course } from './course';

export interface LearningPathItem {
  item_id?: string;
  path_id?: string;
  order_index: number;
  stage_number: number;
  stage_title: string;
  stage_name?: string;
  stage_description?: string;
  course_id: string;
  course_title: string;
  target_skill: string;
  skill_gap: number;
  current_mastery: number;
  target_mastery: number;
  priority_score: number;
  reason: string;
  status: 'AVAILABLE' | 'LOCKED' | 'IN_PROGRESS' | 'COMPLETED' | string;
  estimated_duration_hours: number;
  prerequisites: string[];
  skills_taught: string[];
  course?: Course;
}

export interface LearningPathStage {
  stage_number: number;
  stage_title: string;
  stage_name: string;
  description: string;
  target_skills: string[];
  estimated_duration_hours: number;
  status: string;
  courses: LearningPathItem[];
}

export interface LearningPathResponse {
  learning_path_id: string;
  user_id: string;
  career_goal: string;
  overall_readiness: number;
  total_duration_hours: number;
  total_stages: number;
  total_courses: number;
  generated_at: string;
  is_active: boolean;
  stages: LearningPathStage[];
  ordered_courses: LearningPathItem[];
}
