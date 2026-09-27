import React from 'react';
import type { LucideIcon } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  trend?: string;
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
}) => {
  return (
    <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-xs flex items-start justify-between">
      <div>
        <span className="text-xs font-medium text-slate-500 uppercase tracking-wider">{title}</span>
        <div className="text-2xl font-bold text-slate-900 mt-1.5">{value}</div>
        {subtitle && <div className="text-xs text-slate-500 mt-1">{subtitle}</div>}
        {trend && <div className="text-xs font-semibold text-emerald-600 mt-2">{trend}</div>}
      </div>
      <div className="p-2.5 bg-indigo-50 border border-indigo-100 rounded-lg text-indigo-600">
        <Icon className="w-5 h-5" />
      </div>
    </div>
  );
};
