import React from 'react';
import { BarChart3, TrendingUp, CheckCircle, Clock } from 'lucide-react';
import { SkillRadarChart } from '../components/dashboard/SkillRadarChart';
import { StatCard } from '../components/common/StatCard';

export const AnalyticsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs">
        <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
          <BarChart3 className="w-5 h-5 text-indigo-600" />
          Skill Analytics & Performance Metrics
        </h2>
        <p className="text-xs text-slate-600 mt-1">
          Detailed metrics on learning velocity, topic retention, and recommendation engine precision.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <StatCard title="Hours Spent Learning" value="42.5 hrs" icon={Clock} trend="+12.4 hrs vs last month" />
        <StatCard title="Quiz Success Rate" value="88.4%" icon={CheckCircle} trend="+4.1% improvement" />
        <StatCard title="Skill Acquisition Rate" value="3.2 Skills/Mo" icon={TrendingUp} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <SkillRadarChart />
        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs">
          <h3 className="text-base font-bold text-slate-900 mb-3">RecSys Model Performance</h3>
          <div className="space-y-3 text-xs text-slate-700">
            <div className="flex justify-between p-3 rounded-lg bg-slate-50 border border-slate-200">
              <span className="font-medium">Explicit Course Ratings Avg</span>
              <span className="font-bold text-indigo-600">4.85 / 5.0</span>
            </div>
            <div className="flex justify-between p-3 rounded-lg bg-slate-50 border border-slate-200">
              <span className="font-medium font-medium">Recommendation Click-Through Rate (CTR)</span>
              <span className="font-bold text-emerald-600">34.2%</span>
            </div>
            <div className="flex justify-between p-3 rounded-lg bg-slate-50 border border-slate-200">
              <span className="font-medium">Prerequisite Satisfaction Ratio</span>
              <span className="font-bold text-blue-600">98.1%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
