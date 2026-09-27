import { apiClient } from './api';
import type { UserProfile } from '../types/user';

export const getUserProfile = async (userId: string): Promise<UserProfile> => {
  const response = await apiClient.get<UserProfile>(`/users/${userId}`);
  return response.data;
};

export const updateUserGoal = async (userId: string, goal: string): Promise<UserProfile> => {
  const response = await apiClient.put<UserProfile>(`/users/${userId}/goal`, { learning_goal: goal });
  return response.data;
};
