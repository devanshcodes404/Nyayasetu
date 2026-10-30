import React, { useEffect, useState } from 'react';
import { apiClient } from '../lib/api-client';
import { TrendingUp, AlertCircle, BarChart3 } from 'lucide-react';

export const InsightsPage: React.FC = () => {
  const [data, setData] = useState<any | null>(null);
  const [court, setCourt] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    let endpoint = '/analytics/outcomes';
    if (court) endpoint += `?court=${encodeURIComponent(court)}`;

    apiClient
      .get<any>(endpoint)
      .then((res) => setData(res))
      .catch((err) => console.error('Failed to load outcome analytics', err))
      .finally(() => setLoading(false));
  }, [court]);

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20 text-[10px] font-bold uppercase tracking-wider mb-2">
          <TrendingUp className="w-3 h-3" />
          <span>Case Outcome Analytics</span>
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-white">Historical Outcome Insights</h1>
        <p className="text-xs text-slate-400 mt-1">
          Aggregated distribution of historical judicial dispositions across Indian courts.
        </p>
      </div>

      {/* Mandatory Statutory Disclaimer Card */}
      <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs flex items-start gap-3">
        <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
        <div>
          <span className="font-bold block">Legal Integrity & Risk Disclaimer</span>
          <p className="mt-0.5 text-amber-200/90 leading-relaxed">
            Historical disposition distributions reflect statistical aggregates from imported public judgments. They do NOT calculate win probabilities, assess individual case merits, or guarantee future judicial outcomes. NyayaSetu AI is an assistance platform and not a substitute for professional legal evaluation.
          </p>
        </div>
      </div>

      {/* Filter */}
      <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-between">
        <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
          Filter by Court Hierarchy
        </span>
        <select
          value={court}
          onChange={(e) => setCourt(e.target.value)}
          aria-label="Filter outcome analytics by court hierarchy"
          className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-amber-500"
        >
          <option value="">All Indian Courts</option>
          <option value="Supreme Court">Supreme Court of India</option>
          <option value="Delhi">High Court of Delhi</option>
          <option value="Bombay">High Court of Bombay</option>
        </select>
      </div>

      {/* Analytics Card */}
      {loading ? (
        <div className="py-20 flex justify-center items-center">
          <div className="w-8 h-8 border-4 border-amber-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : data ? (
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-6">
          <div className="flex items-center justify-between pb-4 border-b border-slate-800">
            <div>
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                Corpus Records Analyzed
              </span>
              <div className="text-2xl font-bold text-white mt-1">{data.total_analyzed}</div>
            </div>
            <div className="p-2.5 rounded-lg bg-amber-500/10 text-amber-400 border border-amber-500/20">
              <BarChart3 className="w-5 h-5" />
            </div>
          </div>

          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 mb-3">
              Normalized Disposition Breakdown
            </h3>

            {Object.keys(data.disposition_distribution || {}).length > 0 ? (
              <div className="space-y-3">
                {Object.entries(data.disposition_distribution).map(([outcome, count]: [string, any]) => {
                  const pct = data.total_analyzed > 0 ? Math.round((count / data.total_analyzed) * 100) : 0;
                  return (
                    <div key={outcome} className="space-y-1">
                      <div className="flex justify-between text-xs font-semibold text-slate-300">
                        <span>{outcome}</span>
                        <span>{count} ({pct}%)</span>
                      </div>
                      <div className="w-full h-2 rounded-full bg-slate-950 overflow-hidden border border-slate-800">
                        <div
                          className="h-full bg-amber-500 rounded-full"
                          style={{ width: `${pct}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <p className="text-xs text-slate-500 py-4 text-center">
                No normalized outcomes recorded for this court filter yet.
              </p>
            )}
          </div>
        </div>
      ) : null}
    </div>
  );
};
