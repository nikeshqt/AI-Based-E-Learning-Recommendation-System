import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  fetchCourseLearningContent,
  completeLesson,
  enrollInCourse,
} from '../services/courseLearningService';
import type {
  CourseLearningResponse,
  LessonPublicSchema,
} from '../types/courseLearning';

interface CourseLearningPageProps {
  courseId?: string;
  onBack?: () => void;
}

export const CourseLearningPage: React.FC<CourseLearningPageProps> = ({
  courseId: propCourseId,
  onBack,
}) => {
  const { courseId: paramCourseId } = useParams<{ courseId: string }>();
  const navigate = useNavigate();
  const targetCourseId = propCourseId || paramCourseId || 'crs_sec_04';

  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [courseData, setCourseData] = useState<CourseLearningResponse | null>(null);
  const [activeLesson, setActiveLesson] = useState<LessonPublicSchema | null>(null);
  const [actionLoading, setActionLoading] = useState<boolean>(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const loadData = async () => {
    if (!targetCourseId) return;
    try {
      setLoading(true);
      setError(null);
      // Ensure user is enrolled first
      await enrollInCourse(targetCourseId);
      const data = await fetchCourseLearningContent(targetCourseId);
      setCourseData(data);

      // Default active lesson to first incomplete lesson, or first lesson overall
      let initialLesson: LessonPublicSchema | null = null;
      for (const mod of data.modules) {
        for (const les of mod.lessons) {
          if (!les.is_completed && !initialLesson) {
            initialLesson = les;
            break;
          }
        }
        if (initialLesson) break;
      }
      if (!initialLesson && data.modules.length > 0 && data.modules[0].lessons.length > 0) {
        initialLesson = data.modules[0].lessons[0];
      }
      setActiveLesson(initialLesson);
    } catch (err: any) {
      console.error('Failed to load course content:', err);
      setError(err?.response?.data?.detail || 'Failed to load course lessons.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [targetCourseId]);


  const handleCompleteLesson = async () => {
    if (!targetCourseId || !activeLesson) return;
    try {
      setActionLoading(true);
      setSuccessMsg(null);
      const res = await completeLesson(targetCourseId, activeLesson.lesson_id);
      
      if (res.course_completed) {
        setSuccessMsg('🎉 Congratulations! You have completed all lessons in this course!');
      } else {
        setSuccessMsg('Lesson marked as completed!');
      }

      // Refresh course data
      const updatedData = await fetchCourseLearningContent(targetCourseId);
      setCourseData(updatedData);

      // Update active lesson state
      const updatedLesson = { ...activeLesson, is_completed: true };
      setActiveLesson(updatedLesson);

      // Find next incomplete lesson automatically
      let nextLesson: LessonPublicSchema | null = null;
      let foundCurrent = false;

      for (const mod of updatedData.modules) {
        for (const les of mod.lessons) {
          if (foundCurrent && !les.is_completed) {
            nextLesson = les;
            break;
          }
          if (les.lesson_id === activeLesson.lesson_id) {
            foundCurrent = true;
          }
        }
        if (nextLesson) break;
      }

      if (nextLesson) {
        setTimeout(() => {
          setActiveLesson(nextLesson);
          setSuccessMsg(null);
        }, 1200);
      }
    } catch (err: any) {
      console.error('Failed to mark lesson complete:', err);
      setError(err?.response?.data?.detail || 'Failed to update lesson completion state.');
    } finally {
      setActionLoading(false);
    }
  };

  const handleBackNavigation = () => {
    if (onBack) {
      onBack();
    } else {
      navigate('/catalog');
    }
  };

  const allLessons: LessonPublicSchema[] = courseData
    ? courseData.modules.flatMap((m) => m.lessons)
    : [];

  const currentLessonIndex = activeLesson
    ? allLessons.findIndex((l) => l.lesson_id === activeLesson.lesson_id)
    : -1;

  const prevLesson = currentLessonIndex > 0 ? allLessons[currentLessonIndex - 1] : null;
  const nextLesson =
    currentLessonIndex >= 0 && currentLessonIndex < allLessons.length - 1
      ? allLessons[currentLessonIndex + 1]
      : null;

  if (loading) {
    return (
      <div className="min-h-screen bg-[#F8FAFC] flex items-center justify-center p-6">
        <div className="flex items-center space-x-3 text-[#64748B]">
          <div className="w-5 h-5 border-2 border-[#4F46E5] border-t-transparent rounded-full animate-spin"></div>
          <span className="font-medium text-sm">Loading course lessons...</span>
        </div>
      </div>
    );
  }

  if (error || !courseData) {
    return (
      <div className="min-h-screen bg-[#F8FAFC] p-6">
        <div className="max-w-4xl mx-auto bg-[#FFFFFF] rounded-xl border border-[#E2E8F0] p-6">
          <h2 className="text-xl font-semibold text-[#0F172A] mb-2">Error Loading Course</h2>
          <p className="text-[#64748B] mb-4">{error || 'Course not found.'}</p>
          <button
            onClick={handleBackNavigation}
            className="px-4 py-2 bg-[#4F46E5] hover:bg-[#4338CA] text-white text-sm font-medium rounded-lg transition-colors"
          >
            Back to Catalog
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#F8FAFC] flex flex-col font-sans">
      {/* Top Header Navigation */}
      <header className="bg-[#FFFFFF] border-b border-[#E2E8F0] px-6 py-4 flex items-center justify-between sticky top-0 z-10">
        <div className="flex items-center space-x-4">
          <button
            onClick={handleBackNavigation}
            className="text-sm font-medium text-[#64748B] hover:text-[#0F172A] flex items-center space-x-1"
          >
            <span>←</span>
            <span>Back</span>
          </button>
          <div className="h-4 w-px bg-[#E2E8F0]" />
          <div>
            <span className="text-xs font-semibold uppercase tracking-wider text-[#4F46E5]">
              {courseData.category}
            </span>
            <h1 className="text-base font-semibold text-[#0F172A] leading-tight">
              {courseData.title}
            </h1>
          </div>
        </div>

        <div className="flex items-center space-x-6">
          <div className="flex flex-col items-end">
            <span className="text-xs text-[#64748B] font-medium">
              Progress: {courseData.progress_percentage}% ({courseData.completed_lessons_count}/{courseData.total_lessons_count} Lessons)
            </span>
            <div className="w-36 h-2 bg-[#E2E8F0] rounded-full mt-1 overflow-hidden">
              <div
                className="h-full bg-[#4F46E5] transition-all duration-300 rounded-full"
                style={{ width: `${courseData.progress_percentage}%` }}
              />
            </div>
          </div>
        </div>
      </header>

      {/* Main Layout Container */}
      <div className="flex-1 flex overflow-hidden">
        {/* Modules & Lessons Sidebar */}
        <aside className="w-80 bg-[#FFFFFF] border-r border-[#E2E8F0] flex flex-col overflow-y-auto">
          <div className="p-4 border-b border-[#E2E8F0] bg-[#F8FAFC]">
            <h2 className="text-xs font-semibold text-[#64748B] uppercase tracking-wider">
              Course Modules & Lessons
            </h2>
          </div>

          <div className="flex-1 divide-y divide-[#E2E8F0]">
            {courseData.modules.map((mod, modIdx) => (
              <div key={mod.module_id} className="p-4">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-sm font-semibold text-[#0F172A]">
                    Module {modIdx + 1}: {mod.title}
                  </h3>
                </div>

                <div className="space-y-1">
                  {mod.lessons.map((les) => {
                    const isActive = activeLesson?.lesson_id === les.lesson_id;
                    return (
                      <button
                        key={les.lesson_id}
                        onClick={() => setActiveLesson(les)}
                        className={`w-full text-left p-2.5 rounded-lg flex items-start space-x-3 transition-colors text-sm ${
                          isActive
                            ? 'bg-[#F1F5F9] border border-[#E2E8F0]'
                            : 'hover:bg-[#F8FAFC]'
                        }`}
                      >
                        <div className="mt-0.5 flex-shrink-0">
                          {les.is_completed ? (
                            <span className="w-4 h-4 rounded-full bg-[#10B981] text-white flex items-center justify-center text-[10px] font-bold">
                              ✓
                            </span>
                          ) : (
                            <span
                              className={`w-4 h-4 rounded-full border border-[#CBD5E1] flex items-center justify-center text-[10px] ${
                                isActive ? 'border-[#4F46E5] text-[#4F46E5] font-bold' : 'text-[#64748B]'
                              }`}
                            >
                              ▶
                            </span>
                          )}
                        </div>

                        <div className="flex-1 min-w-0">
                          <p
                            className={`text-xs font-medium truncate ${
                              isActive ? 'text-[#4F46E5]' : 'text-[#0F172A]'
                            }`}
                          >
                            {les.title}
                          </p>
                          <p className="text-[11px] text-[#64748B] mt-0.5">
                            {les.estimated_duration_minutes} min
                          </p>
                        </div>
                      </button>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </aside>

        {/* Lesson Reader Content Area */}
        <main className="flex-1 overflow-y-auto p-8 max-w-4xl mx-auto">
          {successMsg && (
            <div className="mb-6 p-4 bg-[#ECFDF5] border border-[#A7F3D0] rounded-xl text-[#065F46] text-sm font-medium flex items-center justify-between">
              <span>{successMsg}</span>
              <button
                onClick={() => setSuccessMsg(null)}
                className="text-[#065F46] hover:text-[#047857] text-xs font-bold"
              >
                Dismiss
              </button>
            </div>
          )}

          {activeLesson ? (
            <div className="space-y-6">
              <div className="bg-[#FFFFFF] rounded-xl border border-[#E2E8F0] p-6 shadow-sm">
                <div className="flex items-center justify-between border-b border-[#E2E8F0] pb-4 mb-4">
                  <div>
                    <span className="text-xs font-semibold text-[#64748B] uppercase tracking-wider">
                      Lesson {currentLessonIndex + 1} of {allLessons.length}
                    </span>
                    <h2 className="text-2xl font-bold text-[#0F172A] mt-1">
                      {activeLesson.title}
                    </h2>
                  </div>
                  <div className="flex items-center space-x-2 bg-[#F8FAFC] border border-[#E2E8F0] px-3 py-1.5 rounded-lg text-xs font-medium text-[#475569]">
                    <span>⏱ {activeLesson.estimated_duration_minutes} mins</span>
                  </div>
                </div>

                {activeLesson.description && (
                  <p className="text-sm text-[#475569] bg-[#F8FAFC] p-3.5 rounded-lg border border-[#E2E8F0] mb-6">
                    {activeLesson.description}
                  </p>
                )}

                {/* Lesson Body Content */}
                <div className="prose max-w-none text-[#0F172A] text-sm leading-relaxed space-y-4 whitespace-pre-line">
                  {activeLesson.content || 'Lesson content is coming soon.'}
                </div>

                {/* Lesson Completion Controls */}
                <div className="mt-8 pt-6 border-t border-[#E2E8F0] flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    {prevLesson && (
                      <button
                        onClick={() => setActiveLesson(prevLesson)}
                        className="px-4 py-2 border border-[#E2E8F0] text-[#0F172A] text-sm font-medium rounded-lg hover:bg-[#F8FAFC] transition-colors"
                      >
                        ← Previous Lesson
                      </button>
                    )}
                    {nextLesson && (
                      <button
                        onClick={() => setActiveLesson(nextLesson)}
                        className="px-4 py-2 border border-[#E2E8F0] text-[#0F172A] text-sm font-medium rounded-lg hover:bg-[#F8FAFC] transition-colors"
                      >
                        Next Lesson →
                      </button>
                    )}
                  </div>

                  <button
                    onClick={handleCompleteLesson}
                    disabled={actionLoading || activeLesson.is_completed}
                    className={`px-5 py-2.5 rounded-lg text-sm font-semibold transition-colors flex items-center space-x-2 ${
                      activeLesson.is_completed
                        ? 'bg-[#ECFDF5] text-[#065F46] border border-[#A7F3D0] cursor-default'
                        : 'bg-[#4F46E5] hover:bg-[#4338CA] text-white shadow-sm'
                    }`}
                  >
                    {actionLoading ? (
                      <span>Updating...</span>
                    ) : activeLesson.is_completed ? (
                      <span>✓ Completed</span>
                    ) : (
                      <span>Mark as Complete & Next</span>
                    )}
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-[#FFFFFF] rounded-xl border border-[#E2E8F0] p-8 text-center text-[#64748B]">
              <p>Select a lesson from the sidebar to begin reading.</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};
