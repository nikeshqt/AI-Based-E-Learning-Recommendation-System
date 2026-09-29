import React from 'react';
import {
  LayoutDashboard,
  Users,
  BookOpen,
  TrendingUp,
  BarChart3,
  History,
  Settings,
  LogOut,
  ShieldCheck,
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export type AdminTab =
  | 'dashboard'
  | 'students'
  | 'courses'
  | 'progress'
  | 'analytics'
  | 'activity'
  | 'settings';

interface AdminSidebarProps {
  activeTab: AdminTab;
  setActiveTab: (tab: AdminTab) => void;
  onSelectStudentId?: (id: string | null) => void;
}

export const AdminSidebar: React.FC<AdminSidebarProps> = ({
  activeTab,
  setActiveTab,
  onSelectStudentId,
}) => {
  const { logout } = useAuth();

  const navItems = [
    { id: 'dashboard' as AdminTab, label: 'Dashboard', icon: LayoutDashboard },
    { id: 'students' as AdminTab, label: 'Students', icon: Users },
    { id: 'courses' as AdminTab, label: 'Courses', icon: BookOpen },
    { id: 'progress' as AdminTab, label: 'Course Progress', icon: TrendingUp },
    { id: 'analytics' as AdminTab, label: 'Analytics', icon: BarChart3 },
    { id: 'activity' as AdminTab, label: 'Activity Logs', icon: History },
    { id: 'settings' as AdminTab, label: 'Settings', icon: Settings },
  ];

  const handleTabClick = (tab: AdminTab) => {
    if (onSelectStudentId) {
      onSelectStudentId(null);
    }
    setActiveTab(tab);
  };

  return (
    <aside className="w-64 bg-white border border-slate-200 p-4 flex flex-col justify-between shrink-0 min-h-[calc(100vh-7rem)] rounded-xl shadow-xs font-sans">
      <div className="space-y-6">
        <div className="flex items-center gap-2.5 px-3 py-2 bg-indigo-50 border border-indigo-100 rounded-lg">
          <ShieldCheck className="w-4 h-4 text-indigo-700" />
          <span className="text-xs font-bold text-indigo-900 tracking-wide uppercase">
            Admin Console
          </span>
        </div>

        <div>
          <div className="px-3 py-1 text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2">
            Navigation
          </div>
          <nav className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => handleTabClick(item.id)}
                  className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-colors cursor-pointer ${
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
      </div>

      <div className="pt-4 border-t border-slate-200">
        <button
          onClick={logout}
          className="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium text-rose-600 hover:bg-rose-50 transition-colors cursor-pointer"
        >
          <LogOut className="w-4 h-4 text-rose-500" />
          Logout
        </button>
      </div>
    </aside>
  );
};
