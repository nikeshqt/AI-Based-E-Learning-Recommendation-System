import React from 'react';
import { StatCard } from '../components/common/StatCard';
import { Award, Flame, Clock, CheckCircle2 } from 'lucide-react';

export const ProgressPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="bg-white border border-slate-200 rounded-xl p-6">
        <h2 className="text-2xl font-bold text-slate-900">Learner Progress</h2>
        <p className="text-xs text-slate-600 mt-1">
          Track your module completions, quiz scores, and skill progression over time.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard title="Overall Completion" value="68%" subtitle="14 of 20 modules completed" icon={Award} trend="+12% this month" />
        <StatCard title="Learning Streak" value="12 Days" subtitle="Daily goal: 45 mins" icon={Flame} trend="Active streak" />
        <StatCard title="Total Study Time" value="38.5 hrs" subtitle="Avg 1.2 hrs/day" icon={Clock} />
        <StatCard title="Quizzes Passed" value="18 / 20" subtitle="First-try pass rate 90%" icon={CheckCircle2} />
      </div>

      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs space-y-4">
        <h3 className="text-lg font-bold text-slate-900">Current Course Enrollments</h3>
        <div className="space-y-3">
          {[
            { title: 'Graph Neural Networks for Recommendation Systems', progress: 85, category: 'AI' },
            { title: 'Cybersecurity Fundamentals: Network Defense', progress: 50, category: 'Cybersecurity' },
            { title: 'Production Vector Search with Qdrant', progress: 30, category: 'Data Engineering' },
          ].map((item) => (
            <div key={item.title} className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
              <div className="flex justify-between items-center text-xs">
                <span className="font-semibold text-slate-900 text-sm">{item.title}</span>
                <span className="font-bold text-indigo-600">{item.progress}% Completed</span>
              </div>
              <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
                <div
                  className="bg-indigo-600 h-full rounded-full transition-all"
                  style={{ width: `${item.progress}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
