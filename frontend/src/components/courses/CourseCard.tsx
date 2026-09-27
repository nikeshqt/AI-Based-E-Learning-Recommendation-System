import React from 'react';
import type { Course } from '../../types/course';
import { Clock, Star, Users, BookOpen } from 'lucide-react';
import { formatDuration } from '../../utils/formatters';

interface CourseCardProps {
  course: Course;
  matchScore?: number;
  onSelect?: (courseId: string) => void;
}

export const CourseCard: React.FC<CourseCardProps> = ({ course, matchScore, onSelect }) => {
  return (
    <div
      onClick={() => onSelect && onSelect(course.course_id)}
      className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between hover:border-slate-300 shadow-xs transition-all cursor-pointer group"
    >
      <div>
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-slate-100 border border-slate-200 text-slate-700">
            {course.category}
          </span>
          {matchScore !== undefined && (
            <span className="text-xs font-bold text-indigo-600 bg-indigo-50 border border-indigo-100 px-2 py-0.5 rounded-full">
              {Math.round(matchScore * 100)}% Match
            </span>
          )}
        </div>

        <h3 className="text-base font-bold text-slate-900 group-hover:text-indigo-600 transition-colors line-clamp-2">
          {course.title}
        </h3>
        <p className="text-xs text-slate-600 mt-1 line-clamp-2">{course.description}</p>
      </div>

      <div className="mt-5 pt-3 border-t border-slate-100 space-y-3">
        <div className="flex items-center justify-between text-xs text-slate-500">
          <span className="flex items-center gap-1">
            <Clock className="w-3.5 h-3.5 text-slate-400" />
            {formatDuration(course.duration_hours)}
          </span>
          <span className="flex items-center gap-1 text-amber-600 font-semibold">
            <Star className="w-3.5 h-3.5 fill-amber-500 text-amber-500" />
            {course.rating.toFixed(1)}
          </span>
          <span className="flex items-center gap-1">
            <Users className="w-3.5 h-3.5 text-slate-400" />
            {course.enrolled_count.toLocaleString()}
          </span>
        </div>

        <div className="flex items-center gap-1.5 flex-wrap">
          {course.skills_taught.slice(0, 3).map((skill) => (
            <span
              key={skill}
              className="text-[11px] px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200 font-medium"
            >
              {skill}
            </span>
          ))}
        </div>

        <button className="w-full py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-xs font-medium text-white transition-colors flex items-center justify-center gap-1.5">
          <BookOpen className="w-3.5 h-3.5" /> View Syllabus & Lessons
        </button>
      </div>
    </div>
  );
};
