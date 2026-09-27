import React from 'react';
import type { Course } from '../../types/course';
import { X, Clock, PlayCircle, CheckCircle2, Award, UserCheck } from 'lucide-react';
import { formatDuration } from '../../utils/formatters';

interface CourseDetailModalProps {
  course: Course | null;
  onClose: () => void;
}

export const CourseDetailModal: React.FC<CourseDetailModalProps> = ({ course, onClose }) => {
  if (!course) return null;

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white border border-slate-200 rounded-xl max-w-2xl w-full p-6 space-y-5 max-h-[90vh] overflow-y-auto relative shadow-lg">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        <div>
          <span className="text-xs font-semibold uppercase tracking-wider text-indigo-700 px-2.5 py-0.5 rounded-full bg-indigo-50 border border-indigo-100">
            {course.category} • {course.difficulty_level}
          </span>
          <h2 className="text-xl font-bold text-slate-900 mt-2">{course.title}</h2>
          <p className="text-xs text-slate-500 mt-1">Instructor: <span className="text-slate-800 font-medium">{course.instructor_name}</span></p>
        </div>

        <p className="text-sm text-slate-700 leading-relaxed">{course.description}</p>

        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700">
          <div>
            <span className="text-slate-500 block text-[11px]">Duration</span>
            <span className="font-semibold text-slate-900 flex items-center gap-1 mt-0.5">
              <Clock className="w-3.5 h-3.5 text-indigo-600" />
              {formatDuration(course.duration_hours)}
            </span>
          </div>
          <div>
            <span className="text-slate-500 block text-[11px]">Rating</span>
            <span className="font-semibold text-slate-900 flex items-center gap-1 mt-0.5">
              <Award className="w-3.5 h-3.5 text-amber-500" />
              {course.rating.toFixed(1)} / 5.0
            </span>
          </div>
          <div>
            <span className="text-slate-500 block text-[11px]">Prerequisites</span>
            <span className="font-semibold text-emerald-700 flex items-center gap-1 mt-0.5">
              <UserCheck className="w-3.5 h-3.5" />
              Verified Eligible
            </span>
          </div>
        </div>

        <div>
          <h3 className="text-sm font-bold text-slate-900 mb-2">Skills You Will Acquire</h3>
          <div className="flex flex-wrap gap-2">
            {course.skills_taught.map((skill) => (
              <span
                key={skill}
                className="text-xs px-2.5 py-1 rounded-full bg-indigo-50 border border-indigo-100 text-indigo-700 font-medium"
              >
                {skill}
              </span>
            ))}
          </div>
        </div>

        <div>
          <h3 className="text-sm font-bold text-slate-900 mb-2">Course Modules & Lessons</h3>
          <div className="space-y-2">
            {course.lessons.length > 0 ? (
              course.lessons.map((lesson) => (
                <div
                  key={lesson.lesson_id}
                  className="p-3 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-between text-xs text-slate-800"
                >
                  <div className="flex items-center gap-2.5">
                    <PlayCircle className="w-4 h-4 text-indigo-600" />
                    <span className="font-medium">{lesson.title}</span>
                  </div>
                  <span className="text-slate-500">{lesson.duration_minutes} mins</span>
                </div>
              ))
            ) : (
              <div className="p-3.5 rounded-lg bg-slate-50 border border-slate-200 text-xs text-slate-500 text-center">
                Interactive video lessons and quizzes ready for enrollment.
              </div>
            )}
          </div>
        </div>

        <div className="pt-2 flex gap-3">
          <button className="flex-1 py-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-xs font-semibold text-white transition-colors flex items-center justify-center gap-1.5">
            <CheckCircle2 className="w-4 h-4" /> Enroll Now
          </button>
          <button
            onClick={onClose}
            className="px-4 py-2.5 rounded-lg bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 text-xs font-medium"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
