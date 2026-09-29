import React, { useEffect, useState } from 'react';
import {
  BarChart3,
  Users,
  BookOpen,
  TrendingUp,
  Target,
  Award,
  AlertCircle,
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
} from 'recharts';
import { adminApi } from '../../services/adminApi';
import type { AdminAnalyticsResponse } from '../../types/admin';

export const AdminAnalyticsPage: React.FC = () => {
  const [data, setData] = useState<AdminAnalyticsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await adminApi.getAnalytics();
      setData(res);
    } catch (err: any) {
      console.error('Failed to load system analytics:', err);
      setError(err?.response?.data?.detail || 'Failed to aggregate system analytics.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh] text-slate-500 font-sans">
        <div className="w-5 h-5 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin mr-3"></div>
        <span className="text-sm font-medium">Aggregating real database analytics...</span>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="bg-rose-50 border border-rose-200 rounded-xl p-6 text-center text-rose-700 font-sans">
        <p className="font-semibold text-sm mb-2">Unable to load system analytics</p>
        <p className="text-xs text-rose-600 mb-4">{error}</p>
        <button
          onClick={fetchAnalytics}
          className="px-4 py-2 bg-rose-600 text-white text-xs font-semibold rounded-lg hover:bg-rose-700 transition-colors cursor-pointer"
        >
          Retry
        </button>
      </div>
    );
  }

  const { student_analytics, course_analytics, learning_analytics, skill_analytics } = data;

  const hasStudentData = student_analytics.total_students > 0;

  return (
    <div className="space-y-6 font-sans">
      {/* Header */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-indigo-600" />
            <h2 className="text-xl font-bold text-slate-900 tracking-tight">System-Wide Analytics</h2>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Aggregated institutional learning metrics, curriculum engagement rates, and skill deficit distributions.
          </p>
        </div>
      </div>

      {!hasStudentData ? (
        <div className="bg-white border border-slate-200 rounded-xl p-12 text-center shadow-xs">
          <AlertCircle className="w-10 h-10 text-slate-300 mx-auto mb-3" />
          <h3 className="text-base font-bold text-slate-800">No student data available yet.</h3>
          <p className="text-xs text-slate-500 mt-1">
            Analytics will populate dynamically as students register, take assessments, and complete course modules.
          </p>
        </div>
      ) : (
        <>
          {/* 1. STUDENT ANALYTICS */}
          <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs space-y-4">
            <div className="flex items-center gap-2 pb-3 border-b border-slate-100">
              <Users className="w-4 h-4 text-indigo-600" />
              <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wide">
                Student Analytics
              </h3>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-slate-50 p-4 rounded-xl">
                <span className="text-slate-500 text-xs block mb-1">Total Students</span>
                <span className="text-2xl font-bold text-slate-900">{student_analytics.total_students}</span>
              </div>
              <div className="bg-slate-50 p-4 rounded-xl">
                <span className="text-slate-500 text-xs block mb-1">New Registrations (30d)</span>
                <span className="text-2xl font-bold text-indigo-600">
                  {student_analytics.new_registrations}
                </span>
              </div>
              <div className="bg-slate-50 p-4 rounded-xl">
                <span className="text-slate-500 text-xs block mb-1">Active Students</span>
                <span className="text-2xl font-bold text-emerald-600">
                  {student_analytics.active_students}
                </span>
              </div>
              <div className="bg-slate-50 p-4 rounded-xl">
                <span className="text-slate-500 text-xs block mb-1">Assessment Completion Rate</span>
                <span className="text-2xl font-bold text-violet-600">
                  {student_analytics.assessment_completion_rate}%
                </span>
              </div>
            </div>
          </div>

          {/* 2. COURSE & LEARNING ANALYTICS GRID */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Course Analytics */}
            <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs space-y-4">
              <div className="flex items-center gap-2 pb-3 border-b border-slate-100">
                <BookOpen className="w-4 h-4 text-indigo-600" />
                <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wide">
                  Course Analytics
                </h3>
              </div>

              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="bg-slate-50 p-3.5 rounded-lg">
                  <span className="text-slate-500 block text-[11px]">Total Published Courses</span>
                  <span className="text-xl font-bold text-slate-900">{course_analytics.total_courses}</span>
                </div>
                <div className="bg-slate-50 p-3.5 rounded-lg">
                  <span className="text-slate-500 block text-[11px]">Avg Course Completion</span>
                  <span className="text-xl font-bold text-teal-600">
                    {course_analytics.average_completion_percentage}%
                  </span>
                </div>
              </div>

              <div>
                <h4 className="text-xs font-semibold text-slate-700 mb-2">Most Enrolled Courses</h4>
                <div className="space-y-2">
                  {course_analytics.most_enrolled_courses.slice(0, 3).map((c, i) => (
                    <div key={i} className="flex justify-between items-center text-xs bg-slate-50 p-2.5 rounded-lg">
                      <span className="font-medium text-slate-800 line-clamp-1">{c.title}</span>
                      <span className="font-bold text-indigo-600 whitespace-nowrap ml-2">
                        {c.enrollments} enrollments
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Learning Analytics */}
            <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs space-y-4">
              <div className="flex items-center gap-2 pb-3 border-b border-slate-100">
                <TrendingUp className="w-4 h-4 text-indigo-600" />
                <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wide">
                  Learning Analytics
                </h3>
              </div>

              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="bg-slate-50 p-3.5 rounded-lg">
                  <span className="text-slate-500 block text-[11px]">Average Learner Progress</span>
                  <span className="text-xl font-bold text-slate-900">
                    {learning_analytics.average_student_progress}%
                  </span>
                </div>
                <div className="bg-slate-50 p-3.5 rounded-lg">
                  <span className="text-slate-500 block text-[11px]">Active Learners</span>
                  <span className="text-xl font-bold text-indigo-600">
                    {learning_analytics.active_learners_count}
                  </span>
                </div>
                <div className="bg-slate-50 p-3.5 rounded-lg">
                  <span className="text-slate-500 block text-[11px]">Courses Completed</span>
                  <span className="text-xl font-bold text-emerald-600">
                    {learning_analytics.completed_courses_count}
                  </span>
                </div>
                <div className="bg-slate-50 p-3.5 rounded-lg">
                  <span className="text-slate-500 block text-[11px]">Incomplete Learning Paths</span>
                  <span className="text-xl font-bold text-amber-600">
                    {learning_analytics.incomplete_learning_paths_count}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* 3. SKILL ANALYTICS */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Common Skill Gaps */}
            <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs">
              <div className="flex items-center gap-2 mb-4 pb-3 border-b border-slate-100">
                <Target className="w-4 h-4 text-indigo-600" />
                <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wide">
                  Most Common Skill Gaps
                </h3>
              </div>
              {skill_analytics.most_common_skill_gaps.length > 0 ? (
                <div className="h-60 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={skill_analytics.most_common_skill_gaps}>
                      <XAxis dataKey="skill" tick={{ fontSize: 10, fill: '#64748B' }} stroke="#CBD5E1" />
                      <YAxis tick={{ fontSize: 10, fill: '#64748B' }} stroke="#CBD5E1" />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: '#FFFFFF',
                          borderRadius: '8px',
                          border: '1px solid #E2E8F0',
                          fontSize: '12px',
                        }}
                      />
                      <Bar dataKey="avg_gap" fill="#F59E0B" radius={[4, 4, 0, 0]} name="Average Gap (%)" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <div className="py-12 text-center text-xs text-slate-400">Not enough data available.</div>
              )}
            </div>

            {/* Career Goal Distribution */}
            <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs">
              <div className="flex items-center gap-2 mb-4 pb-3 border-b border-slate-100">
                <Award className="w-4 h-4 text-indigo-600" />
                <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wide">
                  Career Goal Distribution
                </h3>
              </div>
              {skill_analytics.career_goal_distribution.length > 0 ? (
                <div className="h-60 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={skill_analytics.career_goal_distribution} layout="vertical">
                      <XAxis type="number" tick={{ fontSize: 10, fill: '#64748B' }} stroke="#CBD5E1" />
                      <YAxis
                        dataKey="career_goal"
                        type="category"
                        tick={{ fontSize: 10, fill: '#475569' }}
                        stroke="#CBD5E1"
                        width={90}
                      />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: '#FFFFFF',
                          borderRadius: '8px',
                          border: '1px solid #E2E8F0',
                          fontSize: '12px',
                        }}
                      />
                      <Bar dataKey="student_count" fill="#4F46E5" radius={[0, 4, 4, 0]} name="Students" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <div className="py-12 text-center text-xs text-slate-400">Not enough data available.</div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
};
