import React, { useEffect, useState } from 'react';
import {
  Search,
  Filter,
  CheckCircle2,
  Eye,
  Power,
  Users,
  Calendar,
  Clock,
  ArrowUpDown,
} from 'lucide-react';
import { adminApi } from '../../services/adminApi';
import type { AdminStudentListItem } from '../../types/admin';

interface AdminStudentsPageProps {
  onSelectStudent: (studentId: string) => void;
}

export const AdminStudentsPage: React.FC<AdminStudentsPageProps> = ({ onSelectStudent }) => {
  const [students, setStudents] = useState<AdminStudentListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters & Search
  const [search, setSearch] = useState('');
  const [careerGoal, setCareerGoal] = useState('');
  const [assessmentStatus, setAssessmentStatus] = useState('');
  const [accountStatus, setAccountStatus] = useState('');
  const [sortBy, setSortBy] = useState('created_at');
  const [sortOrder, setSortOrder] = useState('desc');

  // Deactivation confirmation modal state
  const [selectedStudentForAction, setSelectedStudentForAction] = useState<AdminStudentListItem | null>(null);
  const [actionLoading, setActionLoading] = useState(false);

  const fetchStudents = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await adminApi.getStudents({
        search: search || undefined,
        career_goal: careerGoal || undefined,
        assessment_status: assessmentStatus || undefined,
        account_status: accountStatus || undefined,
        sort_by: sortBy,
        sort_order: sortOrder,
      });
      setStudents(res.students);
    } catch (err: any) {
      console.error('Failed to load students:', err);
      setError(err?.response?.data?.detail || 'Failed to load student registry.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStudents();
  }, [careerGoal, assessmentStatus, accountStatus, sortBy, sortOrder]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchStudents();
  };

  const handleToggleStatus = async () => {
    if (!selectedStudentForAction) return;
    try {
      setActionLoading(true);
      const newStatus = !selectedStudentForAction.is_active;
      await adminApi.updateStudentStatus(selectedStudentForAction.user_id, newStatus);
      // Update local state
      setStudents((prev) =>
        prev.map((s) =>
          s.user_id === selectedStudentForAction.user_id ? { ...s, is_active: newStatus } : s
        )
      );
      setSelectedStudentForAction(null);
    } catch (err: any) {
      alert(err?.response?.data?.detail || 'Failed to update student account status.');
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div className="space-y-6 font-sans">
      {/* Header */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <Users className="w-5 h-5 text-indigo-600" />
            <h2 className="text-xl font-bold text-slate-900 tracking-tight">Student Management</h2>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Browse registered learners, inspect assessment statuses, review learning progress, and manage account access.
          </p>
        </div>
        <div className="text-xs font-semibold text-slate-600 bg-slate-50 border border-slate-200 px-3 py-1.5 rounded-lg">
          Total Learners: <span className="text-indigo-600 font-bold">{students.length}</span>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-xs space-y-3">
        <form onSubmit={handleSearchSubmit} className="flex flex-col md:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by student name or email address..."
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
            value={careerGoal}
            onChange={(e) => setCareerGoal(e.target.value)}
            className="px-2.5 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-700 text-xs focus:outline-none"
          >
            <option value="">All Career Goals</option>
            <option value="Cybersecurity Analyst">Cybersecurity Analyst</option>
            <option value="AI/ML Engineer">AI/ML Engineer</option>
            <option value="Data Science">Data Science</option>
            <option value="Software Engineering">Software Engineering</option>
          </select>

          <select
            value={assessmentStatus}
            onChange={(e) => setAssessmentStatus(e.target.value)}
            className="px-2.5 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-700 text-xs focus:outline-none"
          >
            <option value="">All Assessment Statuses</option>
            <option value="completed">Completed</option>
            <option value="not_completed">Not Completed</option>
          </select>

          <select
            value={accountStatus}
            onChange={(e) => setAccountStatus(e.target.value)}
            className="px-2.5 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-700 text-xs focus:outline-none"
          >
            <option value="">All Account Statuses</option>
            <option value="active">Active Accounts</option>
            <option value="inactive">Deactivated Accounts</option>
          </select>

          <div className="ml-auto flex items-center gap-2">
            <span className="text-slate-400 flex items-center gap-1">
              <ArrowUpDown className="w-3 h-3" /> Sort:
            </span>
            <select
              value={`${sortBy}-${sortOrder}`}
              onChange={(e) => {
                const [sb, so] = e.target.value.split('-');
                setSortBy(sb);
                setSortOrder(so);
              }}
              className="px-2.5 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-700 text-xs focus:outline-none"
            >
              <option value="created_at-desc">Newest First</option>
              <option value="created_at-asc">Oldest First</option>
              <option value="name-asc">Name (A-Z)</option>
              <option value="name-desc">Name (Z-A)</option>
              <option value="progress-desc">Highest Progress</option>
            </select>
          </div>
        </div>
      </div>

      {/* Student Table */}
      <div className="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center p-12 text-slate-500">
            <div className="w-5 h-5 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin mr-3"></div>
            <span className="text-xs font-medium">Loading student records...</span>
          </div>
        ) : error ? (
          <div className="p-8 text-center text-xs text-rose-600">{error}</div>
        ) : students.length === 0 ? (
          <div className="p-12 text-center">
            <Users className="w-10 h-10 text-slate-300 mx-auto mb-3" />
            <p className="text-sm font-semibold text-slate-700">No students registered yet.</p>
            <p className="text-xs text-slate-400 mt-1">
              {search || careerGoal || assessmentStatus || accountStatus
                ? 'Try clearing your search or filter options.'
                : 'New student registrations will appear here in real-time.'}
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold uppercase tracking-wider text-[11px]">
                <tr>
                  <th className="py-3 px-4">Student</th>
                  <th className="py-3 px-4">Career Goal</th>
                  <th className="py-3 px-4">Assessment</th>
                  <th className="py-3 px-4">Skill Level</th>
                  <th className="py-3 px-4">Progress</th>
                  <th className="py-3 px-4">Registered</th>
                  <th className="py-3 px-4">Last Login</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {students.map((student) => {
                  const isAssessed = student.assessment_status === 'Completed';
                  return (
                    <tr key={student.user_id} className="hover:bg-slate-50 transition-colors">
                      {/* Name & Email */}
                      <td className="py-3.5 px-4">
                        <div className="flex items-center gap-3">
                          <div className="w-8 h-8 rounded-full bg-indigo-100 text-indigo-700 flex items-center justify-center font-bold text-xs shrink-0">
                            {student.full_name.charAt(0).toUpperCase()}
                          </div>
                          <div>
                            <div className="font-semibold text-slate-900">{student.full_name}</div>
                            <div className="text-[11px] text-slate-400 font-mono">{student.email}</div>
                          </div>
                        </div>
                      </td>

                      {/* Goal */}
                      <td className="py-3.5 px-4 font-medium text-slate-700">
                        {student.career_goal}
                      </td>

                      {/* Assessment */}
                      <td className="py-3.5 px-4">
                        {isAssessed ? (
                          <div className="flex items-center gap-1.5 text-emerald-600 font-semibold">
                            <CheckCircle2 className="w-3.5 h-3.5" />
                            <span>
                              {student.assessment_score !== null ? `${Math.round(student.assessment_score)}%` : 'Passed'}
                            </span>
                          </div>
                        ) : (
                          <div className="flex items-center gap-1.5 text-slate-400">
                            <Clock className="w-3.5 h-3.5" />
                            <span>Pending</span>
                          </div>
                        )}
                      </td>

                      {/* Skill Level */}
                      <td className="py-3.5 px-4">
                        <span className="px-2 py-0.5 rounded text-[10px] font-semibold uppercase bg-slate-100 text-slate-600">
                          {student.skill_level}
                        </span>
                      </td>

                      {/* Progress */}
                      <td className="py-3.5 px-4">
                        <div className="w-28 space-y-1">
                          <div className="flex justify-between text-[10px] text-slate-500">
                            <span>{student.enrolled_courses_count} courses</span>
                            <span className="font-semibold">{student.overall_progress}%</span>
                          </div>
                          <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                            <div
                              className="bg-indigo-600 h-full rounded-full"
                              style={{ width: `${student.overall_progress}%` }}
                            />
                          </div>
                        </div>
                      </td>

                      {/* Registration Date */}
                      <td className="py-3.5 px-4 text-slate-500 whitespace-nowrap">
                        <div className="flex items-center gap-1">
                          <Calendar className="w-3 h-3 text-slate-400" />
                          {student.created_at ? new Date(student.created_at).toLocaleDateString() : 'N/A'}
                        </div>
                      </td>

                      {/* Last Login */}
                      <td className="py-3.5 px-4 text-slate-500 whitespace-nowrap">
                        {student.last_login ? new Date(student.last_login).toLocaleDateString() : 'Never'}
                      </td>

                      {/* Account Status Badge */}
                      <td className="py-3.5 px-4">
                        <span
                          className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold ${
                            student.is_active
                              ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                              : 'bg-rose-50 text-rose-700 border border-rose-200'
                          }`}
                        >
                          <span
                            className={`w-1.5 h-1.5 rounded-full ${
                              student.is_active ? 'bg-emerald-500' : 'bg-rose-500'
                            }`}
                          ></span>
                          {student.is_active ? 'Active' : 'Deactivated'}
                        </span>
                      </td>

                      {/* Actions */}
                      <td className="py-3.5 px-4 text-right">
                        <div className="flex items-center justify-end gap-1.5">
                          <button
                            onClick={() => onSelectStudent(student.user_id)}
                            title="Inspect 360 Student Profile"
                            className="p-1.5 text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors cursor-pointer"
                          >
                            <Eye className="w-4 h-4" />
                          </button>
                          <button
                            onClick={() => setSelectedStudentForAction(student)}
                            title={student.is_active ? 'Deactivate Student Account' : 'Activate Student Account'}
                            className={`p-1.5 rounded-lg transition-colors cursor-pointer ${
                              student.is_active
                                ? 'text-slate-400 hover:text-rose-600 hover:bg-rose-50'
                                : 'text-slate-400 hover:text-emerald-600 hover:bg-emerald-50'
                            }`}
                          >
                            <Power className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Confirmation Modal for Account Activation / Deactivation */}
      {selectedStudentForAction && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white border border-slate-200 rounded-2xl max-w-md w-full p-6 shadow-xl space-y-4">
            <div className="flex items-center gap-3">
              <div
                className={`p-2.5 rounded-xl ${
                  selectedStudentForAction.is_active
                    ? 'bg-rose-50 text-rose-600'
                    : 'bg-emerald-50 text-emerald-600'
                }`}
              >
                <Power className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-slate-900">
                  {selectedStudentForAction.is_active
                    ? 'Deactivate Student Account?'
                    : 'Activate Student Account?'}
                </h3>
                <p className="text-xs text-slate-500">
                  {selectedStudentForAction.full_name} ({selectedStudentForAction.email})
                </p>
              </div>
            </div>

            <p className="text-xs text-slate-600 leading-relaxed">
              {selectedStudentForAction.is_active
                ? 'Deactivating this student account will immediately reject future student logins and block existing access tokens with HTTP 403 Forbidden. Student progress and records will remain safely preserved.'
                : 'Activating this account will restore full student access, allowing the learner to login and resume coursework.'}
            </p>

            <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
              <button
                onClick={() => setSelectedStudentForAction(null)}
                disabled={actionLoading}
                className="px-3.5 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-lg transition-colors cursor-pointer"
              >
                Cancel
              </button>
              <button
                onClick={handleToggleStatus}
                disabled={actionLoading}
                className={`px-4 py-2 text-xs font-semibold text-white rounded-lg transition-colors shadow-xs cursor-pointer ${
                  selectedStudentForAction.is_active
                    ? 'bg-rose-600 hover:bg-rose-700'
                    : 'bg-emerald-600 hover:bg-emerald-700'
                }`}
              >
                {actionLoading
                  ? 'Processing...'
                  : selectedStudentForAction.is_active
                  ? 'Yes, Deactivate Account'
                  : 'Yes, Activate Account'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
