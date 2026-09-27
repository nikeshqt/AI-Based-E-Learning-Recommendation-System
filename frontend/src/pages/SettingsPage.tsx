import React from 'react';
import { Settings, Sliders, Database, Shield } from 'lucide-react';

export const SettingsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs">
        <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
          <Settings className="w-5 h-5 text-slate-500" />
          Profile & System Settings
        </h2>
        <p className="text-xs text-slate-600 mt-1">
          Configure your career goal, skill preferences, and API configuration.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white border border-slate-200 rounded-xl p-5 space-y-4 shadow-xs">
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <Sliders className="w-4 h-4 text-indigo-600" />
            Learner Profile Preferences
          </h3>
          <div className="space-y-3 text-xs">
            <div>
              <label className="text-slate-600 block mb-1 font-medium">Target Career Goal</label>
              <input
                type="text"
                defaultValue="Cybersecurity Analyst"
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 text-xs focus:outline-none focus:border-indigo-500"
              />
            </div>
            <div>
              <label className="text-slate-600 block mb-1 font-medium">Preferred Learning Format</label>
              <select className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 text-xs focus:outline-none focus:border-indigo-500">
                <option value="practical">Practical / Hands-on Labs</option>
                <option value="visual">Video Lectures & Demos</option>
                <option value="reading">Text & Documentation</option>
              </select>
            </div>
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-xl p-5 space-y-4 shadow-xs">
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <Database className="w-4 h-4 text-indigo-600" />
            Database & API Connection
          </h3>
          <div className="space-y-3 text-xs text-slate-700">
            <div>
              <label className="text-slate-600 block mb-1 font-medium">FastAPI Backend Endpoint</label>
              <input
                type="text"
                defaultValue="http://127.0.0.1:8080/api/v1"
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 font-mono text-[11px]"
              />
            </div>
            <div className="flex items-center gap-2 pt-2 text-slate-600">
              <Shield className="w-4 h-4 text-emerald-600" />
              <span>PostgreSQL Persistent Database Connected</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
