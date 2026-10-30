import React from 'react';
import { Quote, Sparkles } from 'lucide-react';

export const CitationsPage: React.FC = () => {
  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20 text-[10px] font-bold uppercase tracking-wider mb-2">
          <Quote className="w-3 h-3" />
          <span>Citation Verification Engine</span>
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-white">Legal Citations & Authorities</h1>
        <p className="text-xs text-slate-400 mt-1">
          Automated extraction and graph linking of AIR, SCC, SCR, and Neutral citations across petitions and judgments.
        </p>
      </div>

      <div className="p-8 rounded-2xl bg-slate-900 border border-slate-800 space-y-6 text-center">
        <div className="w-12 h-12 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20 flex items-center justify-center mx-auto">
          <Sparkles className="w-6 h-6" />
        </div>

        <div className="max-w-md mx-auto space-y-2">
          <h2 className="text-base font-bold text-white">Citation Resolution Graph Ready (PART 2)</h2>
          <p className="text-xs text-slate-400 leading-relaxed">
            The citation extraction regex models and database entity <code className="text-amber-400 font-mono text-[11px]">LegalCitation</code> have been established in the backend. Full automated authority resolution against the 17.1M judgment corpus is scheduled for PART 2.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-left max-w-lg mx-auto pt-4 border-t border-slate-800">
          <div className="p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs">
            <span className="font-semibold text-slate-200 block mb-1">Supported Citation Formats:</span>
            <span className="text-[11px] text-slate-400 font-mono block">• AIR (All India Reporter)</span>
            <span className="text-[11px] text-slate-400 font-mono block">• SCC (Supreme Court Cases)</span>
            <span className="text-[11px] text-slate-400 font-mono block">• Indian Neutral Citations (INSC)</span>
          </div>

          <div className="p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs">
            <span className="font-semibold text-slate-200 block mb-1">Verification Statuses:</span>
            <span className="text-[11px] text-emerald-400 block">• Verified Authority</span>
            <span className="text-[11px] text-amber-400 block">• Ambiguous Reporter</span>
            <span className="text-[11px] text-slate-500 block">• Unindexed Precedent</span>
          </div>
        </div>
      </div>
    </div>
  );
};
