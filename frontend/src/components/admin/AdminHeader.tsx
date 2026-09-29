import React from 'react';
import { ShieldCheck, LogOut, ExternalLink } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

interface AdminHeaderProps {
  onSwitchToStudentView?: () => void;
}

export const AdminHeader: React.FC<AdminHeaderProps> = ({ onSwitchToStudentView }) => {
  const { user, logout } = useAuth();
  const displayName = user?.full_name || 'System Administrator';
  const email = user?.email || 'admin@elearning.io';

  return (
    <header className="bg-white border border-slate-200 rounded-xl px-6 py-3.5 mb-6 flex items-center justify-between shadow-xs font-sans">
      <div className="flex items-center gap-3">
        <div className="p-2 bg-indigo-50 border border-indigo-100 rounded-lg">
          <ShieldCheck className="w-5 h-5 text-indigo-600" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-lg font-bold text-slate-900 tracking-tight">NeuralLearn AI</h1>
            <span className="px-2 py-0.5 text-[10px] font-semibold bg-indigo-100 text-indigo-700 rounded-full uppercase">
              Admin Portal
            </span>
          </div>
          <p className="text-xs text-slate-500">
            System Administration & Learning Management
          </p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        {onSwitchToStudentView && (
          <button
            onClick={onSwitchToStudentView}
            className="hidden md:inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-600 hover:text-indigo-600 hover:bg-slate-100 border border-slate-200 rounded-lg transition-colors cursor-pointer"
          >
            <ExternalLink className="w-3.5 h-3.5" />
            Switch to Student View
          </button>
        )}

        <div className="flex items-center gap-3 pl-3 border-l border-slate-200">
          <div className="w-8 h-8 rounded-full bg-slate-900 flex items-center justify-center text-white font-semibold text-xs uppercase shadow-xs">
            {displayName.charAt(0)}
          </div>
          <div className="hidden sm:block text-left">
            <div className="text-xs font-semibold text-slate-900">{displayName}</div>
            <div className="text-[11px] text-slate-500">{email}</div>
          </div>
          <button
            onClick={logout}
            title="Sign Out"
            className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors ml-1 cursor-pointer"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
};
