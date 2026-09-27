import { apiClient } from './api';
import type { SkillGapResponse, SkillGapDetailResponse } from '../types/skillGap';

export const fetchUserSkillGaps = async (token?: string): Promise<SkillGapResponse> => {
  const authToken = token || localStorage.getItem('token');
  const headers = authToken ? { Authorization: `Bearer ${authToken}` } : {};
  const response = await apiClient.get<SkillGapResponse>('/skill-gaps', { headers });
  return response.data;
};

export const fetchSkillGapDetail = async (
  skillId: string,
  token?: string
): Promise<SkillGapDetailResponse> => {
  const authToken = token || localStorage.getItem('token');
  const headers = authToken ? { Authorization: `Bearer ${authToken}` } : {};
  const response = await apiClient.get<SkillGapDetailResponse>(`/skill-gaps/${skillId}`, {
    headers,
  });
  return response.data;
};
