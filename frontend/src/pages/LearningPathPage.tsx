import React, { useEffect, useState } from 'react';
import {
  GitBranch,
  Target,
  Clock,
  BookOpen,
  CheckCircle2,
  Lock,
  RefreshCw,
  HelpCircle,
  ChevronRight,
  Layers,
} from 'lucide-react';
import { fetchCurrentLearningPath, generateLearningPath } from '../services/learningPathService';
import type { LearningPathResponse, LearningPathItem } from '../types/learningPath';

interface LearningPathPageProps {
  onSelectCourse?: (courseId: string) => void;
}

export const LearningPathPage: React.FC<LearningPathPageProps> = ({ onSelectCourse }) => {
  const [path, setPath] = useState<LearningPathResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [regenerating, setRegenerating] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const loadPath = async () => {
    try {
      setLoading(true);
      const data = await fetchCurrentLearningPath();
      setPath(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load learning path.');
    } finally {
      setLoading(false);
    }
  };

  const handleRegenerate = async () => {
    try {
      setRegenerating(true);
      const data = await generateLearningPath();
      setPath(data);
    } catch (err: any) {
      console.error('Error regenerating learning path:', err);
    } finally {
      setRegenerating(false);
    }
  };

  useEffect(() => {
    loadPath();
  }, []);

  const handleCourseClick = (item: LearningPathItem) => {
    if (onSelectCourse) {
      onSelectCourse(item.course_id);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border-3 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-sm font-medium text-slate-600">Generating personalized prerequisite-aware roadmap...</p>
        </div>
      </div>
    );
  }

  if (error || !path) {
    return (
      <div className="bg-rose-50 border border-rose-200 rounded-xl p-6 text-rose-800">
        <h3 className="font-semibold text-lg mb-1">Error Loading Learning Path</h3>
        <p className="text-sm">{error || 'Could not fetch your personalized learning path.'}</p>
        <button
          onClick={loadPath}
          className="mt-4 px-4 py-2 bg-rose-600 text-white font-semibold text-xs rounded-lg hover:bg-rose-700"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 shadow-xs">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
            <GitBranch className="w-6 h-6 text-indigo-600" />
            Your Learning Path
          </h1>
          <p className="text-sm text-slate-600 mt-1">
            A personalized roadmap built around your career goal and current skill gaps.
          </p>
        </div>
        <button
          onClick={handleRegenerate}
          disabled={regenerating}
          className="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-xs font-semibold text-white flex items-center gap-2 transition-colors shrink-0 shadow-xs"
        >
          <RefreshCw className={`w-4 h-4 ${regenerating ? 'animate-spin' : ''}`} />
          Regenerate Pathway
        </button>
      </div>

      {/* Top Summary Bar */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div>
          <div className="flex items-center gap-2 text-slate-500 mb-1">
            <Target className="w-4 h-4 text-indigo-600" />
            <span className="text-xs font-semibold uppercase tracking-wider">Career Goal</span>
          </div>
          <p className="text-base font-bold text-slate-900">{path.career_goal}</p>
          <p className="text-[11px] text-slate-500 mt-0.5">Active Target</p>
        </div>

        <div>
          <div className="flex items-center justify-between mb-1">
            <div className="flex items-center gap-2 text-slate-500">
              <Layers className="w-4 h-4 text-emerald-600" />
              <span className="text-xs font-semibold uppercase tracking-wider">Readiness</span>
            </div>
            <span className="text-sm font-bold text-indigo-600">{path.overall_readiness}%</span>
          </div>
          <div className="w-full h-2.5 bg-slate-100 rounded-full overflow-hidden border border-slate-200 mt-1.5">
            <div
              className="h-full bg-indigo-600 rounded-full transition-all duration-500"
              style={{ width: `${Math.min(100, Math.max(0, path.overall_readiness))}%` }}
            />
          </div>
        </div>

        <div>
          <div className="flex items-center gap-2 text-slate-500 mb-1">
            <BookOpen className="w-4 h-4 text-blue-600" />
            <span className="text-xs font-semibold uppercase tracking-wider">Total Courses</span>
          </div>
          <p className="text-base font-bold text-slate-900">{path.total_courses} Courses</p>
          <p className="text-[11px] text-slate-500 mt-0.5">Ordered by prerequisites</p>
        </div>

        <div>
          <div className="flex items-center gap-2 text-slate-500 mb-1">
            <Clock className="w-4 h-4 text-amber-600" />
            <span className="text-xs font-semibold uppercase tracking-wider">Estimated Time</span>
          </div>
          <p className="text-base font-bold text-slate-900">{path.total_duration_hours} Hours</p>
          <p className="text-[11px] text-slate-500 mt-0.5">Cumulative learning time</p>
        </div>
      </div>

      {/* Vertical Roadmap Stages */}
      <div className="space-y-8">
        {path.stages.map((stage) => (
          <div key={stage.stage_number} className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs space-y-6">
            {/* Stage Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-100 pb-4">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-bold font-mono px-2 py-0.5 bg-indigo-100 text-indigo-800 rounded">
                    0{stage.stage_number} {stage.stage_name.toUpperCase()}
                  </span>
                  <span className="text-xs px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 font-semibold border border-slate-200">
                    {stage.status === 'AVAILABLE' ? 'Available Now' : 'Locked Stage'}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-slate-900">{stage.stage_title}</h3>
                <p className="text-xs text-slate-600 mt-1">{stage.description}</p>
              </div>

              <div className="flex items-center gap-3 text-xs text-slate-500 shrink-0">
                <span className="flex items-center gap-1 font-semibold text-slate-700">
                  <Clock className="w-3.5 h-3.5 text-slate-400" />
                  {stage.estimated_duration_hours} Hours
                </span>
                <span className="text-slate-300">•</span>
                <span className="font-semibold text-slate-700">{stage.courses.length} Courses</span>
              </div>
            </div>

            {/* Targeted Skill Badges */}
            <div className="flex items-center gap-2 flex-wrap text-xs">
              <span className="text-slate-500 font-medium">Targeted Skills:</span>
              {stage.target_skills.map((sk) => (
                <span key={sk} className="px-2 py-0.5 bg-slate-100 text-slate-700 font-medium rounded border border-slate-200">
                  {sk}
                </span>
              ))}
            </div>

            {/* Courses in Stage */}
            <div className="space-y-4">
              {stage.courses.map((item) => (
                <div
                  key={item.course_id}
                  className={`p-5 rounded-xl border transition-all ${
                    item.status === 'LOCKED'
                      ? 'bg-slate-50/70 border-slate-200 opacity-80'
                      : 'bg-white border-slate-200 hover:border-indigo-300'
                  }`}
                >
                  <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 mb-4">
                    <div className="flex items-start gap-3">
                      <div className="w-8 h-8 rounded-lg bg-indigo-50 border border-indigo-100 shrink-0 flex items-center justify-center font-mono font-bold text-indigo-700 text-xs mt-0.5">
                        {item.order_index < 10 ? `0${item.order_index}` : item.order_index}
                      </div>
                      <div>
                        <div className="flex items-center gap-2 flex-wrap">
                          <h4 className="text-base font-bold text-slate-900">{item.course_title}</h4>
                          <span className="text-[11px] px-2 py-0.5 rounded bg-slate-100 border border-slate-200 text-slate-700 font-medium">
                            Target Skill: {item.target_skill}
                          </span>
                        </div>
                        <div className="flex items-center gap-4 text-xs text-slate-500 mt-1">
                          <span className="flex items-center gap-1 font-medium text-slate-700">
                            <Clock className="w-3.5 h-3.5 text-slate-400" />
                            {item.estimated_duration_hours} Hours
                          </span>
                          <span className="flex items-center gap-1 text-emerald-700 font-medium">
                            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                            Prerequisites Met
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-3 self-end lg:self-center">
                      {item.status === 'LOCKED' ? (
                        <span className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-100 text-slate-600 font-semibold text-xs rounded-lg border border-slate-200">
                          <Lock className="w-3.5 h-3.5" />
                          Locked
                        </span>
                      ) : (
                        <button
                          onClick={() => handleCourseClick(item)}
                          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs rounded-lg transition-colors flex items-center gap-1.5 shadow-xs"
                        >
                          <span>View Course</span>
                          <ChevronRight className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                  </div>

                  {/* Metrics & Rationale */}
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4 p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs">
                    <div className="md:col-span-3 space-y-1">
                      <div className="flex items-center gap-1.5 text-indigo-700 font-semibold">
                        <HelpCircle className="w-3.5 h-3.5 text-indigo-600" />
                        <span>WHY THIS COURSE IS IN YOUR PATH</span>
                      </div>
                      <p className="text-slate-700 leading-relaxed">{item.reason}</p>
                    </div>

                    <div className="border-t md:border-t-0 md:border-l border-slate-200 pt-2 md:pt-0 md:pl-4 flex flex-col justify-center space-y-1">
                      <div className="flex justify-between text-[11px] text-slate-600">
                        <span>Current Mastery:</span>
                        <strong className="text-slate-900">{item.current_mastery}%</strong>
                      </div>
                      <div className="flex justify-between text-[11px] text-slate-600">
                        <span>Target Mastery:</span>
                        <strong className="text-slate-900">{item.target_mastery}%</strong>
                      </div>
                      {item.skill_gap > 0 && (
                        <div className="flex justify-between text-[11px] text-rose-600 font-semibold">
                          <span>Skill Gap:</span>
                          <span>{item.skill_gap}%</span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
