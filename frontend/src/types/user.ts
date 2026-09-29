export interface UserSkillMastery {
  skill_id: string;
  skill_name: string;
  mastery_score: number; // 0.0 to 1.0
  last_evaluated: string;
  category: string;
}

export interface UserProfile {
  user_id: string;
  full_name: string;
  email: string;
  role?: 'student' | 'admin';
  is_active?: boolean;
  last_login?: string;
  created_at?: string;
  avatar_url?: string;
  learning_goal: string;
  preferred_learning_style: 'visual' | 'reading' | 'practical' | 'auditory';
  skill_level: 'beginner' | 'intermediate' | 'advanced';
  skills: UserSkillMastery[];
  weekly_goal_hours: number;
  completed_hours: number;
  streak_days: number;
}
