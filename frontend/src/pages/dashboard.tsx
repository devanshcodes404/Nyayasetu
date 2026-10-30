import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { apiClient } from '../lib/api-client';
import { DashboardMetrics } from '../types/api';
import { formatDate } from '../lib/utils';
import {
  Briefcase,
  FileText,
  Calendar,
  BookOpen,
  Plus,
  Upload,
  Search,
  ArrowUpRight,
} from 'lucide-react';

export const DashboardPage: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient
      .get<DashboardMetrics>('/analytics/dashboard')
      .then((data) => setMetrics(data))
      .catch((err) => console.error('Failed to load dashboard metrics', err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-8">
      {/* Top Banner / Actions */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white">Legal Dashboard</h1>
          <p className="text-xs text-slate-400 mt-1">
            Real-time court brief status, upcoming hearings, and Indian case-law corpus metrics.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Link
            to="/cases/new"
            className="flex items-center gap-2 px-3.5 py-2 bg-amber-500 hover:bg-amber-400 text-slate-950 font-semibold text-xs rounded-lg transition-colors shadow-md shadow-amber-500/10"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>New Case Brief</span>
          </Link>
          <Link
            to="/documents"
            className="flex items-center gap-2 px-3.5 py-2 bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 font-semibold text-xs rounded-lg transition-colors"
          >
            <Upload className="w-3.5 h-3.5 text-amber-400" />
            <span>Upload Document</span>
          </Link>
          <Link
            to="/judgments"
            className="flex items-center gap-2 px-3.5 py-2 bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 font-semibold text-xs rounded-lg transition-colors"
          >
            <Search className="w-3.5 h-3.5 text-amber-400" />
            <span>Search Corpus</span>
          </Link>
        </div>
      </div>

      {/* Metrics Row: Distinguishing Private Workspace vs Public Corpus */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Private Metric 1 */}
        <div className="p-5 rounded-xl bg-slate-900 border border-slate-800 relative overflow-hidden">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Active Briefs
            </span>
            <div className="p-2 rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/20">
              <Briefcase className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-white">
            {loading ? '—' : metrics?.my_active_cases ?? 0}
          </div>
          <span className="text-[11px] text-slate-500 mt-1 block">Private workspace cases</span>
        </div>

        {/* Private Metric 2 */}
        <div className="p-5 rounded-xl bg-slate-900 border border-slate-800 relative overflow-hidden">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Upcoming Hearings
            </span>
            <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400 border border-amber-500/20">
              <Calendar className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-white">
            {loading ? '—' : metrics?.my_upcoming_hearings_count ?? 0}
          </div>
          <span className="text-[11px] text-slate-500 mt-1 block">Scheduled on court calendar</span>
        </div>

        {/* Private Metric 3 */}
        <div className="p-5 rounded-xl bg-slate-900 border border-slate-800 relative overflow-hidden">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Stored Documents
            </span>
            <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <FileText className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-white">
            {loading ? '—' : metrics?.my_total_documents ?? 0}
          </div>
          <span className="text-[11px] text-slate-500 mt-1 block">Parsed & encrypted files</span>
        </div>

        {/* Public Corpus Metric */}
        <div className="p-5 rounded-xl bg-slate-900 border border-amber-500/30 relative overflow-hidden">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold uppercase tracking-wider text-amber-400">
              Public Judgments
            </span>
            <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400 border border-amber-500/20">
              <BookOpen className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-white">
            {loading ? '—' : metrics?.public_judgments_imported ?? 0}
          </div>
          <span className="text-[11px] text-amber-400/80 mt-1 block">
            {metrics?.public_courts_count ?? 0} courts indexed (Sumitedu)
          </span>
        </div>
      </div>

      {/* Main Grid: Recent Cases & Upcoming Hearings */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Recent Cases */}
        <div className="lg:col-span-2 p-6 rounded-xl bg-slate-900 border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-bold text-white uppercase tracking-wider">
              Recent Case Briefs
            </h2>
            <Link
              to="/cases"
              className="text-xs font-semibold text-amber-400 hover:text-amber-300 flex items-center gap-1"
            >
              <span>View All</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {metrics?.recent_cases && metrics.recent_cases.length > 0 ? (
            <div className="divide-y divide-slate-800/80">
              {metrics.recent_cases.map((c) => (
                <div key={c.id} className="py-3.5 flex items-center justify-between gap-4">
                  <div className="min-w-0">
                    <Link
                      to={`/cases/${c.id}`}
                      className="font-semibold text-sm text-slate-200 hover:text-amber-400 truncate block transition-colors"
                    >
                      {c.title}
                    </Link>
                    <div className="flex items-center gap-2 text-xs text-slate-400 mt-0.5">
                      <span className="font-mono text-slate-300">{c.case_number}</span>
                      <span>•</span>
                      <span>{c.court}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-3 shrink-0">
                    <span className="text-[11px] px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-medium">
                      {c.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-10 text-slate-500 text-xs">
              No active briefs found. Click "New Case Brief" to create one.
            </div>
          )}
        </div>

        {/* Upcoming Hearings */}
        <div className="p-6 rounded-xl bg-slate-900 border border-slate-800">
          <h2 className="text-sm font-bold text-white uppercase tracking-wider mb-4">
            Hearing Schedule
          </h2>

          {metrics?.upcoming_hearings && metrics.upcoming_hearings.length > 0 ? (
            <div className="space-y-3">
              {metrics.upcoming_hearings.map((h, idx) => (
                <div
                  key={idx}
                  className="p-3 rounded-lg bg-slate-950 border border-slate-800/80 flex items-start gap-3"
                >
                  <div className="p-2 rounded-md bg-amber-500/10 text-amber-400 border border-amber-500/20 shrink-0 mt-0.5">
                    <Calendar className="w-3.5 h-3.5" />
                  </div>
                  <div className="min-w-0">
                    <Link
                      to={`/cases/${h.case_id}`}
                      className="text-xs font-semibold text-slate-200 hover:text-amber-400 truncate block transition-colors"
                    >
                      {h.title}
                    </Link>
                    <p className="text-[11px] text-slate-400 mt-0.5">{h.court}</p>
                    <span className="inline-block mt-1 text-[10px] font-mono text-amber-400 font-medium">
                      {formatDate(h.date)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-10 text-slate-500 text-xs">
              No scheduled hearings on your calendar.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
