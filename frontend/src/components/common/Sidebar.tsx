import React from 'react';
import {
  LayoutDashboard,
  ClipboardCheck,
  Target,
  Compass,
  GitBranch,
  BookOpen,
  PlayCircle,
  TrendingUp,
  MessageSquare,
  BarChart3,
  User,
} from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab }) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'assessment', label: 'Skill Assessment', icon: ClipboardCheck },
    { id: 'skill-gaps', label: 'Skill Gap Analysis', icon: Target },
    { id: 'recommendations', label: 'Recommendations', icon: Compass },
    { id: 'learning-path', label: 'Learning Path', icon: GitBranch },
    { id: 'courses', label: 'Courses', icon: BookOpen },
    { id: 'learn', label: 'Course Reader', icon: PlayCircle },
    { id: 'progress', label: 'Progress', icon: TrendingUp },
    { id: 'ai-tutor', label: 'AI Tutor', icon: MessageSquare },
    { id: 'analytics', label: 'Analytics', icon: BarChart3 },
    { id: 'settings', label: 'Profile & Settings', icon: User },
  ];


  return (
    <aside className="w-64 bg-white border-r border-slate-200 p-4 flex flex-col justify-between hidden md:flex shrink-0 min-h-[calc(100vh-5rem)] rounded-xl">
      <div className="space-y-6">
        <div className="px-3 py-1 text-xs font-semibold text-slate-400 uppercase tracking-wider">
          Main Menu
        </div>
        <nav className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-indigo-50 text-indigo-700 font-semibold border-l-4 border-indigo-600'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-indigo-600' : 'text-slate-400'}`} />
                {item.label}
              </button>
            );
          })}
        </nav>
      </div>

      <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-600">
        <div className="font-semibold text-slate-800 mb-0.5">PostgreSQL RecSys v2.0</div>
        <div className="text-[11px] text-slate-500">Active Engine: TF-IDF & Skill Gap Matrix</div>
      </div>
    </aside>
  );
};
