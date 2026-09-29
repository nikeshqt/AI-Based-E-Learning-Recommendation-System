import React, { useEffect, useState } from 'react';
import {
  Users,
  BookOpen,
  GraduationCap,
  CheckCircle2,
  TrendingUp,
  Award,
  ArrowRight,
  Activity,
  UserCheck,
} from 'lucide-react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  BarChart,
  Bar,
} from 'recharts';
import { adminApi } from '../../services/adminApi';
import type { AdminDashboardStats } from '../../types/admin';

interface AdminDashboardPageProps {
  onNavigateToTab: (tab: 'students' | 'courses' | 'progress' | 'analytics' | 'activity') => void;
}

export const AdminDashboardPage: React.FC<AdminDashboardPageProps> = ({ onNavigateToTab }) => {
  const [stats, setStats] = useState<AdminDashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStats = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await adminApi.getDashboardStats();
      setStats(data);
    } catch (err: any) {
      console.error('Failed to load admin stats:', err);
      setError(err?.response?.data?.detail || 'Failed to load system metrics.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="flex items-center space-x-3 text-slate-500">
          <div className="w-5 h-5 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
          <span className="text-sm font-medium">Loading administrative overview...</span>
        </div>
      </div>
    );
  }

  if (error || !stats) {
    return (
      <div className="bg-rose-50 border border-rose-200 rounded-xl p-6 text-center text-rose-700 font-sans">
        <p className="font-semibold text-sm mb-2">Unable to load dashboard metrics</p>
        <p className="text-xs text-rose-600 mb-4">{error}</p>
        <button
          onClick={fetchStats}
          className="px-4 py-2 bg-rose-600 text-white text-xs font-semibold rounded-lg hover:bg-rose-700 transition-colors cursor-pointer"
        >
          Retry
        </button>
      </div>
    );
  }

  const metricCards = [
    {
      label: 'Total Students',
      value: stats.total_students,
      icon: Users,
      color: 'text-indigo-600',
      bgColor: 'bg-indigo-50',
      action: () => onNavigateToTab('students'),
    },
    {
      label: 'Active Students',
      value: stats.active_students,
      icon: UserCheck,
      color: 'text-emerald-600',
      bgColor: 'bg-emerald-50',
      action: () => onNavigateToTab('students'),
    },
    {
      label: 'Total Courses',
      value: stats.total_courses,
      icon: BookOpen,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      action: () => onNavigateToTab('courses'),
    },
    {
      label: 'Total Enrollments',
      value: stats.total_enrollments,
      icon: GraduationCap,
      color: 'text-violet-600',
      bgColor: 'bg-violet-50',
      action: () => onNavigateToTab('progress'),
    },
    {
      label: 'Courses Completed',
      value: stats.courses_completed,
      icon: CheckCircle2,
      color: 'text-teal-600',
      bgColor: 'bg-teal-50',
      action: () => onNavigateToTab('progress'),
    },
    {
      label: 'Avg Course Progress',
      value: `${stats.avg_course_progress}%`,
      icon: TrendingUp,
      color: 'text-amber-600',
      bgColor: 'bg-amber-50',
      action: () => onNavigateToTab('progress'),
    },
    {
      label: 'Assessment Completion',
      value: `${stats.assessment_completion_rate}%`,
      icon: Award,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
      action: () => onNavigateToTab('students'),
    },
  ];

  return (
    <div className="space-y-6 font-sans">
      {/* Header Banner */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">System Administrator Dashboard</h2>
          <p className="text-xs text-slate-500 mt-1">
            Real-time overview of learner engagement, curriculum progress, and recommendation platform metrics.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => onNavigateToTab('students')}
            className="inline-flex items-center gap-1.5 px-3.5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold rounded-lg shadow-xs transition-colors cursor-pointer"
          >
            Manage Students
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => onNavigateToTab('courses')}
            className="inline-flex items-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-semibold rounded-lg transition-colors cursor-pointer"
          >
            Course Catalog
          </button>
        </div>
      </div>

      {/* 7 Summary Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3">
        {metricCards.map((card, idx) => {
          const Icon = card.icon;
          return (
            <div
              key={idx}
              onClick={card.action}
              className="bg-white border border-slate-200 rounded-xl p-4 shadow-xs hover:border-indigo-300 transition-all cursor-pointer flex flex-col justify-between"
            >
              <div className="flex items-center justify-between mb-3">
                <span className="text-[11px] font-semibold text-slate-500 leading-tight">
                  {card.label}
                </span>
                <div className={`p-1.5 rounded-lg ${card.bgColor} ${card.color}`}>
                  <Icon className="w-4 h-4" />
                </div>
              </div>
              <div className="text-xl font-bold text-slate-900 tracking-tight">
                {card.value}
              </div>
            </div>
          );
        })}
      </div>

      {/* Visualizations Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Enrollment Trend Chart */}
        <div className="lg:col-span-2 bg-white border border-slate-200 rounded-xl p-5 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Enrollment Activity Trend</h3>
              <p className="text-xs text-slate-500">Student enrollment flow over recent time periods</p>
            </div>
            <button
              onClick={() => onNavigateToTab('analytics')}
              className="text-xs font-semibold text-indigo-600 hover:text-indigo-800 cursor-pointer"
            >
              Full Analytics →
            </button>
          </div>
          <div className="h-64 w-full">
            {stats.enrollment_trends.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={stats.enrollment_trends}>
                  <defs>
                    <linearGradient id="enrollmentGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#4F46E5" stopOpacity={0.2} />
                      <stop offset="95%" stopColor="#4F46E5" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="date" tick={{ fontSize: 11, fill: '#64748B' }} stroke="#CBD5E1" />
                  <YAxis tick={{ fontSize: 11, fill: '#64748B' }} stroke="#CBD5E1" allowDecimals={false} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#FFFFFF',
                      borderRadius: '8px',
                      border: '1px solid #E2E8F0',
                      fontSize: '12px',
                    }}
                  />
                  <Area
                    type="monotone"
                    dataKey="enrollments"
                    stroke="#4F46E5"
                    strokeWidth={2}
                    fillOpacity={1}
                    fill="url(#enrollmentGrad)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-full text-xs text-slate-400">
                No enrollment trend data recorded yet.
              </div>
            )}
          </div>
        </div>

        {/* Career Goals Breakdown */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Career Goal Distribution</h3>
              <p className="text-xs text-slate-500">Learner career objectives</p>
            </div>
          </div>
          <div className="h-64 w-full">
            {stats.goal_distribution.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={stats.goal_distribution} layout="vertical" margin={{ left: 10 }}>
                  <XAxis type="number" tick={{ fontSize: 10, fill: '#64748B' }} stroke="#CBD5E1" />
                  <YAxis
                    dataKey="name"
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
                  <Bar dataKey="value" fill="#6366F1" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-full text-xs text-slate-400">
                No career goal data available yet.
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Recent Activity Log Strip */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-indigo-600" />
            <h3 className="text-sm font-bold text-slate-900">Recent Administrative Activity</h3>
          </div>
          <button
            onClick={() => onNavigateToTab('activity')}
            className="text-xs font-semibold text-indigo-600 hover:text-indigo-800 cursor-pointer"
          >
            View All Audit Logs →
          </button>
        </div>

        {stats.recent_activity.length > 0 ? (
          <div className="divide-y divide-slate-100">
            {stats.recent_activity.map((act) => (
              <div key={act.log_id} className="py-2.5 flex items-center justify-between text-xs">
                <div className="flex items-center gap-3">
                  <span className="px-2 py-0.5 rounded font-mono text-[10px] font-semibold bg-slate-100 text-slate-700">
                    {act.action}
                  </span>
                  <span className="text-slate-800 font-medium">{act.details || 'Administrative event'}</span>
                </div>
                <div className="text-slate-400 text-[11px] whitespace-nowrap ml-4">
                  {new Date(act.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} •{' '}
                  {new Date(act.timestamp).toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="py-6 text-center text-xs text-slate-400">
            No administrative activity yet.
          </div>
        )}
      </div>
    </div>
  );
};
