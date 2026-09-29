import React, { useEffect, useState } from 'react';
import {
  BookOpen,
  Plus,
  Edit2,
  Power,
  Users,
  Clock,
} from 'lucide-react';
import { adminApi } from '../../services/adminApi';
import type { AdminCourseItem, AdminCourseCreatePayload } from '../../types/admin';

export const AdminCoursesPage: React.FC = () => {
  const [courses, setCourses] = useState<AdminCourseItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Modal states
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [editingCourse, setEditingCourse] = useState<AdminCourseItem | null>(null);
  const [formSubmitting, setFormSubmitting] = useState(false);

  // Form states
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [category, setCategory] = useState('Cybersecurity');
  const [difficulty, setDifficulty] = useState('Intermediate');
  const [durationHours, setDurationHours] = useState(8.0);
  const [instructorName, setInstructorName] = useState('');
  const [prerequisitesStr, setPrerequisitesStr] = useState('');
  const [skillsTaughtStr, setSkillsTaughtStr] = useState('');

  const fetchCourses = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await adminApi.getCourses();
      setCourses(data);
    } catch (err: any) {
      console.error('Failed to load courses:', err);
      setError(err?.response?.data?.detail || 'Failed to fetch course catalog.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCourses();
  }, []);

  const openCreateModal = () => {
    setTitle('');
    setDescription('');
    setCategory('Cybersecurity');
    setDifficulty('Intermediate');
    setDurationHours(8.0);
    setInstructorName('');
    setPrerequisitesStr('');
    setSkillsTaughtStr('');
    setEditingCourse(null);
    setIsCreateModalOpen(true);
  };

  const openEditModal = (course: AdminCourseItem) => {
    setEditingCourse(course);
    setTitle(course.title);
    setDescription(course.description);
    setCategory(course.category);
    setDifficulty(course.difficulty_level);
    setDurationHours(course.duration_hours);
    setInstructorName(course.instructor_name);
    setPrerequisitesStr(course.prerequisites.join(', '));
    setSkillsTaughtStr(course.skills_taught.join(', '));
    setIsCreateModalOpen(true);
  };

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !description || !instructorName) {
      alert('Please fill in title, description, and instructor name.');
      return;
    }

    const prereqs = prerequisitesStr
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean);
    const skills = skillsTaughtStr
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean);

    try {
      setFormSubmitting(true);
      if (editingCourse) {
        // Edit course
        const updated = await adminApi.updateCourse(editingCourse.course_id, {
          title,
          description,
          category,
          difficulty_level: difficulty,
          duration_hours: Number(durationHours),
          instructor_name: instructorName,
          prerequisites: prereqs,
          skills_taught: skills,
        });
        setCourses((prev) =>
          prev.map((c) => (c.course_id === editingCourse.course_id ? updated : c))
        );
      } else {
        // Create course
        const payload: AdminCourseCreatePayload = {
          title,
          description,
          category,
          difficulty_level: difficulty,
          duration_hours: Number(durationHours),
          instructor_name: instructorName,
          prerequisites: prereqs,
          skills_taught: skills,
        };
        const created = await adminApi.createCourse(payload);
        setCourses((prev) => [created, ...prev]);
      }
      setIsCreateModalOpen(false);
    } catch (err: any) {
      alert(err?.response?.data?.detail || 'Failed to save course changes.');
    } finally {
      setFormSubmitting(false);
    }
  };

  const handleToggleCourseStatus = async (courseId: string, currentStatus: boolean) => {
    try {
      const newStatus = !currentStatus;
      await adminApi.updateCourseStatus(courseId, newStatus);
      setCourses((prev) =>
        prev.map((c) => (c.course_id === courseId ? { ...c, is_active: newStatus } : c))
      );
    } catch (err: any) {
      alert(err?.response?.data?.detail || 'Failed to toggle course status.');
    }
  };

  return (
    <div className="space-y-6 font-sans">
      {/* Header */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-indigo-600" />
            <h2 className="text-xl font-bold text-slate-900 tracking-tight">Course Management</h2>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Author and maintain courses, configure prerequisite skill matrices, and control catalog availability.
          </p>
        </div>
        <button
          onClick={openCreateModal}
          className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold rounded-lg shadow-xs transition-colors cursor-pointer"
        >
          <Plus className="w-4 h-4" />
          Create Course
        </button>
      </div>

      {/* Courses List */}
      <div className="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center p-12 text-slate-500">
            <div className="w-5 h-5 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin mr-3"></div>
            <span className="text-xs font-medium">Loading catalog courses...</span>
          </div>
        ) : error ? (
          <div className="p-8 text-center text-xs text-rose-600">{error}</div>
        ) : courses.length === 0 ? (
          <div className="p-12 text-center">
            <BookOpen className="w-10 h-10 text-slate-300 mx-auto mb-3" />
            <p className="text-sm font-semibold text-slate-700">No courses available.</p>
            <p className="text-xs text-slate-400 mt-1">Click "Create Course" to add the first curriculum course.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold uppercase tracking-wider text-[11px]">
                <tr>
                  <th className="py-3 px-4">Course Title</th>
                  <th className="py-3 px-4">Category</th>
                  <th className="py-3 px-4">Difficulty</th>
                  <th className="py-3 px-4">Duration</th>
                  <th className="py-3 px-4">Instructor</th>
                  <th className="py-3 px-4">Enrollments</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {courses.map((course) => (
                  <tr key={course.course_id} className="hover:bg-slate-50 transition-colors">
                    <td className="py-3.5 px-4">
                      <div className="font-semibold text-slate-900">{course.title}</div>
                      <div className="text-[11px] text-slate-400 line-clamp-1 max-w-sm">
                        {course.description}
                      </div>
                      <div className="flex items-center gap-1.5 mt-1">
                        {course.skills_taught.slice(0, 3).map((sk, idx) => (
                          <span
                            key={idx}
                            className="px-1.5 py-0.2 rounded text-[9px] font-medium bg-indigo-50 text-indigo-700"
                          >
                            {sk}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="py-3.5 px-4 font-medium text-slate-700">{course.category}</td>
                    <td className="py-3.5 px-4">
                      <span className="px-2 py-0.5 rounded text-[10px] font-semibold uppercase bg-slate-100 text-slate-600">
                        {course.difficulty_level}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-slate-600 font-medium">
                      <div className="flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5 text-slate-400" />
                        {course.duration_hours}h
                      </div>
                    </td>
                    <td className="py-3.5 px-4 text-slate-600">{course.instructor_name}</td>
                    <td className="py-3.5 px-4">
                      <div className="flex items-center gap-1 font-semibold text-slate-700">
                        <Users className="w-3.5 h-3.5 text-slate-400" />
                        {course.enrolled_count}
                      </div>
                    </td>
                    <td className="py-3.5 px-4">
                      <span
                        className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold ${
                          course.is_active
                            ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                            : 'bg-slate-100 text-slate-500'
                        }`}
                      >
                        <span
                          className={`w-1.5 h-1.5 rounded-full ${
                            course.is_active ? 'bg-emerald-500' : 'bg-slate-400'
                          }`}
                        ></span>
                        {course.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <div className="flex items-center justify-end gap-1.5">
                        <button
                          onClick={() => openEditModal(course)}
                          title="Edit Course"
                          className="p-1.5 text-slate-500 hover:text-indigo-600 hover:bg-slate-100 rounded-lg transition-colors cursor-pointer"
                        >
                          <Edit2 className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleToggleCourseStatus(course.course_id, course.is_active)}
                          title={course.is_active ? 'Deactivate Course' : 'Activate Course'}
                          className={`p-1.5 rounded-lg transition-colors cursor-pointer ${
                            course.is_active
                              ? 'text-slate-400 hover:text-rose-600 hover:bg-rose-50'
                              : 'text-slate-400 hover:text-emerald-600 hover:bg-emerald-50'
                          }`}
                        >
                          <Power className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Create / Edit Course Modal */}
      {isCreateModalOpen && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4 z-50 overflow-y-auto">
          <div className="bg-white border border-slate-200 rounded-2xl max-w-xl w-full p-6 shadow-xl space-y-4 my-8">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <h3 className="text-base font-bold text-slate-900">
                {editingCourse ? 'Edit Course Catalog Item' : 'Create New Course'}
              </h3>
              <button
                onClick={() => setIsCreateModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 text-sm cursor-pointer"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleFormSubmit} className="space-y-4 text-xs">
              <div>
                <label className="block text-slate-700 font-semibold mb-1">Course Title *</label>
                <input
                  type="text"
                  required
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g., Applied Network Defense & Threat Hunting"
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-slate-700 font-semibold mb-1">Description *</label>
                <textarea
                  required
                  rows={3}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Course summary, syllabus goals, and target outcomes..."
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-700 font-semibold mb-1">Category / Domain *</label>
                  <select
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 focus:outline-none focus:border-indigo-500"
                  >
                    <option value="Cybersecurity">Cybersecurity</option>
                    <option value="Artificial Intelligence">Artificial Intelligence</option>
                    <option value="Data Science">Data Science</option>
                    <option value="Software Engineering">Software Engineering</option>
                    <option value="Cloud Computing">Cloud Computing</option>
                  </select>
                </div>

                <div>
                  <label className="block text-slate-700 font-semibold mb-1">Difficulty Level *</label>
                  <select
                    value={difficulty}
                    onChange={(e) => setDifficulty(e.target.value)}
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 focus:outline-none focus:border-indigo-500"
                  >
                    <option value="Beginner">Beginner</option>
                    <option value="Intermediate">Intermediate</option>
                    <option value="Advanced">Advanced</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-700 font-semibold mb-1">Duration (Hours) *</label>
                  <input
                    type="number"
                    step="0.5"
                    min="1"
                    required
                    value={durationHours}
                    onChange={(e) => setDurationHours(parseFloat(e.target.value))}
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 focus:outline-none focus:border-indigo-500"
                  />
                </div>

                <div>
                  <label className="block text-slate-700 font-semibold mb-1">Instructor Name *</label>
                  <input
                    type="text"
                    required
                    value={instructorName}
                    onChange={(e) => setInstructorName(e.target.value)}
                    placeholder="e.g., Dr. Alice Smith"
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-slate-700 font-semibold mb-1">
                  Skills Covered (Comma-separated)
                </label>
                <input
                  type="text"
                  value={skillsTaughtStr}
                  onChange={(e) => setSkillsTaughtStr(e.target.value)}
                  placeholder="e.g., Python, Linux, Networking, Wireshark"
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 focus:outline-none focus:border-indigo-500"
                />
                <p className="text-[10px] text-slate-400 mt-1">
                  Used by the AI hybrid recommendation engine to match student skill gaps.
                </p>
              </div>

              <div>
                <label className="block text-slate-700 font-semibold mb-1">
                  Prerequisites (Comma-separated)
                </label>
                <input
                  type="text"
                  value={prerequisitesStr}
                  onChange={(e) => setPrerequisitesStr(e.target.value)}
                  placeholder="e.g., Linux, Python"
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 focus:outline-none focus:border-indigo-500"
                />
                <p className="text-[10px] text-slate-400 mt-1">
                  Enforces prerequisite ordering in personalized learning pathways.
                </p>
              </div>

              <div className="flex items-center justify-end gap-2 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setIsCreateModalOpen(false)}
                  className="px-3.5 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-lg transition-colors cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={formSubmitting}
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold rounded-lg shadow-xs transition-colors cursor-pointer"
                >
                  {formSubmitting
                    ? 'Saving...'
                    : editingCourse
                    ? 'Update Course'
                    : 'Save & Publish Course'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
