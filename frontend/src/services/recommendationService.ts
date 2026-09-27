import { apiClient } from './api';
import type { RecommendationResponse, AdaptiveLearningPath } from '../types/recommendation';

export const fetchPersonalizedRecommendations = async (
  userId?: string,
  limit = 10
): Promise<RecommendationResponse> => {
  const token = localStorage.getItem('token');
  const headers = token ? { Authorization: `Bearer ${token}` } : {};

  if (!userId) {
    const response = await apiClient.get<RecommendationResponse>(
      `/recommendations/personalized?limit=${limit}`,
      { headers }
    );
    return response.data;
  }

  const response = await apiClient.post<RecommendationResponse>(
    '/recommendations/personalized',
    { user_id: userId, limit },
    { headers }
  );
  return response.data;
};

export const fetchAdaptiveLearningPath = async (
  userId: string,
  targetGoal: string
): Promise<AdaptiveLearningPath> => {
  const token = localStorage.getItem('token');
  const headers = token ? { Authorization: `Bearer ${token}` } : {};
  const response = await apiClient.post<AdaptiveLearningPath>(
    '/learning-paths/generate',
    { user_id: userId, target_goal: targetGoal },
    { headers }
  );
  return response.data;
};

export const trackUserInteractionEvent = async (eventData: {
  user_id: string;
  event_type: string;
  lesson_id?: string;
  course_id?: string;
  payload?: Record<string, unknown>;
}): Promise<void> => {
  await apiClient.post('/events/track', eventData);
};
