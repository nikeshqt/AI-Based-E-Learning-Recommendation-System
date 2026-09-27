import React from 'react';
import { Cpu, ShieldCheck } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="mt-8 pt-4 pb-2 border-t border-slate-200 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-2">
      <div className="flex items-center gap-2">
        <Cpu className="w-4 h-4 text-indigo-600" />
        <span>NeuralLearn E-Learning Engine • PostgreSQL Persistence</span>
      </div>
      <div className="flex items-center gap-4 text-[11px]">
        <span className="flex items-center gap-1 text-slate-500">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
          Secure Telemetry Logging
        </span>
        <span>FastAPI & RecSys Matrix</span>
      </div>
    </footer>
  );
};
