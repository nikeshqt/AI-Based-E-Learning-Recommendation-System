import React, { useEffect, useState } from 'react';
import { Compass, Filter, RefreshCw, Zap } from 'lucide-react';
import { RecommendedFeed } from '../components/dashboard/RecommendedFeed';
import { CourseCard } from '../components/courses/CourseCard';
import { fetchPersonalizedRecommendations } from '../services/recommendationService';
import type { RecommendationItem } from '../types/recommendation';

interface RecommendationsPageProps {
  onSelectCourse?: (courseId: string) => void;
}

const mockCatalogRecs: RecommendationItem[] = [
  {
    recommendation_id: 'rec_01',
    match_score: 0.96,
    recommendation_reason: 'Recommended because your Networking mastery is currently 40%, while your Cybersecurity Analyst goal requires 80%. This course directly targets the Networking skill gap.',
    stage_sources: ['KnowledgeGraph', 'VectorSearch'],
    prerequisites_met: true,
    target_skill_gap: 'Networking',
    matched_skills: ['Networking', 'Cybersecurity'],
    skill_gaps_addressed: ['Networking'],
    current_skill_level: 40,
    target_skill_level: 80,
    gap: 40,
    course: {
      course_id: 'crs_sec_03',
      title: 'Cybersecurity Fundamentals: Network Defense & Wireshark',
      description: 'Learn packet inspection, intrusion detection systems, and network vulnerability analysis.',
      instructor_name: 'Sarah Connor',
      thumbnail_url: '',
      category: 'Cybersecurity',
      difficulty_level: 'Intermediate',
      duration_hours: 8.0,
      rating: 4.9,
      enrolled_count: 3100,
      prerequisites: ['Networking', 'Linux'],
      skills_taught: ['Networking', 'Cybersecurity', 'Wireshark'],
      lessons: [],
    },
  },
  {
    recommendation_id: 'rec_02',
    match_score: 0.91,
    recommendation_reason: 'Your Linux mastery is 35%, and Linux is an important prerequisite for your Cybersecurity Analyst goal. Improving Linux will reduce a major skill gap.',
    stage_sources: ['VectorSearch', 'CollaborativeFiltering'],
    prerequisites_met: true,
    target_skill_gap: 'Linux',
    matched_skills: ['Linux'],
    skill_gaps_addressed: ['Linux'],
    current_skill_level: 35,
    target_skill_level: 75,
    gap: 40,
    course: {
      course_id: 'crs_qdrant_02',
      title: 'Advanced Linux System Administration & Shell Automation',
      description: 'Master bash scripting, process management, security permissions, and Linux administration.',
      instructor_name: 'Marcus Vance',
      thumbnail_url: '',
      category: 'Operating Systems',
      difficulty_level: 'Intermediate',
      duration_hours: 6.0,
      rating: 4.8,
      enrolled_count: 2890,
      prerequisites: ['Python'],
      skills_taught: ['Linux', 'Bash', 'Administration'],
      lessons: [],
    },
  },
];

export const RecommendationsPage: React.FC<RecommendationsPageProps> = ({ onSelectCourse }) => {
  const [recs, setRecs] = useState<RecommendationItem[]>(mockCatalogRecs);
  const [loading, setLoading] = useState<boolean>(false);

  const loadRecs = async () => {
    try {
      setLoading(true);
      const res = await fetchPersonalizedRecommendations('usr_demo', 10);
      if (res && res.recommendations && res.recommendations.length > 0) {
        setRecs(res.recommendations);
      }
    } catch (err) {
      console.warn('Using fallback recommendations feed:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRecs();
  }, []);

  return (
    <div className="space-y-6">
      <div className="bg-white border border-slate-200 rounded-xl p-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 shadow-xs">
        <div>
          <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            <Compass className="w-5 h-5 text-indigo-600" />
            AI Course Recommendations
          </h2>
          <p className="text-xs text-slate-600 mt-1">
            Data-driven recommendations tailored to your career goal requirements and skill gaps.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button className="px-3.5 py-2 rounded-lg bg-white border border-slate-200 text-xs font-medium text-slate-700 hover:bg-slate-50 flex items-center gap-1.5">
            <Filter className="w-3.5 h-3.5 text-slate-500" /> Filter
          </button>
          <button
            onClick={loadRecs}
            disabled={loading}
            className="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-xs font-semibold text-white flex items-center gap-1.5 transition-colors"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} /> Re-Rank Catalog
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="bg-white border border-slate-200 rounded-xl p-4 space-y-4 shadow-xs h-fit">
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <Zap className="w-4 h-4 text-amber-500" />
            RecSys Tuning
          </h3>
          <div className="space-y-3 text-xs">
            <div>
              <label className="text-slate-600 block mb-1 font-medium">Skill Gap Weight</label>
              <input type="range" min="0" max="100" defaultValue="40" className="w-full accent-indigo-600" />
            </div>
            <div>
              <label className="text-slate-600 block mb-1 font-medium">Career Goal Alignment</label>
              <input type="range" min="0" max="100" defaultValue="80" className="w-full accent-indigo-600" />
            </div>
            <div>
              <label className="text-slate-600 block mb-1 font-medium">Prerequisite Strictness</label>
              <input type="range" min="0" max="100" defaultValue="90" className="w-full accent-indigo-600" />
            </div>
          </div>
        </div>

        <div className="lg:col-span-3 space-y-6">
          <RecommendedFeed recommendations={recs} onSelectCourse={onSelectCourse} />

          <div>
            <h3 className="text-base font-bold text-slate-900 mb-3">Recommended Next Steps</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {recs.map((rec) => (
                <CourseCard
                  key={rec.recommendation_id}
                  course={rec.course}
                  matchScore={rec.match_score}
                  onSelect={onSelectCourse}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

