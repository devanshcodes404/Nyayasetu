import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { apiClient } from '../lib/api-client';
import { LegalCase } from '../types/api';
import { formatDate } from '../lib/utils';
import { Briefcase, Plus, Search, Filter, Calendar, FileText, ChevronRight } from 'lucide-react';

export const CasesPage: React.FC = () => {
  const [cases, setCases] = useState<LegalCase[]>([]);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchCases = async () => {
    setLoading(true);
    try {
      let endpoint = '/cases';
      const params = new URLSearchParams();
      if (statusFilter) params.append('status', statusFilter);
      if (search) params.append('q', search);
      if (params.toString()) endpoint += `?${params.toString()}`;

      const data = await apiClient.get<LegalCase[]>(endpoint);
      setCases(data);
    } catch (err) {
      console.error('Failed to load cases', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCases();
  }, [statusFilter]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchCases();
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white">My Court Cases</h1>
          <p className="text-xs text-slate-400 mt-1">
            Manage your legal briefs, hearing schedules, and client case files.
          </p>
        </div>

        <Link
          to="/cases/new"
          className="inline-flex items-center gap-2 px-4 py-2.5 bg-amber-500 hover:bg-amber-400 text-slate-950 font-semibold text-xs rounded-lg transition-colors shadow-lg shadow-amber-500/10"
        >
          <Plus className="w-4 h-4" />
          <span>New Case Brief</span>
        </Link>
      </div>

      {/* Filter and Search Bar */}
      <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 flex flex-col md:flex-row gap-4 items-center justify-between">
        <form onSubmit={handleSearchSubmit} className="relative w-full md:max-w-md">
          <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by title, case number, court, or client..."
            className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-10 pr-4 py-2 text-xs text-slate-200 placeholder:text-slate-600 focus:outline-none focus:border-amber-500"
          />
        </form>

        <div className="flex items-center gap-3 w-full md:w-auto">
          <Filter className="w-4 h-4 text-slate-400" />
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            aria-label="Filter cases by status"
            className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-amber-500"
          >
            <option value="">All Statuses</option>
            <option value="Active">Active</option>
            <option value="Pending">Pending</option>
            <option value="Disposed">Disposed</option>
            <option value="Appeal">Appeal</option>
          </select>
        </div>
      </div>

      {/* Cases List Table / Cards */}
      {loading ? (
        <div className="py-20 flex justify-center items-center">
          <div className="w-8 h-8 border-4 border-amber-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : cases.length > 0 ? (
        <div className="rounded-xl border border-slate-800 overflow-hidden bg-slate-900">
          <div className="divide-y divide-slate-800">
            {cases.map((c) => (
              <Link
                key={c.id}
                to={`/cases/${c.id}`}
                className="p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:bg-slate-800/40 transition-colors block"
              >
                <div className="min-w-0 space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-sm text-slate-100 hover:text-amber-400">
                      {c.title}
                    </span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
                      {c.case_number}
                    </span>
                  </div>
                  <div className="text-xs text-slate-400 flex flex-wrap items-center gap-3">
                    <span>{c.court}</span>
                    <span>•</span>
                    <span>Client: <span className="text-slate-300">{c.client_name}</span></span>
                    <span>•</span>
                    <span>Opponent: <span className="text-slate-300">{c.opposing_party}</span></span>
                  </div>
                </div>

                <div className="flex items-center gap-4 shrink-0">
                  {c.next_hearing_date && (
                    <div className="flex items-center gap-1.5 text-xs text-amber-400 bg-amber-500/10 px-2.5 py-1 rounded-md border border-amber-500/20">
                      <Calendar className="w-3.5 h-3.5" />
                      <span>{formatDate(c.next_hearing_date)}</span>
                    </div>
                  )}
                  <span className="text-xs px-2.5 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-medium">
                    {c.status}
                  </span>
                  <div className="flex items-center gap-1 text-xs text-slate-500">
                    <FileText className="w-3.5 h-3.5" />
                    <span>{c.documents_count ?? 0}</span>
                  </div>
                  <ChevronRight className="w-4 h-4 text-slate-600" />
                </div>
              </Link>
            ))}
          </div>
        </div>
      ) : (
        <div className="text-center py-20 border border-dashed border-slate-800 rounded-xl bg-slate-900/40">
          <Briefcase className="w-10 h-10 text-slate-600 mx-auto mb-3" />
          <h3 className="text-sm font-semibold text-slate-300">No cases found</h3>
          <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
            Get started by adding your first active brief or adjusting search parameters.
          </p>
        </div>
      )}
    </div>
  );
};

