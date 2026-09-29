import { apiClient } from './api';
import type {
  AdminDashboardStats,
  AdminStudentListResponse,
  AdminStudentDetailResponse,
  AdminCourseItem,
  AdminCourseCreatePayload,
  AdminProgressItem,
  AdminAnalyticsResponse,
  AdminActivityItem,
} from '../types/admin';

export const adminApi = {
  getDashboardStats: async (): Promise<AdminDashboardStats> => {
    const res = await apiClient.get<AdminDashboardStats>('/admin/dashboard');
    return res.data;
  },

  getStudents: async (params?: {
    search?: string;
    career_goal?: string;
    assessment_status?: string;
    account_status?: string;
    sort_by?: string;
    sort_order?: string;
  }): Promise<AdminStudentListResponse> => {
    const res = await apiClient.get<AdminStudentListResponse>('/admin/students', { params });
    return res.data;
  },

  getStudentDetail: async (studentId: string): Promise<AdminStudentDetailResponse> => {
    const res = await apiClient.get<AdminStudentDetailResponse>(`/admin/students/${studentId}`);
    return res.data;
  },

  updateStudentStatus: async (
    studentId: string,
    isActive: boolean
  ): Promise<{ status: string; student_id: string; is_active: boolean }> => {
    const res = await apiClient.patch(`/admin/students/${studentId}/status`, {
      is_active: isActive,
    });
    return res.data;
  },

  getCourses: async (): Promise<AdminCourseItem[]> => {
    const res = await apiClient.get<AdminCourseItem[]>('/admin/courses');
    return res.data;
  },

  createCourse: async (payload: AdminCourseCreatePayload): Promise<AdminCourseItem> => {
    const res = await apiClient.post<AdminCourseItem>('/admin/courses', payload);
    return res.data;
  },

  updateCourse: async (
    courseId: string,
    payload: Partial<AdminCourseCreatePayload> & { is_active?: boolean }
  ): Promise<AdminCourseItem> => {
    const res = await apiClient.put<AdminCourseItem>(`/admin/courses/${courseId}`, payload);
    return res.data;
  },

  updateCourseStatus: async (
    courseId: string,
    isActive: boolean
  ): Promise<{ status: string; course_id: string; is_active: boolean }> => {
    const res = await apiClient.patch(`/admin/courses/${courseId}/status`, {
      is_active: isActive,
    });
    return res.data;
  },

  getProgress: async (params?: {
    course_id?: string;
    student_id?: string;
    status?: string;
  }): Promise<AdminProgressItem[]> => {
    const res = await apiClient.get<AdminProgressItem[]>('/admin/progress', { params });
    return res.data;
  },

  updateProgress: async (
    enrollmentId: string,
    payload: { progress_percentage?: number; status?: string; reason?: string }
  ): Promise<AdminProgressItem> => {
    const res = await apiClient.patch<AdminProgressItem>(`/admin/progress/${enrollmentId}`, payload);
    return res.data;
  },

  getAnalytics: async (): Promise<AdminAnalyticsResponse> => {
    const res = await apiClient.get<AdminAnalyticsResponse>('/admin/analytics');
    return res.data;
  },

  getActivityLogs: async (limit: number = 50): Promise<AdminActivityItem[]> => {
    const res = await apiClient.get<AdminActivityItem[]>('/admin/activity', {
      params: { limit },
    });
    return res.data;
  },
};
