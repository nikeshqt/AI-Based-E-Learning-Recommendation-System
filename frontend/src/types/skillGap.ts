export interface SkillGapItem {
  skill: string;
  skill_id?: string;
  current_mastery: number;
  target_mastery: number;
  gap: number;
  priority: number;
  priority_level?: 'High' | 'Medium' | 'Low' | string;
  category: 'STRONG' | 'DEVELOPING' | 'NEEDS_IMPROVEMENT' | 'CRITICAL_GAP' | string;
  is_prerequisite?: boolean;
  importance?: number;
}

export interface SkillGapResponse {
  user_id: string;
  learning_goal: string;
  overall_readiness: number;
  skills: SkillGapItem[];
}

export interface SkillGapDetailResponse {
  skill_name: string;
  skill_id?: string;
  current_mastery: number;
  target_mastery: number;
  gap: number;
  proficiency: string;
  priority: number;
  priority_level: string;
  category: string;
  is_prerequisite: boolean;
  explanation: string;
  related_courses: string[];
  prerequisite_skills: string[];
}
