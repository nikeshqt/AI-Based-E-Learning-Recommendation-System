import React, { useEffect, useState } from 'react';
import { Target, TrendingUp, AlertTriangle, CheckCircle2, ShieldAlert, BookOpen } from 'lucide-react';
import { fetchUserSkillGaps } from '../services/skillGapService';
import type { SkillGapResponse } from '../types/skillGap';

interface SkillGapPageProps {
  onNavigateToRecommendations?: () => void;
}

export const SkillGapPage: React.FC<SkillGapPageProps> = ({ onNavigateToRecommendations }) => {
  const [data, setData] = useState<SkillGapResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadGaps = async () => {
      try {
        setLoading(true);
        const res = await fetchUserSkillGaps();
        setData(res);
      } catch (err: any) {
        setError(err.message || 'Failed to load skill gap analysis.');
      } finally {
        setLoading(false);
      }
    };

    loadGaps();
  }, []);

  const getCategoryBadge = (category: string) => {
    switch (category) {
      case 'STRONG':
        return (
          <span className="inline-flex items-center gap-1 text-xs px-2.5 py-1 bg-emerald-50 text-emerald-700 border border-emerald-200 font-semibold rounded-md">
            <CheckCircle2 className="w-3.5 h-3.5" />
            Strong
          </span>
        );
      case 'DEVELOPING':
        return (
          <span className="inline-flex items-center gap-1 text-xs px-2.5 py-1 bg-blue-50 text-blue-700 border border-blue-200 font-semibold rounded-md">
            <TrendingUp className="w-3.5 h-3.5" />
            Developing
          </span>
        );
      case 'NEEDS_IMPROVEMENT':
        return (
          <span className="inline-flex items-center gap-1 text-xs px-2.5 py-1 bg-amber-50 text-amber-700 border border-amber-200 font-semibold rounded-md">
            <AlertTriangle className="w-3.5 h-3.5" />
            Needs Improvement
          </span>
        );
      case 'CRITICAL_GAP':
        return (
          <span className="inline-flex items-center gap-1 text-xs px-2.5 py-1 bg-rose-50 text-rose-700 border border-rose-200 font-semibold rounded-md">
            <ShieldAlert className="w-3.5 h-3.5" />
            Critical Gap
          </span>
        );
      default:
        return (
          <span className="text-xs px-2.5 py-1 bg-slate-100 text-slate-700 border border-slate-200 font-semibold rounded-md">
            {category}
          </span>
        );
    }
  };

  const getPriorityBadge = (priorityLevel?: string) => {
    if (priorityLevel === 'High') {
      return <span className="text-xs px-2 py-0.5 bg-rose-100 text-rose-800 font-semibold rounded">High Priority</span>;
    }
    if (priorityLevel === 'Medium') {
      return <span className="text-xs px-2 py-0.5 bg-amber-100 text-amber-800 font-semibold rounded">Medium Priority</span>;
    }
    return <span className="text-xs px-2 py-0.5 bg-slate-100 text-slate-700 font-semibold rounded">Low Priority</span>;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border-3 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-sm font-medium text-slate-600">Calculating skill gaps and career goal targets...</p>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="bg-rose-50 border border-rose-200 rounded-xl p-6 text-rose-800">
        <h3 className="font-semibold text-lg mb-1">Error Loading Skill Gap Analysis</h3>
        <p className="text-sm">{error || 'Could not fetch skill gap data.'}</p>
      </div>
    );
  }

  const prioritySkills = data.skills.filter((s) => s.gap > 0);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Skill Gap Analysis</h1>
        <p className="text-sm text-slate-600 mt-1">
          See which skills you need to strengthen to reach your learning goal.
        </p>
      </div>

      {/* Top Section: Goal & Overall Readiness */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <Target className="w-5 h-5 text-indigo-600" />
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Current Goal</span>
          </div>
          <h2 className="text-xl font-bold text-slate-900">{data.learning_goal}</h2>
          <p className="text-xs text-slate-600 mt-1">
            Target proficiency thresholds derived from industry domain benchmarks and curriculum requirements.
          </p>
        </div>

        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Overall Readiness</span>
            <span className="text-lg font-bold text-indigo-600">{data.overall_readiness}%</span>
          </div>
          <div className="w-full h-3 bg-slate-100 rounded-full overflow-hidden border border-slate-200">
            <div
              className="h-full bg-indigo-600 transition-all duration-500 rounded-full"
              style={{ width: `${Math.min(100, Math.max(0, data.overall_readiness))}%` }}
            />
          </div>
          <p className="text-xs text-slate-500 mt-2 text-right">
            Based on {data.skills.length} target skills for {data.learning_goal}
          </p>
        </div>
      </div>

      {/* Skill Gap Overview */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs space-y-6">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <h3 className="text-lg font-bold text-slate-900">Skill Gap Overview</h3>
          <div className="flex items-center gap-4 text-xs font-medium text-slate-600">
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 bg-indigo-600 rounded-xs"></span>
              Current Mastery
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 bg-slate-300 rounded-xs"></span>
              Target Mastery
            </div>
          </div>
        </div>

        <div className="space-y-6">
          {data.skills.map((item) => (
            <div key={item.skill} className="space-y-2">
              <div className="flex items-center justify-between flex-wrap gap-2">
                <div className="flex items-center gap-2">
                  <span className="font-semibold text-slate-900 text-sm">{item.skill}</span>
                  {item.is_prerequisite && (
                    <span className="text-[10px] px-1.5 py-0.5 bg-slate-100 text-slate-600 font-medium rounded border border-slate-200">
                      Prerequisite
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-xs text-slate-600">
                    <strong className="text-slate-900">{item.current_mastery}%</strong> → {item.target_mastery}%
                    {item.gap > 0 && <span className="ml-2 font-medium text-rose-600">({item.gap}% gap)</span>}
                  </span>
                  {getCategoryBadge(item.category)}
                </div>
              </div>

              {/* Progress / Comparison Bar */}
              <div className="relative w-full h-4 bg-slate-100 rounded-md overflow-hidden border border-slate-200">
                {/* Target Marker Background */}
                <div
                  className="absolute top-0 bottom-0 left-0 bg-slate-200 opacity-60"
                  style={{ width: `${Math.min(100, item.target_mastery)}%` }}
                />
                {/* Current Mastery Bar */}
                <div
                  className="absolute top-0 bottom-0 left-0 bg-indigo-600 rounded-l-md transition-all duration-300"
                  style={{ width: `${Math.min(100, item.current_mastery)}%` }}
                />
                {/* Target Pin Line */}
                <div
                  className="absolute top-0 bottom-0 w-0.5 bg-slate-600 z-10"
                  style={{ left: `${Math.min(100, item.target_mastery)}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Priority Skills */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div>
            <h3 className="text-lg font-bold text-slate-900">Priority Skills</h3>
            <p className="text-xs text-slate-600">
              Skills ranked by gap size, prerequisite importance, and goal impact.
            </p>
          </div>
          <span className="text-xs px-2.5 py-1 bg-indigo-50 text-indigo-700 border border-indigo-100 font-semibold rounded-md">
            {prioritySkills.length} Priority Gaps
          </span>
        </div>

        {prioritySkills.length === 0 ? (
          <div className="p-6 text-center text-slate-600 text-sm bg-slate-50 rounded-lg border border-slate-200">
            🎉 Great job! You have achieved or exceeded target mastery for all skills required for {data.learning_goal}.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {prioritySkills.map((item) => (
              <div
                key={item.skill}
                className="border border-slate-200 rounded-xl p-4 bg-white hover:border-indigo-200 transition-colors flex flex-col justify-between space-y-4"
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-bold text-slate-900 text-base">{item.skill}</h4>
                    {getPriorityBadge(item.priority_level)}
                  </div>

                  <div className="grid grid-cols-3 gap-2 py-2 border-y border-slate-100 text-center text-xs my-2">
                    <div>
                      <span className="block text-slate-500 text-[10px] uppercase">Current</span>
                      <span className="font-bold text-slate-900 text-sm">{item.current_mastery}%</span>
                    </div>
                    <div>
                      <span className="block text-slate-500 text-[10px] uppercase">Target</span>
                      <span className="font-bold text-slate-900 text-sm">{item.target_mastery}%</span>
                    </div>
                    <div>
                      <span className="block text-slate-500 text-[10px] uppercase">Gap</span>
                      <span className="font-bold text-rose-600 text-sm">{item.gap}%</span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between text-xs text-slate-600 mt-2">
                    <span>Category: {getCategoryBadge(item.category)}</span>
                    <span className="text-slate-500 font-mono">Score: {item.priority.toFixed(2)}</span>
                  </div>
                </div>

                <button
                  onClick={onNavigateToRecommendations}
                  className="w-full py-2 px-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs rounded-lg transition-colors flex items-center justify-center gap-1.5 shadow-xs"
                >
                  <BookOpen className="w-3.5 h-3.5" />
                  View Recommended Courses
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
