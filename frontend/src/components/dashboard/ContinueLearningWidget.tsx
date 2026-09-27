import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { PlayCircle, CheckCircle2, BookOpen, Clock } from 'lucide-react';
import { fetchDashboardStats } from '../../services/courseLearningService';
import type { DashboardStatsResponse } from '../../types/courseLearning';

export const ContinueLearningWidget: React.FC = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState<DashboardStatsResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    let isMounted = true;
    const loadStats = async () => {
      try {
        const data = await fetchDashboardStats();
        if (isMounted) setStats(data);
      } catch (err) {
        console.error('Failed to load dashboard stats:', err);
      } finally {
        if (isMounted) setLoading(false);
      }
    };
    loadStats();
    return () => {
      isMounted = false;
    };
  }, []);

  if (loading) {
    return (
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs animate-pulse">
        <div className="h-4 bg-slate-200 rounded w-1/3 mb-4"></div>
        <div className="h-12 bg-slate-100 rounded"></div>
      </div>
    );
  }

  const continueData = stats?.continue_learning;
  const hasActive = continueData?.has_active_course && continueData?.course_id;

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs space-y-4">
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div className="flex items-center space-x-2">
          <BookOpen className="w-5 h-5 text-indigo-600" />
          <h3 className="font-semibold text-slate-900 text-sm">Course Learning & Progress</h3>
        </div>
        <div className="flex items-center space-x-3 text-xs font-medium text-slate-600">
          <span className="flex items-center space-x-1">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span>{stats?.completed_courses_count || 0} Completed</span>
          </span>
          <span className="text-slate-300">•</span>
          <span className="flex items-center space-x-1">
            <PlayCircle className="w-4 h-4 text-indigo-600" />
            <span>{stats?.in_progress_courses_count || 0} In Progress</span>
          </span>
        </div>
      </div>

      {hasActive ? (
        <div className="bg-slate-50 border border-slate-200 rounded-lg p-4 space-y-3">
          <div className="flex items-start justify-between">
            <div>
              <span className="text-[11px] font-semibold uppercase tracking-wider text-indigo-600">
                ACTIVE COURSE
              </span>
              <h4 className="text-base font-bold text-slate-900 leading-snug">
                {continueData.course_title}
              </h4>
            </div>
            <span className="text-xs font-bold text-indigo-600 bg-indigo-50 border border-indigo-100 px-2.5 py-1 rounded-full">
              {Math.round(continueData.progress_percentage || 0)}% Done
            </span>
          </div>

          <div className="w-full h-2 bg-slate-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-indigo-600 rounded-full transition-all duration-300"
              style={{ width: `${continueData.progress_percentage || 0}%` }}
            />
          </div>

          <div className="flex items-center justify-between pt-1 text-xs">
            <div className="flex items-center space-x-2 text-slate-600">
              <Clock className="w-3.5 h-3.5 text-slate-400" />
              <span>
                Next: <strong className="text-slate-800">{continueData.next_lesson_title || 'Continue Lesson'}</strong>
              </span>
            </div>
            <button
              onClick={() => navigate(`/courses/${continueData.course_id}/learn`)}
              className="px-3.5 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg text-xs transition-colors flex items-center space-x-1 shadow-xs"
            >
              <span>Continue Learning</span>
              <span>→</span>
            </button>
          </div>
        </div>
      ) : (
        <div className="bg-slate-50 border border-slate-200 rounded-lg p-4 text-center space-y-2">
          <p className="text-xs text-slate-600">No active course in progress.</p>
          <button
            onClick={() => navigate('/catalog')}
            className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold rounded-lg transition-colors inline-block"
          >
            Explore Catalog & Enroll
          </button>
        </div>
      )}
    </div>
  );
};
