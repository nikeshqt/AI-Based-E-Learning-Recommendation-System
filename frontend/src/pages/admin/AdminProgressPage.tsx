import React, { useEffect, useState } from 'react';
import {
  TrendingUp,
  Search,
  Filter,
  Edit3,
} from 'lucide-react';
import { adminApi } from '../../services/adminApi';
import type { AdminProgressItem } from '../../types/admin';

export const AdminProgressPage: React.FC = () => {
  const [records, setRecords] = useState<AdminProgressItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters
  const [searchStudent, setSearchStudent] = useState('');
  const [filterCourse, setFilterCourse] = useState('');
  const [filterStatus, setFilterStatus] = useState('');

  // Correction Modal
  const [adjustingRecord, setAdjustingRecord] = useState<AdminProgressItem | null>(null);
  const [newProgress, setNewProgress] = useState<number>(0);
  const [newStatus, setNewStatus] = useState<string>('IN_PROGRESS');
  const [adjustmentReason, setAdjustmentReason] = useState<string>('');
  const [submittingCorrection, setSubmittingCorrection] = useState(false);

  const fetchProgress = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await adminApi.getProgress({
        student_id: searchStudent || undefined,
        course_id: filterCourse || undefined,
        status: filterStatus || undefined,
      });
      setRecords(data);
    } catch (err: any) {
      console.error('Failed to load progress records:', err);
      setError(err?.response?.data?.detail || 'Failed to fetch course progress.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProgress();
  }, [filterCourse, filterStatus]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchProgress();
  };

  const openAdjustmentModal = (record: AdminProgressItem) => {
    setAdjustingRecord(record);
    setNewProgress(record.progress_percentage);
    setNewStatus(record.status);
    setAdjustmentReason('');
  };

  const handleCorrectionSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!adjustingRecord) return;

    try {
      setSubmittingCorrection(true);
      const updated = await adminApi.updateProgress(adjustingRecord.enrollment_id, {
        progress_percentage: Number(newProgress),
        status: newStatus,
        reason: adjustmentReason || 'Administrative adjustment',
      });
      setRecords((prev) =>
        prev.map((r) => (r.enrollment_id === adjustingRecord.enrollment_id ? updated : r))
      );
      setAdjustingRecord(null);
    } catch (err: any) {
      alert(err?.response?.data?.detail || 'Failed to update student progress.');
    } finally {
      setSubmittingCorrection(false);
    }
  };

  // Distinct courses for filter dropdown
  const uniqueCourses = Array.from(new Set(records.map((r) => r.course_title)));

  return (
    <div className="space-y-6 font-sans">
      {/* Header */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-indigo-600" />
            <h2 className="text-xl font-bold text-slate-900 tracking-tight">
              Course Progress Management
            </h2>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Supervise lesson completion telemetry, inspect learner pacing, and perform audited administrative corrections.
          </p>
        </div>
        <div className="text-xs font-semibold text-slate-600 bg-slate-50 border border-slate-200 px-3 py-1.5 rounded-lg">
          Active Enrollments: <span className="text-indigo-600 font-bold">{records.length}</span>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-xs space-y-3">
        <form onSubmit={handleSearchSubmit} className="flex flex-col md:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              value={searchStudent}
              onChange={(e) => setSearchStudent(e.target.value)}
              placeholder="Search by student ID, name, or course title..."
              className="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:border-indigo-500"
            />
          </div>
          <button
            type="submit"
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold rounded-lg shadow-xs transition-colors cursor-pointer"
          >
            Search
          </button>
        </form>

        <div className="flex flex-wrap items-center gap-3 pt-2 border-t border-slate-100 text-xs">
          <div className="flex items-center gap-1.5 text-slate-500 font-medium">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            Filters:
          </div>

          <select
            value={filterCourse}
            onChange={(e) => setFilterCourse(e.target.value)}
            className="px-2.5 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-700 text-xs focus:outline-none"
          >
            <option value="">All Courses</option>
            {uniqueCourses.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>

          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="px-2.5 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-700 text-xs focus:outline-none"
          >
            <option value="">All Statuses</option>
            <option value="ENROLLED">Enrolled</option>
            <option value="IN_PROGRESS">In Progress</option>
            <option value="COMPLETED">Completed</option>
          </select>
        </div>
      </div>

      {/* Progress Records Table */}
      <div className="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center p-12 text-slate-500">
            <div className="w-5 h-5 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin mr-3"></div>
            <span className="text-xs font-medium">Loading course progress records...</span>
          </div>
        ) : error ? (
          <div className="p-8 text-center text-xs text-rose-600">{error}</div>
        ) : records.length === 0 ? (
          <div className="p-12 text-center">
            <TrendingUp className="w-10 h-10 text-slate-300 mx-auto mb-3" />
            <p className="text-sm font-semibold text-slate-700">No course progress records found.</p>
            <p className="text-xs text-slate-400 mt-1">Student course enrollments will appear here.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold uppercase tracking-wider text-[11px]">
                <tr>
                  <th className="py-3 px-4">Student</th>
                  <th className="py-3 px-4">Course</th>
                  <th className="py-3 px-4">Progress %</th>
                  <th className="py-3 px-4">Completed Lessons</th>
                  <th className="py-3 px-4">Started Date</th>
                  <th className="py-3 px-4">Last Activity</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Adjustment</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {records.map((item) => (
                  <tr key={item.enrollment_id} className="hover:bg-slate-50 transition-colors">
                    <td className="py-3.5 px-4">
                      <div className="font-semibold text-slate-900">{item.student_name}</div>
                      <div className="text-[11px] text-slate-400 font-mono">{item.student_email}</div>
                    </td>
                    <td className="py-3.5 px-4 font-medium text-slate-800">{item.course_title}</td>
                    <td className="py-3.5 px-4">
                      <div className="w-28 space-y-1">
                        <span className="font-semibold text-slate-800">{item.progress_percentage}%</span>
                        <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                          <div
                            className="bg-indigo-600 h-full rounded-full"
                            style={{ width: `${item.progress_percentage}%` }}
                          />
                        </div>
                      </div>
                    </td>
                    <td className="py-3.5 px-4 text-slate-600">
                      {item.completed_lessons} / {item.total_lessons}
                    </td>
                    <td className="py-3.5 px-4 text-slate-500 whitespace-nowrap">
                      {item.started_date ? new Date(item.started_date).toLocaleDateString() : 'N/A'}
                    </td>
                    <td className="py-3.5 px-4 text-slate-500 whitespace-nowrap">
                      {item.last_activity ? new Date(item.last_activity).toLocaleString() : 'N/A'}
                    </td>
                    <td className="py-3.5 px-4">
                      <span
                        className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold uppercase ${
                          item.status === 'COMPLETED'
                            ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                            : 'bg-indigo-50 text-indigo-700 border border-indigo-200'
                        }`}
                      >
                        {item.status}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <button
                        onClick={() => openAdjustmentModal(item)}
                        title="Administrative Progress Correction"
                        className="inline-flex items-center gap-1 px-2.5 py-1 text-slate-600 hover:text-indigo-600 hover:bg-slate-100 border border-slate-200 rounded-lg text-xs font-semibold transition-colors cursor-pointer"
                      >
                        <Edit3 className="w-3.5 h-3.5" />
                        Adjust
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Administrative Progress Adjustment Modal */}
      {adjustingRecord && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white border border-slate-200 rounded-2xl max-w-md w-full p-6 shadow-xl space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <h3 className="text-base font-bold text-slate-900">
                Administrative Progress Correction
              </h3>
              <button
                onClick={() => setAdjustingRecord(null)}
                className="text-slate-400 hover:text-slate-600 text-sm cursor-pointer"
              >
                ✕
              </button>
            </div>

            <p className="text-xs text-slate-600">
              Adjust progress for <strong>{adjustingRecord.student_name}</strong> in{' '}
              <strong>{adjustingRecord.course_title}</strong>. An administrative audit log will be
              recorded automatically.
            </p>

            <form onSubmit={handleCorrectionSubmit} className="space-y-4 text-xs">
              <div>
                <label className="block text-slate-700 font-semibold mb-1">
                  Progress Percentage (0 - 100%)
                </label>
                <input
                  type="number"
                  min="0"
                  max="100"
                  step="1"
                  required
                  value={newProgress}
                  onChange={(e) => setNewProgress(parseFloat(e.target.value))}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 focus:outline-none focus:border-indigo-500 font-mono"
                />
              </div>

              <div>
                <label className="block text-slate-700 font-semibold mb-1">Status</label>
                <select
                  value={newStatus}
                  onChange={(e) => setNewStatus(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 focus:outline-none focus:border-indigo-500"
                >
                  <option value="ENROLLED">ENROLLED</option>
                  <option value="IN_PROGRESS">IN_PROGRESS</option>
                  <option value="COMPLETED">COMPLETED</option>
                </select>
              </div>

              <div>
                <label className="block text-slate-700 font-semibold mb-1">
                  Reason for Administrative Correction *
                </label>
                <textarea
                  rows={2}
                  required
                  value={adjustmentReason}
                  onChange={(e) => setAdjustmentReason(e.target.value)}
                  placeholder="e.g., Credit granted for prior external lab completion..."
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setAdjustingRecord(null)}
                  className="px-3.5 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-lg transition-colors cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submittingCorrection}
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold rounded-lg shadow-xs transition-colors cursor-pointer"
                >
                  {submittingCorrection ? 'Recording Audit...' : 'Save & Record Audit'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
