import React, { useEffect, useState } from 'react';
import { StatCard } from '../components/common/StatCard';
import { SkillRadarChart } from '../components/dashboard/SkillRadarChart';
import { RecommendedFeed } from '../components/dashboard/RecommendedFeed';
import { LearningRoadmap } from '../components/dashboard/LearningRoadmap';
import { SkillGapWidget } from '../components/dashboard/SkillGapWidget';
import { ContinueLearningWidget } from '../components/dashboard/ContinueLearningWidget';
import { AITutorChat } from '../components/ai-tutor/AITutorChat';
import { BookOpen, Award, Target, Flame } from 'lucide-react';
import { fetchUserSkillGaps } from '../services/skillGapService';
import { fetchDashboardStats } from '../services/courseLearningService';
import { apiClient } from '../services/api';

interface DashboardPageProps {
  onSelectCourse?: (courseId: string) => void;
  onNavigateToSkillGaps?: () => void;
  onNavigateToLearningPath?: () => void;
}

export const DashboardPage: React.FC<DashboardPageProps> = ({
  onSelectCourse,
  onNavigateToSkillGaps,
  onNavigateToLearningPath,
}) => {
  const [userName, setUserName] = useState<string>('Learner');
  const [careerGoal, setCareerGoal] = useState<string>('Not Set');
  const [readinessScore, setReadinessScore] = useState<number>(0);
  const [assessmentStatus, setAssessmentStatus] = useState<string>('Pending');
  const [completedCount, setCompletedCount] = useState<number>(0);
  const [inProgressCount, setInProgressCount] = useState<number>(0);
  const [avgProgress, setAvgProgress] = useState<number>(0);

  useEffect(() => {
    let isMounted = true;

    const loadDashboardData = async () => {
      try {
        // 1. Fetch user profile
        const userRes = await apiClient.get('/users/me').catch(() => null);
        if (userRes && userRes.data && isMounted) {
          if (userRes.data.full_name) setUserName(userRes.data.full_name);
          if (userRes.data.learning_goal) setCareerGoal(userRes.data.learning_goal);
        }

        // 2. Fetch skill gaps for readiness calculation
        const gapRes = await fetchUserSkillGaps().catch(() => null);
        if (gapRes && isMounted) {
          if (gapRes.learning_goal) setCareerGoal(gapRes.learning_goal);
          if (gapRes.skills && gapRes.skills.length > 0) {
            setAssessmentStatus('Completed');
            const avgGap =
              gapRes.skills.reduce((acc, curr) => acc + curr.gap, 0) / gapRes.skills.length;
            setReadinessScore(Math.round(Math.max(0, 100 - avgGap)));
          } else {
            setAssessmentStatus('Pending');
          }
        }

        // 3. Fetch course stats & progress
        const statsRes = await fetchDashboardStats().catch(() => null);
        if (statsRes && isMounted) {
          setCompletedCount(statsRes.completed_courses_count || 0);
          setInProgressCount(statsRes.in_progress_courses_count || 0);
          if (statsRes.continue_learning && statsRes.continue_learning.progress_percentage) {
            setAvgProgress(Math.round(statsRes.continue_learning.progress_percentage));
          }
        }
      } catch (err) {
        console.warn('Dashboard data load warning:', err);
      }
    };

    loadDashboardData();

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <div className="space-y-6 font-sans">
      {/* Welcome Banner & Career Goal */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Welcome back, {userName}!</h2>
          <p className="text-xs text-slate-600 mt-1">
            Track your progress, view AI recommendations, and evaluate your skill gaps.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs px-3 py-1.5 bg-indigo-50 border border-indigo-100 text-indigo-700 font-semibold rounded-lg">
            Career Goal: {careerGoal}
          </span>
        </div>
      </div>

      {/* Key Stats Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Skill Readiness"
          value={`${readinessScore}%`}
          subtitle={`Targeting ${careerGoal}`}
          icon={Target}
        />
        <StatCard
          title="Assessment Status"
          value={assessmentStatus}
          subtitle="Evaluated via RecSys Matrix"
          icon={Award}
          trend={assessmentStatus === 'Completed' ? 'Verified' : 'Action Required'}
        />
        <StatCard
          title="Courses Tracked"
          value={`${completedCount + inProgressCount}`}
          subtitle={`${completedCount} Completed • ${inProgressCount} Active`}
          icon={BookOpen}
        />
        <StatCard
          title="Learning Progress"
          value={`${avgProgress}%`}
          subtitle="Active course progress"
          icon={Flame}
          trend={avgProgress > 0 ? 'Active' : 'Get Started'}
        />
      </div>

      {/* Main Grid Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <ContinueLearningWidget />
          <RecommendedFeed onSelectCourse={onSelectCourse} />
          <LearningRoadmap onNavigateToLearningPath={onNavigateToLearningPath} />
        </div>
        <div className="space-y-6">
          <SkillGapWidget onNavigateToSkillGaps={onNavigateToSkillGaps} />
          <SkillRadarChart />
          <AITutorChat />
        </div>
      </div>
    </div>
  );
};
