import { apiClient } from './api';
import type { LearningPathResponse } from '../types/learningPath';

export const fetchCurrentLearningPath = async (token?: string): Promise<LearningPathResponse> => {
  const authToken = token || localStorage.getItem('token');
  const headers = authToken ? { Authorization: `Bearer ${authToken}` } : {};
  const response = await apiClient.get<LearningPathResponse>('/learning-paths/current', { headers });
  return response.data;
};

export const generateLearningPath = async (
  targetGoal?: string,
  token?: string
): Promise<LearningPathResponse> => {
  const authToken = token || localStorage.getItem('token');
  const headers = authToken ? { Authorization: `Bearer ${authToken}` } : {};
  const response = await apiClient.post<LearningPathResponse>(
    '/learning-paths/generate',
    { target_goal: targetGoal },
    { headers }
  );
  return response.data;
};

export const fetchLearningPathDetails = async (
  pathId: string,
  token?: string
): Promise<LearningPathResponse> => {
  const authToken = token || localStorage.getItem('token');
  const headers = authToken ? { Authorization: `Bearer ${authToken}` } : {};
  const response = await apiClient.get<LearningPathResponse>(`/learning-paths/${pathId}`, {
    headers,
  });
  return response.data;
};
