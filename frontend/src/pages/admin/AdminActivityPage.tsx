import React, { useEffect, useState } from 'react';
import {
  History,
  Search,
  Filter,
  RefreshCw,
  ShieldCheck,
  UserCheck,
  UserX,
  BookOpen,
  Edit3,
  Clock,
  Layers,
  CheckCircle,
} from 'lucide-react';
import { adminApi } from '../../services/adminApi';
import type { AdminActivityItem } from '../../types/admin';

export const AdminActivityPage: React.FC = () => {
  const [logs, setLogs] = useState<AdminActivityItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters
  const [searchQuery, setSearchQuery] = useState('');
  const [actionFilter, setActionFilter] = useState('');
  const [targetTypeFilter, setTargetTypeFilter] = useState('');

  const fetchLogs = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await adminApi.getActivityLogs(100);
      setLogs(data);
    } catch (err: any) {
      console.error('Failed to load audit logs:', err);
      setError(err?.response?.data?.detail || 'Failed to load activity logs.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  const getActionBadge = (action: string) => {
    const act = action.toUpperCase();
    if (act.includes('LOGIN')) {
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
          <ShieldCheck className="w-3.5 h-3.5" />
          {action}
        </span>
      );
    }
    if (act.includes('DEACTIVATE') || act.includes('DELETE')) {
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-rose-50 text-rose-700 border border-rose-200">
          <UserX className="w-3.5 h-3.5" />
          {action}
        </span>
      );
    }
    if (act.includes('ACTIVATE')) {
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200">
          <UserCheck className="w-3.5 h-3.5" />
          {action}
        </span>
      );
    }
    if (act.includes('CREATE')) {
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-purple-50 text-purple-700 border border-purple-200">
          <BookOpen className="w-3.5 h-3.5" />
          {action}
        </span>
      );
    }
    if (act.includes('UPDATE') || act.includes('PROGRESS')) {
      return (
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-50 text-amber-700 border border-amber-200">
          <Edit3 className="w-3.5 h-3.5" />
          {action}
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-700 border border-slate-200">
        <Layers className="w-3.5 h-3.5" />
        {action}
      </span>
    );
  };

  const filteredLogs = logs.filter((item) => {
    if (actionFilter && !item.action.toUpperCase().includes(actionFilter.toUpperCase())) {
      return false;
    }
    if (targetTypeFilter && item.target_type !== targetTypeFilter) {
      return false;
    }
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      const matchAdmin =
        item.admin_name?.toLowerCase().includes(q) ||
        item.admin_email?.toLowerCase().includes(q) ||
        item.admin_id?.toLowerCase().includes(q);
      const matchAction = item.action.toLowerCase().includes(q);
      const matchTarget =
        item.target_id?.toLowerCase().includes(q) ||
        item.target_type?.toLowerCase().includes(q);
      const matchDetails = item.details?.toLowerCase().includes(q);
      if (!matchAdmin && !matchAction && !matchTarget && !matchDetails) {
        return false;
      }
    }
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2.5">
            <History className="w-7 h-7 text-indigo-600" />
            Audit & Activity Logs
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Immutable administrative audit trail recording logins, student state updates, course changes, and progress corrections.
          </p>
        </div>
        <button
          onClick={fetchLogs}
          disabled={loading}
          className="inline-flex items-center gap-2 px-3.5 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors shadow-sm self-start sm:self-auto"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          Refresh Stream
        </button>
      </div>

      {/* Error state */}
      {error && (
        <div className="p-4 bg-rose-50 border border-rose-200 rounded-xl text-sm text-rose-700 flex items-center gap-3">
          <span className="font-semibold">Error:</span> {error}
        </div>
      )}

      {/* Filter and Search Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200/80 shadow-sm flex flex-col md:flex-row items-center gap-3">
        <div className="relative flex-1 w-full">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            placeholder="Search by admin, action, target ID, details..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 text-sm border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600"
          />
        </div>

        <div className="flex flex-wrap items-center gap-2 w-full md:w-auto">
          <div className="relative min-w-[150px]">
            <Filter className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400" />
            <select
              value={actionFilter}
              onChange={(e) => setActionFilter(e.target.value)}
              className="w-full pl-8 pr-7 py-2 text-xs border border-slate-200 rounded-lg bg-white text-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600"
            >
              <option value="">All Action Types</option>
              <option value="LOGIN">Admin Login</option>
              <option value="STUDENT_ACTIVATE">Student Activated</option>
              <option value="STUDENT_DEACTIVATE">Student Deactivated</option>
              <option value="COURSE_CREATE">Course Created</option>
              <option value="COURSE_UPDATE">Course Updated</option>
              <option value="COURSE_STATUS_CHANGE">Course Status</option>
              <option value="PROGRESS_CORRECTION">Progress Correction</option>
            </select>
          </div>

          <div className="relative min-w-[130px]">
            <select
              value={targetTypeFilter}
              onChange={(e) => setTargetTypeFilter(e.target.value)}
              className="w-full px-3 py-2 text-xs border border-slate-200 rounded-lg bg-white text-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600"
            >
              <option value="">All Targets</option>
              <option value="USER">User</option>
              <option value="COURSE">Course</option>
              <option value="PROGRESS">Progress</option>
              <option value="AUTH">Auth</option>
            </select>
          </div>

          {(searchQuery || actionFilter || targetTypeFilter) && (
            <button
              onClick={() => {
                setSearchQuery('');
                setActionFilter('');
                setTargetTypeFilter('');
              }}
              className="px-3 py-2 text-xs text-indigo-600 hover:text-indigo-800 font-medium"
            >
              Clear
            </button>
          )}
        </div>
      </div>

      {/* Activity Table */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-sm overflow-hidden">
        {loading && logs.length === 0 ? (
          <div className="py-16 text-center">
            <RefreshCw className="w-8 h-8 text-indigo-600 animate-spin mx-auto mb-3" />
            <p className="text-sm text-slate-500 font-medium">Loading audit logs...</p>
          </div>
        ) : filteredLogs.length === 0 ? (
          <div className="py-16 px-4 text-center">
            <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center mx-auto mb-3 text-slate-400">
              <History className="w-6 h-6" />
            </div>
            <h3 className="text-base font-semibold text-slate-900 mb-1">
              No administrative activity yet.
            </h3>
            <p className="text-xs text-slate-500 max-w-sm mx-auto">
              {logs.length === 0
                ? 'System actions performed by administrators will be tracked here in real-time.'
                : 'No logs match your filter criteria. Try clearing search filters.'}
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-50/80 text-xs font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200">
                <tr>
                  <th className="px-5 py-3.5">Timestamp</th>
                  <th className="px-5 py-3.5">Action</th>
                  <th className="px-5 py-3.5">Admin Operator</th>
                  <th className="px-5 py-3.5">Target</th>
                  <th className="px-5 py-3.5">Event Details</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredLogs.map((log) => (
                  <tr key={log.log_id} className="hover:bg-slate-50/60 transition-colors">
                    <td className="px-5 py-4 whitespace-nowrap text-xs text-slate-500">
                      <div className="flex items-center gap-1.5 text-slate-700 font-mono">
                        <Clock className="w-3.5 h-3.5 text-slate-400" />
                        {new Date(log.timestamp).toLocaleString(undefined, {
                          month: 'short',
                          day: 'numeric',
                          year: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit',
                          second: '2-digit',
                        })}
                      </div>
                    </td>

                    <td className="px-5 py-4 whitespace-nowrap">
                      {getActionBadge(log.action)}
                    </td>

                    <td className="px-5 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-slate-900">
                        {log.admin_name || 'System Admin'}
                      </div>
                      <div className="text-xs text-slate-400 font-mono">
                        {log.admin_email || log.admin_id || 'Internal'}
                      </div>
                    </td>

                    <td className="px-5 py-4 whitespace-nowrap">
                      <div className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium bg-slate-100 text-slate-700">
                        {log.target_type || 'SYSTEM'}
                      </div>
                      {log.target_id && (
                        <div className="text-[11px] text-slate-400 font-mono mt-0.5 truncate max-w-[160px]" title={log.target_id}>
                          ID: {log.target_id}
                        </div>
                      )}
                    </td>

                    <td className="px-5 py-4 text-xs text-slate-600 max-w-md">
                      <div className="p-2 bg-slate-50 rounded border border-slate-100 font-mono text-[11px] break-words text-slate-700">
                        {log.details || 'No additional parameters.'}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <div className="px-5 py-3 bg-slate-50/50 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
          <span>Showing {filteredLogs.length} events</span>
          <span className="flex items-center gap-1 text-slate-400">
            <CheckCircle className="w-3.5 h-3.5 text-emerald-500" />
            Audit logging active & immutable
          </span>
        </div>
      </div>
    </div>
  );
};
