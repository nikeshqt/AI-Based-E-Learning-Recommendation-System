import { apiClient } from './api';
import type {
  EnrollmentResponse,
  CourseLearningResponse,
  LessonCompleteResponse,
  ContinueLearningResponse,
  DashboardStatsResponse,
} from '../types/courseLearning';

export const enrollInCourse = async (
  courseId: string,
  token?: string
): Promise<EnrollmentResponse> => {
  const authToken = token || localStorage.getItem('token');
  const headers = authToken ? { Authorization: `Bearer ${authToken}` } : {};
  const response = await apiClient.post<EnrollmentResponse>(
    `/courses/${courseId}/enroll`,
    {},
    { headers }
  );
  return response.data;
};

export const fetchCourseLearningContent = async (
  courseId: string,
  token?: string
): Promise<CourseLearningResponse> => {
  const authToken = token || localStorage.getItem('token');
  const headers = authToken ? { Authorization: `Bearer ${authToken}` } : {};
  const response = await apiClient.get<CourseLearningResponse>(
    `/courses/${courseId}/learning`,
    { headers }
  );
  return response.data;
};

export const completeLesson = async (
  courseId: string,
  lessonId: string,
  token?: string
): Promise<LessonCompleteResponse> => {
  const authToken = token || localStorage.getItem('token');
  const headers = authToken ? { Authorization: `Bearer ${authToken}` } : {};
  const response = await apiClient.post<LessonCompleteResponse>(
    `/courses/${courseId}/lessons/${lessonId}/complete`,
    {},
    { headers }
  );
  return response.data;
};

export const fetchContinueLearning = async (
  token?: string
): Promise<ContinueLearningResponse> => {
  const authToken = token || localStorage.getItem('token');
  const headers = authToken ? { Authorization: `Bearer ${authToken}` } : {};
  const response = await apiClient.get<ContinueLearningResponse>(
    '/learning/continue',
    { headers }
  );
  return response.data;
};

export const fetchDashboardStats = async (
  token?: string
): Promise<DashboardStatsResponse> => {
  const authToken = token || localStorage.getItem('token');
  const headers = authToken ? { Authorization: `Bearer ${authToken}` } : {};
  const response = await apiClient.get<DashboardStatsResponse>(
    '/learning/dashboard-stats',
    { headers }
  );
  return response.data;
};
