export interface CourseLesson {
  lesson_id: string;
  title: string;
  duration_minutes: number;
  video_url?: string;
  is_completed: boolean;
}

export interface Course {
  course_id: string;
  title: string;
  description: string;
  instructor_name: string;
  thumbnail_url: string;
  category: string;
  difficulty_level: 'Beginner' | 'Intermediate' | 'Advanced';
  duration_hours: number;
  rating: number;
  enrolled_count: number;
  prerequisites: string[];
  skills_taught: string[];
  lessons: CourseLesson[];
}
