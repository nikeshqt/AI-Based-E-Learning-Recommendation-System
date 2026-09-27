import type { Course } from './course';

export interface RecommendationItem {
  recommendation_id: string;
  course: Course;
  match_score: number; // 0.0 to 1.0 (e.g. 0.94 -> 94%)
  recommendation_reason: string;
  stage_sources: string[];
  prerequisites_met: boolean;
  target_skill_gap: string;
  matched_skills?: string[];
  skill_gaps_addressed?: string[];
  current_skill_level?: number;
  target_skill_level?: number;
  gap?: number;
}

export interface RecommendationResponse {
  user_id: string;
  generated_at: string;
  recommendations: RecommendationItem[];
}

export interface LearningPathStage {
  stage_number: number;
  stage_title: string;
  description: string;
  target_skills: string[];
  recommended_courses: Course[];
  estimated_duration_weeks: number;
}

export interface AdaptiveLearningPath {
  path_id: string;
  path_title: string;
  overall_goal: string;
  total_duration_weeks: number;
  stages: LearningPathStage[];
}
