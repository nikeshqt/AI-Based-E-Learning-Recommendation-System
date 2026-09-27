import React, { useEffect, useState } from 'react';
import { GitBranch, CheckCircle2, CircleDot, ArrowRight } from 'lucide-react';
import { fetchCurrentLearningPath } from '../../services/learningPathService';
import type { LearningPathResponse } from '../../types/learningPath';

interface LearningRoadmapProps {
  onNavigateToLearningPath?: () => void;
}

export const LearningRoadmap: React.FC<LearningRoadmapProps> = ({ onNavigateToLearningPath }) => {
  const [pathData, setPathData] = useState<LearningPathResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const loadRoadmap = async () => {
      try {
        setLoading(true);
        const res = await fetchCurrentLearningPath();
        if (res) {
          setPathData(res);
        }
      } catch (err) {
        console.warn('Using default roadmap display:', err);
      } finally {
        setLoading(false);
      }
    };
    loadRoadmap();
  }, []);

  if (loading) {
    return (
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs animate-pulse space-y-3">
        <div className="h-4 bg-slate-200 rounded w-1/3"></div>
        <div className="h-20 bg-slate-100 rounded w-full"></div>
      </div>
    );
  }

  const goal = pathData?.career_goal || 'Cybersecurity Analyst';
  const duration = pathData?.total_duration_hours || 24;
  const stages = pathData?.stages || [
    {
      stage_number: 1,
      stage_title: 'Foundation & Prerequisites',
      stage_name: 'Foundation',
      description: 'Build essential prerequisite knowledge and core technical fundamentals.',
      target_skills: ['Linux', 'Networking'],
      estimated_duration_hours: 8,
      status: 'AVAILABLE',
      courses: [],
    },
    {
      stage_number: 2,
      stage_title: 'Core Domain Mastery',
      stage_name: 'Core Skills',
      description: 'Master primary domain competencies and hands-on operational practice.',
      target_skills: ['Cybersecurity', 'Python'],
      estimated_duration_hours: 10,
      status: 'LOCKED',
      courses: [],
    },
  ];

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <GitBranch className="w-4 h-4 text-indigo-600" />
            Personalized Roadmap
          </h3>
          <p className="text-xs text-slate-500">Targeting {goal} • {duration} Hours Total</p>
        </div>
        <button
          onClick={onNavigateToLearningPath}
          className="text-xs font-semibold text-indigo-600 hover:text-indigo-800 flex items-center gap-1"
        >
          View Full Path
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>

      <div className="relative pl-6 space-y-4 before:absolute before:left-2.5 before:top-3 before:bottom-3 before:w-0.5 before:bg-slate-200">
        {stages.map((stage, idx) => (
          <div key={stage.stage_number} className="relative">
            <div className="absolute -left-6 top-0 -translate-x-1/2 p-0.5 rounded-full bg-white border border-slate-300">
              {idx === 0 ? (
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              ) : (
                <CircleDot className="w-4 h-4 text-indigo-600" />
              )}
            </div>
            <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-indigo-700">Stage 0{stage.stage_number}</span>
                <span className="text-[11px] text-slate-500">{stage.estimated_duration_hours} Hours</span>
              </div>
              <h4 className="text-sm font-bold text-slate-900 mt-0.5">{stage.stage_title}</h4>
              <p className="text-xs text-slate-600 mt-1">{stage.description}</p>
              <div className="flex items-center gap-1.5 mt-2.5 flex-wrap">
                {stage.target_skills.map((skill) => (
                  <span key={skill} className="text-[10px] px-2 py-0.5 rounded bg-white border border-slate-200 text-slate-700 font-medium">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

