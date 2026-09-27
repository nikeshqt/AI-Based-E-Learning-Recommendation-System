import { apiClient } from './api';
import type { Course } from '../types/course';

export const fetchCourseCatalog = async (category?: string): Promise<Course[]> => {
  const response = await apiClient.get<Course[]>('/catalog/courses', {
    params: { category },
  });
  return response.data;
};

export const fetchCourseDetails = async (courseId: string): Promise<Course> => {
  const response = await apiClient.get<Course>(`/catalog/courses/${courseId}`);
  return response.data;
};
