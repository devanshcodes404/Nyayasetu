import React, { useState } from 'react';
import { apiClient } from '../lib/api-client';
import { Search, Sparkles, Send, Shield } from 'lucide-react';

export const ResearchPage: React.FC = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<any | null>(null);

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const res = await apiClient.post('/research/ask', {
        query: query.trim(),
        scope: 'all',
      });
      setResponse(res);
    } catch (err: any) {
      alert(err.message || 'Failed to submit query');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20 text-[10px] font-bold uppercase tracking-wider mb-2">
          <Sparkles className="w-3 h-3" />
          <span>Part 2 AI Integration Module</span>
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-white">AI Legal Research & RAG</h1>
        <p className="text-xs text-slate-400 mt-1">
          Query Indian legal provisions, constitutional issues, and court precedents across both the public corpus and private briefs.
        </p>
      </div>

      {/* Query Bar */}
      <form onSubmit={handleAsk} className="p-4 rounded-2xl bg-slate-900 border border-slate-800 space-y-3">
        <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
          Legal Research Question
        </label>
        <div className="flex gap-2">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g. What are the constitutional limitations on the Governor's power under Article 163 to call a floor test?"
              className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-10 pr-4 py-3 text-xs text-slate-200 placeholder:text-slate-600 focus:outline-none focus:border-amber-500"
            />
          </div>
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="px-6 py-3 bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-semibold rounded-lg flex items-center gap-2 transition-colors disabled:opacity-50"
          >
            <span>{loading ? 'Synthesizing...' : 'Ask AI'}</span>
            <Send className="w-3.5 h-3.5" />
          </button>
        </div>
      </form>

      {/* Part 2 Structured Response / Empty State */}
      {response ? (
        <div className="p-6 rounded-2xl bg-slate-900 border border-amber-500/30 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <span className="text-xs font-mono font-bold text-amber-400 uppercase">
              Status: {response.status}
            </span>
            <span className="text-xs text-slate-400 font-mono">Provider: {response.provider}</span>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-300 leading-relaxed">
            {response.message}
          </div>

          <div className="text-[11px] text-slate-500 flex items-center gap-2">
            <Shield className="w-3.5 h-3.5 text-amber-400" />
            <span>Retrieval Scope: {response.scope_used} (Public corpus & private briefs separation preserved)</span>
          </div>
        </div>
      ) : (
        <div className="p-8 rounded-2xl bg-slate-900/40 border border-dashed border-slate-800 text-center space-y-3">
          <Sparkles className="w-10 h-10 text-amber-400/40 mx-auto" />
          <h3 className="text-sm font-semibold text-slate-300">Legal RAG Foundation Ready</h3>
          <p className="text-xs text-slate-500 max-w-md mx-auto leading-relaxed">
            Part 1 establishes the multi-document retrieval contracts and scoped authorization. Part 2 will activate vector embeddings (pgvector) and LLM answer generation with verified pin-point citations.
          </p>
        </div>
      )}
    </div>
  );
};
