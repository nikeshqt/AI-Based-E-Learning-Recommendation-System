import React from 'react';
import { ShieldAlert, ArrowLeft } from 'lucide-react';

interface AccessDeniedProps {
  onReturnToDashboard: () => void;
}

export const AccessDenied: React.FC<AccessDeniedProps> = ({ onReturnToDashboard }) => {
  return (
    <div className="min-h-[70vh] flex items-center justify-center p-6 font-sans">
      <div className="max-w-md w-full bg-white border border-slate-200 rounded-2xl p-8 shadow-xs text-center">
        <div className="w-16 h-16 bg-rose-50 border border-rose-100 rounded-2xl flex items-center justify-center mx-auto mb-5 text-rose-600">
          <ShieldAlert className="w-8 h-8" />
        </div>
        <h2 className="text-xl font-bold text-slate-900 tracking-tight mb-2">Access Denied (HTTP 403)</h2>
        <p className="text-sm text-slate-600 mb-6 leading-relaxed">
          You are authenticated as a <strong>Student</strong>. The Administrator Dashboard and its management APIs require verified <strong>Admin</strong> privileges.
        </p>
        <button
          onClick={onReturnToDashboard}
          className="w-full inline-flex items-center justify-center gap-2 px-4 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold rounded-xl shadow-xs transition-colors cursor-pointer"
        >
          <ArrowLeft className="w-4 h-4" />
          Return to Student Dashboard
        </button>
      </div>
    </div>
  );
};
