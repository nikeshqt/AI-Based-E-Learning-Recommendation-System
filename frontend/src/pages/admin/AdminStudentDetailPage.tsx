import React, { useEffect, useState } from 'react';
import {
  ArrowLeft,
  Award,
  Target,
  Compass,
  GitBranch,
  BookOpen,
  Power,
} from 'lucide-react';
import { adminApi } from '../../services/adminApi';
import type { AdminStudentDetailResponse } from '../../types/admin';

interface AdminStudentDetailPageProps {
  studentId: string;
  onBack: () => void;
}

export const AdminStudentDetailPage: React.FC<AdminStudentDetailPageProps> = ({
  studentId,
  onBack,
}) => {
  const [detail, setDetail] = useState<AdminStudentDetailResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [statusLoading, setStatusLoading] = useState(false);

  const fetchDetail = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await adminApi.getStudentDetail(studentId);
      setDetail(data);
    } catch (err: any) {
      console.error('Failed to load student detail:', err);
      setError(err?.response?.data?.detail || 'Failed to load student details.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDetail();
  }, [studentId]);

  const handleToggleStatus = async () => {
    if (!detail) return;
    try {
      setStatusLoading(true);
      const newStatus = !detail.profile.is_active;
      await adminApi.updateStudentStatus(detail.profile.user_id, newStatus);
      setDetail((prev) =>
        prev
          ? {
              ...prev,
              profile: {
                ...prev.profile,
                is_active: newStatus,
              },
            }
          : prev
      );
    } catch (err: any) {
      alert(err?.response?.data?.detail || 'Failed to update account status.');
    } finally {
      setStatusLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh] text-slate-500 font-sans">
        <div className="w-5 h-5 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin mr-3"></div>
        <span className="text-sm font-medium">Loading comprehensive student profile...</span>
      </div>
    );
  }

  if (error || !detail) {
    return (
      <div className="bg-rose-50 border border-rose-200 rounded-xl p-6 text-center text-rose-700 font-sans space-y-3">
        <p className="font-semibold text-sm">Failed to load student profile</p>
        <p className="text-xs text-rose-600">{error || 'Student record could not be found.'}</p>
        <button
          onClick={onBack}
          className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white text-xs font-semibold rounded-lg hover:bg-indigo-700 transition-colors cursor-pointer"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          Back to Students
        </button>
      </div>
    );
  }

  const { profile, assessment, skill_gaps, recommendations, learning_path, course_progress } = detail;

  return (
    <div className="space-y-6 font-sans">
      {/* Top Bar with Back Button and Quick Status */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <button
          onClick={onBack}
          className="inline-flex items-center gap-2 text-xs font-semibold text-slate-600 hover:text-slate-900 transition-colors cursor-pointer"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Student Directory
        </button>

        <div className="flex items-center gap-3">
          <span
            className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold ${
              profile.is_active
                ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                : 'bg-rose-50 text-rose-700 border border-rose-200'
            }`}
          >
            <span
              className={`w-2 h-2 rounded-full ${profile.is_active ? 'bg-emerald-500' : 'bg-rose-500'}`}
            ></span>
            {profile.is_active ? 'Active Account' : 'Deactivated'}
          </span>

          <button
            onClick={handleToggleStatus}
            disabled={statusLoading}
            className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer shadow-xs ${
              profile.is_active
                ? 'bg-rose-50 text-rose-700 hover:bg-rose-100 border border-rose-200'
                : 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border border-emerald-200'
            }`}
          >
            <Power className="w-3.5 h-3.5" />
            {statusLoading ? 'Updating...' : profile.is_active ? 'Deactivate Account' : 'Activate Account'}
          </button>
        </div>
      </div>

      {/* 1. PROFILE SECTION */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs">
        <div className="flex flex-col md:flex-row items-start md:items-center gap-4 pb-6 border-b border-slate-100">
          <div className="w-14 h-14 rounded-2xl bg-indigo-600 text-white flex items-center justify-center font-bold text-xl shadow-xs">
            {profile.full_name.charAt(0).toUpperCase()}
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-2">
              <h2 className="text-xl font-bold text-slate-900 tracking-tight">{profile.full_name}</h2>
              <span className="px-2 py-0.5 rounded text-[10px] font-semibold uppercase bg-slate-100 text-slate-600">
                {profile.role}
              </span>
            </div>
            <p className="text-xs text-slate-500 font-mono mt-0.5">{profile.email}</p>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-4 pt-6 text-xs">
          <div>
            <span className="text-slate-400 block text-[11px] mb-1">Career Goal</span>
            <span className="font-semibold text-slate-900">{profile.career_goal}</span>
          </div>
          <div>
            <span className="text-slate-400 block text-[11px] mb-1">Learning Style</span>
            <span className="font-semibold text-slate-900 capitalize">{profile.preferred_learning_style}</span>
          </div>
          <div>
            <span className="text-slate-400 block text-[11px] mb-1">Skill Level</span>
            <span className="font-semibold text-slate-900 capitalize">{profile.skill_level}</span>
          </div>
          <div>
            <span className="text-slate-400 block text-[11px] mb-1">Registration Date</span>
            <span className="font-semibold text-slate-900">
              {profile.registration_date ? new Date(profile.registration_date).toLocaleDateString() : 'N/A'}
            </span>
          </div>
          <div>
            <span className="text-slate-400 block text-[11px] mb-1">Last Login</span>
            <span className="font-semibold text-slate-900">
              {profile.last_login ? new Date(profile.last_login).toLocaleDateString() : 'Never'}
            </span>
          </div>
          <div>
            <span className="text-slate-400 block text-[11px] mb-1">Account ID</span>
            <span className="font-mono text-slate-500 text-[11px]">{profile.user_id}</span>
          </div>
        </div>
      </div>

      {/* 2. ASSESSMENT & 3. SKILL GAPS GRID */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Assessment Section */}
        <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <Award className="w-5 h-5 text-indigo-600" />
                <h3 className="text-sm font-bold text-slate-900">Skill Assessment Performance</h3>
              </div>
              <span
                className={`px-2.5 py-1 rounded-full text-xs font-semibold ${
                  assessment.completed
                    ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                    : 'bg-slate-100 text-slate-600'
                }`}
              >
                {assessment.completed ? 'Assessment Completed' : 'Not Completed'}
              </span>
            </div>

            {assessment.completed ? (
              <div className="space-y-4">
                <div className="flex items-center gap-4 bg-slate-50 p-4 rounded-xl">
                  <div className="text-3xl font-extrabold text-indigo-600">
                    {Math.round(assessment.overall_score || 0)}%
                  </div>
                  <div>
                    <div className="text-xs font-semibold text-slate-800">Overall Benchmark Score</div>
                    <div className="text-[11px] text-slate-500">
                      Answered {assessment.correct_answers} of {assessment.total_questions} questions correctly
                    </div>
                  </div>
                </div>

                <div>
                  <h4 className="text-xs font-bold text-slate-700 mb-2 uppercase tracking-wide">
                    Domain Mastery Scores
                  </h4>
                  <div className="space-y-2">
                    {Object.entries(assessment.topic_scores).map(([domain, score]) => (
                      <div key={domain} className="space-y-1">
                        <div className="flex justify-between text-xs">
                          <span className="text-slate-600 font-medium">{domain}</span>
                          <span className="font-semibold text-slate-900">{Math.round(score)}%</span>
                        </div>
                        <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                          <div
                            className="bg-indigo-600 h-full rounded-full"
                            style={{ width: `${score}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="py-12 text-center text-xs text-slate-400">
                Student has not taken the 40-question technical skill assessment yet.
              </div>
            )}
          </div>
          {assessment.submitted_at && (
            <div className="text-[11px] text-slate-400 pt-4 border-t border-slate-100 mt-4">
              Submitted on: {new Date(assessment.submitted_at).toLocaleString()}
            </div>
          )}
        </div>

        {/* Skill Gaps Section */}
        <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs">
          <div className="flex items-center gap-2 mb-4">
            <Target className="w-5 h-5 text-indigo-600" />
            <h3 className="text-sm font-bold text-slate-900">
              Active Skill Gap Matrix ({profile.career_goal})
            </h3>
          </div>

          {skill_gaps.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 text-slate-500 text-[11px] font-semibold uppercase">
                  <tr>
                    <th className="py-2 px-3">Skill</th>
                    <th className="py-2 px-3">Current</th>
                    <th className="py-2 px-3">Required</th>
                    <th className="py-2 px-3">Gap</th>
                    <th className="py-2 px-3 text-right">Priority</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {skill_gaps.map((item, idx) => (
                    <tr key={idx} className="hover:bg-slate-50">
                      <td className="py-2.5 px-3 font-semibold text-slate-800">{item.skill}</td>
                      <td className="py-2.5 px-3 text-slate-600">{Math.round(item.current_mastery)}%</td>
                      <td className="py-2.5 px-3 text-slate-600">{Math.round(item.target_mastery)}%</td>
                      <td className="py-2.5 px-3">
                        <span
                          className={`font-semibold ${
                            item.gap > 0 ? 'text-amber-600' : 'text-emerald-600'
                          }`}
                        >
                          {item.gap > 0 ? `-${Math.round(item.gap)}%` : '0% (Met)'}
                        </span>
                      </td>
                      <td className="py-2.5 px-3 text-right">
                        <span
                          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                            item.priority >= 0.7
                              ? 'bg-rose-50 text-rose-700'
                              : item.priority >= 0.4
                              ? 'bg-amber-50 text-amber-700'
                              : 'bg-slate-100 text-slate-600'
                          }`}
                        >
                          {item.priority >= 0.7 ? 'High' : item.priority >= 0.4 ? 'Medium' : 'Low'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="py-12 text-center text-xs text-slate-400">
              No active skill gaps calculated for this student.
            </div>
          )}
        </div>
      </div>

      {/* 4. AI RECOMMENDATIONS SECTION */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs">
        <div className="flex items-center gap-2 mb-4">
          <Compass className="w-5 h-5 text-indigo-600" />
          <h3 className="text-sm font-bold text-slate-900">AI Personalized Course Recommendations</h3>
        </div>

        {recommendations.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {recommendations.map((rec) => (
              <div
                key={rec.course_id}
                className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-2 text-xs"
              >
                <div className="flex items-start justify-between gap-2">
                  <h4 className="font-bold text-slate-900">{rec.title}</h4>
                  <span className="px-2 py-0.5 rounded font-mono text-[10px] font-bold bg-indigo-100 text-indigo-700 shrink-0">
                    Match: {Math.round(rec.match_score * 100)}%
                  </span>
                </div>
                <p className="text-slate-600 leading-relaxed">{rec.recommendation_reason}</p>
                {rec.target_skill_gap && (
                  <div className="text-[11px] text-indigo-600 font-semibold">
                    Targets Gap: {rec.target_skill_gap}
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="py-6 text-center text-xs text-slate-400">
            No recommendations generated yet.
          </div>
        )}
      </div>

      {/* 5. LEARNING PATH ROADMAP */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <GitBranch className="w-5 h-5 text-indigo-600" />
            <h3 className="text-sm font-bold text-slate-900">
              Personalized Learning Path ({learning_path?.title || 'Active Curriculum'})
            </h3>
          </div>
          {learning_path && (
            <span className="text-xs font-semibold text-slate-600">
              Readiness: <strong className="text-indigo-600">{learning_path.overall_readiness}%</strong>
            </span>
          )}
        </div>

        {learning_path && learning_path.stages.length > 0 ? (
          <div className="space-y-3">
            {learning_path.stages.map((st, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between p-3.5 rounded-lg border border-slate-200 bg-white text-xs hover:border-indigo-200 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div className="w-6 h-6 rounded-full bg-indigo-50 border border-indigo-200 flex items-center justify-center font-bold text-indigo-600 text-[11px]">
                    {st.stage_number}
                  </div>
                  <div>
                    <div className="font-semibold text-slate-900">{st.course_title}</div>
                    <div className="text-[11px] text-slate-500">{st.stage_title}</div>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  {st.target_skill && (
                    <span className="hidden sm:inline-block px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-100 text-slate-600">
                      {st.target_skill}
                    </span>
                  )}
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-semibold uppercase ${
                      st.status === 'COMPLETED'
                        ? 'bg-emerald-50 text-emerald-700'
                        : 'bg-indigo-50 text-indigo-700'
                    }`}
                  >
                    {st.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="py-6 text-center text-xs text-slate-400">
            No active learning path generated yet for this student.
          </div>
        )}
      </div>

      {/* 6. COURSE PROGRESS SECTION */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs">
        <div className="flex items-center gap-2 mb-4">
          <BookOpen className="w-5 h-5 text-indigo-600" />
          <h3 className="text-sm font-bold text-slate-900">Enrolled Courses & Detailed Progress</h3>
        </div>

        {course_progress.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-500 text-[11px] font-semibold uppercase">
                <tr>
                  <th className="py-2.5 px-3">Course</th>
                  <th className="py-2.5 px-3">Category</th>
                  <th className="py-2.5 px-3">Enrolled</th>
                  <th className="py-2.5 px-3">Progress</th>
                  <th className="py-2.5 px-3">Lessons</th>
                  <th className="py-2.5 px-3">Status</th>
                  <th className="py-2.5 px-3">Last Activity</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {course_progress.map((prog, idx) => (
                  <tr key={idx} className="hover:bg-slate-50">
                    <td className="py-3 px-3 font-semibold text-slate-900">{prog.course_title}</td>
                    <td className="py-3 px-3 text-slate-600">{prog.category}</td>
                    <td className="py-3 px-3 text-slate-500">
                      {prog.enrollment_date ? new Date(prog.enrollment_date).toLocaleDateString() : 'N/A'}
                    </td>
                    <td className="py-3 px-3">
                      <div className="w-24 space-y-1">
                        <span className="font-semibold text-slate-800">{prog.progress_percentage}%</span>
                        <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                          <div
                            className="bg-indigo-600 h-full rounded-full"
                            style={{ width: `${prog.progress_percentage}%` }}
                          />
                        </div>
                      </div>
                    </td>
                    <td className="py-3 px-3 text-slate-600">
                      {prog.completed_lessons} / {prog.total_lessons}
                    </td>
                    <td className="py-3 px-3">
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-semibold uppercase ${
                          prog.completion_status === 'COMPLETED'
                            ? 'bg-emerald-50 text-emerald-700'
                            : 'bg-indigo-50 text-indigo-700'
                        }`}
                      >
                        {prog.completion_status}
                      </span>
                    </td>
                    <td className="py-3 px-3 text-slate-500 whitespace-nowrap">
                      {prog.last_activity ? new Date(prog.last_activity).toLocaleString() : 'N/A'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="py-6 text-center text-xs text-slate-400">
            Student is not currently enrolled in any courses.
          </div>
        )}
      </div>
    </div>
  );
};
