import React, { useEffect, useState } from 'react';
import type { RecommendationItem } from '../../types/recommendation';
import { Sparkles, Clock, CheckCircle2, ChevronRight, HelpCircle } from 'lucide-react';
import { formatPercentage, formatDuration } from '../../utils/formatters';
import { fetchPersonalizedRecommendations } from '../../services/recommendationService';

interface RecommendedFeedProps {
  recommendations?: RecommendationItem[];
  onSelectCourse?: (courseId: string) => void;
}

export const RecommendedFeed: React.FC<RecommendedFeedProps> = ({
  recommendations: initialRecs,
  onSelectCourse,
}) => {
  const [recs, setRecs] = useState<RecommendationItem[]>(initialRecs || []);
  const [loading, setLoading] = useState<boolean>(!initialRecs || initialRecs.length === 0);

  useEffect(() => {
    let isMounted = true;
    const loadRecs = async () => {
      try {
        setLoading(true);
        const data = await fetchPersonalizedRecommendations();
        if (isMounted && data && data.recommendations) {
          setRecs(data.recommendations);
        }
      } catch (err) {
        console.warn('Could not load live recommendations:', err);
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    if (!initialRecs || initialRecs.length === 0) {
      loadRecs();
    } else {
      setRecs(initialRecs);
      setLoading(false);
    }

    return () => {
      isMounted = false;
    };
  }, [initialRecs]);

  if (loading) {
    return (
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs space-y-4">
        <div className="h-5 bg-slate-200 rounded w-1/3 animate-pulse"></div>
        <div className="h-24 bg-slate-100 rounded-xl animate-pulse"></div>
        <div className="h-24 bg-slate-100 rounded-xl animate-pulse"></div>
      </div>
    );
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-indigo-600" />
            AI Recommended Content Feed
          </h3>
          <p className="text-xs text-slate-500">Scored via TF-IDF engine + Skill Gap Matrix</p>
        </div>
        <span className="text-xs px-2.5 py-0.5 rounded-full bg-indigo-50 border border-indigo-100 text-indigo-700 font-semibold">
          {recs.length} Matches Found
        </span>
      </div>

      {recs.length === 0 ? (
        <div className="p-6 text-center bg-slate-50 border border-slate-200 rounded-xl space-y-2">
          <p className="text-sm text-slate-700 font-medium">No personalized recommendations yet.</p>
          <p className="text-xs text-slate-500">
            Complete your skill assessment or set a career goal to receive AI course recommendations.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {recs.map((item) => (
            <div
              key={item.recommendation_id}
              onClick={() => onSelectCourse && onSelectCourse(item.course.course_id)}
              className="p-4 rounded-xl bg-slate-50 border border-slate-200 hover:border-indigo-300 transition-all cursor-pointer group flex flex-col gap-3"
            >
              <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 rounded-lg bg-indigo-50 border border-indigo-100 shrink-0 flex items-center justify-center text-indigo-600 font-bold text-base">
                    {item.course.title.charAt(0)}
                  </div>
                  <div>
                    <div className="flex items-center gap-2 flex-wrap">
                      <h4 className="text-sm font-bold text-slate-900 group-hover:text-indigo-600 transition-colors">
                        {item.course.title}
                      </h4>
                      <span className="text-[11px] px-2 py-0.5 rounded bg-white border border-slate-200 text-slate-600 font-medium">
                        {item.course.difficulty_level}
                      </span>
                    </div>

                    <div className="flex items-center gap-4 text-[11px] text-slate-500 mt-1.5">
                      <span className="flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5 text-slate-400" />
                        {formatDuration(item.course.duration_hours)}
                      </span>
                      <span className="flex items-center gap-1 text-emerald-700 font-medium">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                        Prerequisites Met
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3 self-end md:self-center">
                  <div className="text-right">
                    <div className="text-[11px] text-slate-500 font-medium">AI Match</div>
                    <div className="text-base font-bold text-indigo-600">{formatPercentage(item.match_score)}</div>
                  </div>
                  <ChevronRight className="w-5 h-5 text-slate-400 group-hover:text-indigo-600 transition-colors" />
                </div>
              </div>

              {/* Explainable Recommendation Rationale */}
              <div className="p-3 bg-white rounded-lg border border-slate-200 space-y-1.5">
                <div className="flex items-center gap-1.5 text-xs font-semibold text-indigo-700">
                  <HelpCircle className="w-3.5 h-3.5 text-indigo-600" />
                  <span>WHY THIS COURSE?</span>
                </div>
                <p className="text-xs text-slate-700 leading-relaxed font-normal">
                  {item.recommendation_reason}
                </p>
                {item.gap !== undefined && item.gap > 0 && (
                  <div className="flex items-center gap-4 text-[11px] text-slate-500 pt-1 border-t border-slate-100 mt-1">
                    <span>Skill Addressed: <strong className="text-slate-800">{item.target_skill_gap}</strong></span>
                    <span>Current: <strong className="text-slate-800">{item.current_skill_level}%</strong></span>
                    <span>Target: <strong className="text-slate-800">{item.target_skill_level}%</strong></span>
                    <span className="text-rose-600 font-semibold">Gap: {item.gap}%</span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
