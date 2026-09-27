export interface LearningAnalytics {
  total_learning_time_minutes: number;
  courses_completed: number;
  quizzes_passed: number;
  avg_quiz_score: number;
  monthly_progress: {
    month: string;
    hours_spent: number;
    skills_acquired: number;
  }[];
  skill_breakdown: {
    skill_name: string;
    proficiency_percentage: number;
  }[];
}
