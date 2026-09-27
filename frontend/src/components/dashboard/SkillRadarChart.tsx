import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';

interface SkillData {
  skill_name: string;
  mastery_score: number; // 0-100
}

interface SkillRadarChartProps {
  skills?: SkillData[];
}

const defaultSkills: SkillData[] = [
  { skill_name: 'Python', mastery_score: 80 },
  { skill_name: 'Networking', mastery_score: 40 },
  { skill_name: 'Linux', mastery_score: 30 },
  { skill_name: 'Cybersecurity', mastery_score: 60 },
  { skill_name: 'SQL', mastery_score: 75 },
  { skill_name: 'AI / ML', mastery_score: 65 },
];

export const SkillRadarChart: React.FC<SkillRadarChartProps> = ({ skills = defaultSkills }) => {
  return (
    <div className="bg-white border border-slate-200 rounded-xl p-5 flex flex-col justify-between h-full shadow-xs">
      <div>
        <h3 className="text-base font-bold text-slate-900 mb-0.5">Skill Mastery Matrix</h3>
        <p className="text-xs text-slate-500 mb-4">Evaluated skill levels across technical domains</p>
      </div>
      <div className="w-full h-64">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="75%" data={skills}>
            <PolarGrid stroke="#E2E8F0" />
            <PolarAngleAxis dataKey="skill_name" stroke="#64748B" tick={{ fill: '#475569', fontSize: 11, fontWeight: 500 }} />
            <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#CBD5E1" tick={{ fill: '#94A3B8', fontSize: 10 }} />
            <Radar name="Mastery" dataKey="mastery_score" stroke="#4F46E5" fill="#4F46E5" fillOpacity={0.2} />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
