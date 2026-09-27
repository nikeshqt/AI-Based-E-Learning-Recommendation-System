import React from 'react';
import { Bell, Search, Sparkles, LogOut } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

interface HeaderProps {
  userName?: string;
  userGoal?: string;
  activeTab?: string;
}

export const Header: React.FC<HeaderProps> = ({
  userName: propUserName,
  userGoal: propUserGoal,
}) => {
  const { user, logout } = useAuth();

  const displayName = user?.full_name || propUserName || 'Student';
  const displayGoal = user?.learning_goal || propUserGoal || 'Cybersecurity Analyst';

  return (
    <header className="bg-white border border-slate-200 rounded-xl px-6 py-3.5 mb-6 flex items-center justify-between shadow-xs font-sans">
      <div className="flex items-center gap-3">
        <div className="p-2 bg-indigo-50 border border-indigo-100 rounded-lg">
          <Sparkles className="w-5 h-5 text-indigo-600" />
        </div>
        <div>
          <h1 className="text-lg font-bold text-slate-900 tracking-tight">NeuralLearn AI</h1>
          <p className="text-xs text-slate-500">
            Goal: <span className="text-slate-700 font-semibold">{displayGoal}</span>
          </p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="relative hidden md:block">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search courses, skills, or topics..."
            className="pl-9 pr-4 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:border-indigo-500 w-64"
          />
        </div>

        <button className="p-2 rounded-lg text-slate-500 hover:text-slate-800 hover:bg-slate-100 transition-colors relative">
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-indigo-600 rounded-full"></span>
        </button>

        <div className="flex items-center gap-3 pl-3 border-l border-slate-200">
          <div className="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center text-white font-semibold text-xs uppercase">
            {displayName.charAt(0)}
          </div>
          <div className="hidden sm:block text-left">
            <div className="text-xs font-semibold text-slate-900">{displayName}</div>
            <div className="text-[11px] text-slate-500">Student Account</div>
          </div>
          <button
            onClick={logout}
            title="Sign Out"
            className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors ml-1"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
};
