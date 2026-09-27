import { apiClient } from './api';

export interface AssessmentMeta {
  assessment_id: string;
  course_id?: string;
  title: string;
  description?: string;
  total_questions: number;
  time_limit_minutes: number;
}

export interface QuestionPublic {
  question_id: string;
  assessment_id: string;
  domain: string;
  difficulty: string;
  prompt: string;
  code_snippet?: string;
  options: string[];
  skill_measured: string;
}

export interface AnswerPayload {
  question_id: string;
  selected_option: string;
}

export interface AssessmentResultData {
  attempt_id: string;
  assessment_id: string;
  user_id: string;
  total_questions: number;
  answered_questions: number;
  correct_answers: number;
  incorrect_answers: number;
  overall_score: number;
  topic_scores: Record<string, number>;
  difficulty_performance: Record<string, number>;
  skill_proficiency: Record<string, string>;
  submitted_at: string;
}

export const fetchAvailableAssessments = async (): Promise<AssessmentMeta[]> => {
  const response = await apiClient.get<AssessmentMeta[]>('/assessments');
  return response.data;
};

export const fetchAssessmentQuestions = async (
  assessmentId: string,
  token?: string
): Promise<QuestionPublic[]> => {
  const headers = token ? { Authorization: `Bearer ${token}` } : {};
  const response = await apiClient.get<QuestionPublic[]>(`/assessments/${assessmentId}/questions`, {
    headers,
  });
  return response.data;
};

export const submitAssessmentAnswers = async (
  assessmentId: string,
  answers: AnswerPayload[],
  token?: string
): Promise<AssessmentResultData> => {
  const headers = token ? { Authorization: `Bearer ${token}` } : {};
  const response = await apiClient.post<AssessmentResultData>(
    `/assessments/${assessmentId}/submit`,
    { answers },
    { headers }
  );
  return response.data;
};

export const fetchLatestAssessmentResult = async (
  assessmentId: string,
  token?: string
): Promise<AssessmentResultData> => {
  const headers = token ? { Authorization: `Bearer ${token}` } : {};
  const response = await apiClient.get<AssessmentResultData>(`/assessments/${assessmentId}/results`, {
    headers,
  });
  return response.data;
};
