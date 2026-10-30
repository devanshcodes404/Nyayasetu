import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { apiClient } from '../lib/api-client';
import { JudgmentListItem, PaginatedResult } from '../types/api';
import { formatDate } from '../lib/utils';
import {
  BookOpen,
  Search,
  Filter,
  ExternalLink,
  ChevronLeft,
  ChevronRight,
  Database,
} from 'lucide-react';

export const JudgmentsPage: React.FC = () => {
  const [data, setData] = useState<PaginatedResult<JudgmentListItem> | null>(null);
  const [query, setQuery] = useState('');
  const [courtFilter, setCourtFilter] = useState('');
  const [yearFilter, setYearFilter] = useState('');
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);

  const fetchJudgments = async (targetPage: number = 1) => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      params.append('page', targetPage.toString());
      params.append('page_size', '15');
      if (query.trim()) params.append('q', query.trim());
      if (courtFilter) params.append('court', courtFilter);
      if (yearFilter) params.append('year', yearFilter);

      const res = await apiClient.get<PaginatedResult<JudgmentListItem>>(
        `/judgments/search?${params.toString()}`
      );
      setData(res);
      setPage(targetPage);
    } catch (err) {
      console.error('Failed to load judgments', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJudgments(1);
  }, [courtFilter, yearFilter]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchJudgments(1);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20 text-[10px] font-bold uppercase tracking-wider mb-2">
            <Database className="w-3 h-3" />
            <span>Public Indian Case-Law Corpus</span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-white">Judgments & Precedents</h1>
          <p className="text-xs text-slate-400 mt-1">
            Database-backed search over official Supreme Court and High Court judgments from Hugging Face dataset.
          </p>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
        <form onSubmit={handleSearch} className="flex gap-2">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search by keywords, parties, neutral citation (e.g. 2023 INSC 512), or CNR..."
              className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-10 pr-4 py-2.5 text-xs text-slate-200 placeholder:text-slate-600 focus:outline-none focus:border-amber-500"
            />
          </div>
          <button
            type="submit"
            className="px-5 py-2.5 bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-semibold rounded-lg transition-colors"
          >
            Search
          </button>
        </form>

        <div className="flex flex-wrap items-center gap-3 pt-2 border-t border-slate-800/80">
          <div className="flex items-center gap-2">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <span className="text-[11px] text-slate-400 font-semibold uppercase">Filters:</span>
          </div>

          <select
            value={courtFilter}
            onChange={(e) => setCourtFilter(e.target.value)}
            aria-label="Filter judgments by court"
            className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-amber-500"
          >
            <option value="">All Courts</option>
            <option value="Supreme Court">Supreme Court of India</option>
            <option value="Delhi">High Court of Delhi</option>
            <option value="Bombay">High Court of Bombay</option>
          </select>

          <input
            type="number"
            value={yearFilter}
            onChange={(e) => setYearFilter(e.target.value)}
            placeholder="Year (e.g. 2023)"
            className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 w-28 focus:outline-none focus:border-amber-500"
          />

          {(query || courtFilter || yearFilter) && (
            <button
              onClick={() => {
                setQuery('');
                setCourtFilter('');
                setYearFilter('');
              }}
              className="text-xs text-rose-400 hover:underline ml-auto"
            >
              Reset Filters
            </button>
          )}
        </div>
      </div>

      {/* Results Section */}
      {loading ? (
        <div className="py-20 flex justify-center items-center">
          <div className="w-8 h-8 border-4 border-amber-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : data && data.items.length > 0 ? (
        <div className="space-y-4">
          <div className="flex items-center justify-between text-xs text-slate-400 px-1">
            <span>Showing {data.items.length} of {data.total} judgments</span>
            <span>Page {data.page} of {data.total_pages}</span>
          </div>

          <div className="space-y-3">
            {data.items.map((j) => (
              <div
                key={j.id}
                className="p-5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition-colors space-y-3"
              >
                <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-2">
                  <div>
                    <Link
                      to={`/judgments/${j.id}`}
                      className="font-bold text-sm text-slate-100 hover:text-amber-400 transition-colors block"
                    >
                      {j.title}
                    </Link>
                    <div className="flex flex-wrap items-center gap-2 text-xs text-slate-400 mt-1">
                      <span className="text-slate-300 font-semibold">{j.court_name}</span>
                      {j.decision_date && (
                        <>
                          <span>•</span>
                          <span>{formatDate(j.decision_date)}</span>
                        </>
                      )}
                      {j.neutral_citation && (
                        <>
                          <span>•</span>
                          <span className="font-mono text-amber-400">{j.neutral_citation}</span>
                        </>
                      )}
                    </div>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded-full font-medium border ${
                        j.text_availability_status === 'FullText'
                          ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                          : j.text_availability_status === 'HeadnoteOnly'
                          ? 'bg-blue-500/10 text-blue-400 border-blue-500/20'
                          : 'bg-slate-800 text-slate-400 border-slate-700'
                      }`}
                    >
                      {j.text_availability_status}
                    </span>

                    {j.normalized_outcome && (
                      <span className="text-[10px] px-2 py-0.5 rounded bg-slate-950 text-slate-300 border border-slate-800">
                        {j.normalized_outcome}
                      </span>
                    )}
                  </div>
                </div>

                {/* Headnote Snippet if available */}
                {j.headnote_snippet && (
                  <p className="text-xs text-slate-400 bg-slate-950/60 p-3 rounded-lg border border-slate-800/80 leading-relaxed italic">
                    "{j.headnote_snippet}"
                  </p>
                )}

                <div className="flex items-center justify-between pt-1 text-[11px] text-slate-500">
                  <div className="flex items-center gap-4">
                    {j.docket_number && <span>Docket: {j.docket_number}</span>}
                    {j.cnr_number && <span>CNR: {j.cnr_number}</span>}
                  </div>
                  <Link
                    to={`/judgments/${j.id}`}
                    className="text-amber-400 hover:text-amber-300 font-semibold flex items-center gap-1"
                  >
                    <span>Read Full Details</span>
                    <ExternalLink className="w-3 h-3" />
                  </Link>
                </div>
              </div>
            ))}
          </div>

          {/* Pagination Controls */}
          {data.total_pages > 1 && (
            <div className="flex items-center justify-center gap-2 pt-4">
              <button
                onClick={() => fetchJudgments(page - 1)}
                disabled={!data.has_prev}
                className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs font-semibold text-slate-300 disabled:opacity-30 disabled:pointer-events-none hover:bg-slate-800"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <span className="text-xs text-slate-400 px-3">
                {page} / {data.total_pages}
              </span>
              <button
                onClick={() => fetchJudgments(page + 1)}
                disabled={!data.has_next}
                className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs font-semibold text-slate-300 disabled:opacity-30 disabled:pointer-events-none hover:bg-slate-800"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
      ) : (
        <div className="text-center py-20 border border-dashed border-slate-800 rounded-xl bg-slate-900/40">
          <BookOpen className="w-10 h-10 text-slate-600 mx-auto mb-3" />
          <h3 className="text-sm font-semibold text-slate-300">No judgments found</h3>
          <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
            Try adjusting your search keywords or import more records via the CLI import tool.
          </p>
        </div>
      )}
    </div>
  );
};
