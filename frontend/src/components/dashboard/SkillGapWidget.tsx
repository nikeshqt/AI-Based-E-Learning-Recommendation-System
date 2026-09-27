import React, { useEffect, useState } from 'react';
import { ArrowRight, AlertTriangle } from 'lucide-react';
import { fetchUserSkillGaps } from '../../services/skillGapService';
import type { SkillGapItem } from '../../types/skillGap';

interface SkillGapWidgetProps {
  onNavigateToSkillGaps?: () => void;
}

export const SkillGapWidget: React.FC<SkillGapWidgetProps> = ({ onNavigateToSkillGaps }) => {
  const [topGaps, setTopGaps] = useState<SkillGapItem[]>([]);
  const [goal, setGoal] = useState<string>('Cybersecurity Analyst');
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const res = await fetchUserSkillGaps();
        if (res) {
          setGoal(res.learning_goal);
          const activeGaps = res.skills.filter((s) => s.gap > 0).slice(0, 3);
          setTopGaps(activeGaps);
        }
      } catch (err) {
        console.error('Failed to load top skill gaps widget:', err);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs animate-pulse space-y-3">
        <div className="h-4 bg-slate-200 rounded w-1/2"></div>
        <div className="h-3 bg-slate-100 rounded w-full"></div>
        <div className="h-3 bg-slate-100 rounded w-full"></div>
      </div>
    );
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs space-y-4">
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div>
          <h3 className="text-sm font-bold text-slate-900">Your Biggest Skill Gaps</h3>
          <p className="text-[11px] text-slate-500">Targeting {goal}</p>
        </div>
        <span className="p-1 bg-amber-50 text-amber-600 rounded-md border border-amber-100">
          <AlertTriangle className="w-4 h-4" />
        </span>
      </div>

      <div className="space-y-3">
        {topGaps.length === 0 ? (
          <p className="text-xs text-slate-500 italic text-center py-2">
            No active skill gaps! You meet target mastery.
          </p>
        ) : (
          topGaps.map((item) => (
            <div key={item.skill} className="space-y-1">
              <div className="flex items-center justify-between text-xs font-semibold">
                <span className="text-slate-800">{item.skill}</span>
                <span className="text-rose-600 font-bold">{item.gap}% gap</span>
              </div>
              <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden border border-slate-200">
                <div
                  className="h-full bg-indigo-600 rounded-full"
                  style={{ width: `${Math.min(100, item.current_mastery)}%` }}
                />
              </div>
              <div className="flex items-center justify-between text-[10px] text-slate-500">
                <span>Current: {item.current_mastery}%</span>
                <span>Target: {item.target_mastery}%</span>
              </div>
            </div>
          ))
        )}
      </div>

      <button
        onClick={onNavigateToSkillGaps}
        className="w-full py-2 px-3 bg-slate-50 hover:bg-slate-100 text-indigo-600 font-semibold text-xs rounded-lg border border-slate-200 transition-colors flex items-center justify-center gap-1.5"
      >
        <span>View Skill Gap Analysis</span>
        <ArrowRight className="w-3.5 h-3.5" />
      </button>
    </div>
  );
};
