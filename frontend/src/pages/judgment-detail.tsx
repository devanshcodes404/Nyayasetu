import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { apiClient } from '../lib/api-client';
import { JudgmentDetail } from '../types/api';
import { formatDate } from '../lib/utils';
import {
  ArrowLeft,
  Scale,
  ExternalLink,
  Sparkles,
} from 'lucide-react';

export const JudgmentDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [judgment, setJudgment] = useState<JudgmentDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    apiClient
      .get<JudgmentDetail>(`/judgments/${id}`)
      .then((data) => setJudgment(data))
      .catch((err) => {
        console.error('Failed to load judgment detail', err);
        navigate('/judgments');
      })
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return (
      <div className="py-20 flex justify-center items-center">
        <div className="w-8 h-8 border-4 border-amber-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!judgment) return null;

  return (
    <div className="space-y-6">
      <button
        onClick={() => navigate('/judgments')}
        className="inline-flex items-center gap-2 text-xs font-semibold text-slate-400 hover:text-slate-200 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Judgments Corpus</span>
      </button>

      {/* Main Header */}
      <div className="p-6 md:p-8 rounded-2xl bg-slate-900 border border-slate-800 space-y-6">
        <div className="space-y-2">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs px-2.5 py-1 rounded bg-amber-500/10 text-amber-400 font-mono font-bold border border-amber-500/20">
              {judgment.court_name}
            </span>
            {judgment.neutral_citation && (
              <span className="text-xs px-2.5 py-1 rounded bg-slate-800 text-slate-300 font-mono border border-slate-700">
                {judgment.neutral_citation}
              </span>
            )}
            <span className="text-xs px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium">
              Text: {judgment.text_availability_status}
            </span>
          </div>

          <h1 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">
            {judgment.title}
          </h1>

          <div className="flex flex-wrap items-center gap-4 text-xs text-slate-400 pt-1">
            {judgment.decision_date && <span>Decided: {formatDate(judgment.decision_date)}</span>}
            {judgment.bench_name && <span>Bench: {judgment.bench_name}</span>}
            {judgment.presiding_judge && <span>Presiding: {judgment.presiding_judge}</span>}
          </div>
        </div>

        {/* Parties & Bench Information */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 rounded-xl bg-slate-950 border border-slate-800/80 text-xs">
          <div>
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Petitioner</span>
            <span className="text-slate-200 font-medium mt-0.5 block">{judgment.petitioner || '—'}</span>
          </div>
          <div>
            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Respondent</span>
            <span className="text-slate-200 font-medium mt-0.5 block">{judgment.respondent || '—'}</span>
          </div>
          {judgment.coram_members_text && (
            <div className="md:col-span-2 pt-2 border-t border-slate-800/80">
              <span className="text-[10px] text-slate-500 uppercase font-semibold block">Coram Members</span>
              <span className="text-slate-300 font-medium mt-0.5 block">{judgment.coram_members_text}</span>
            </div>
          )}
        </div>

        {/* Disposition / Decision */}
        {judgment.disposition_text && (
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">
              Court Disposition & Holding
            </h3>
            <p className="text-xs text-slate-200 leading-relaxed font-medium">
              {judgment.disposition_text}
            </p>
          </div>
        )}

        {/* Headnote Text */}
        {judgment.headnote_text && (
          <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2">
            <h3 className="text-xs font-bold uppercase tracking-wider text-amber-400 flex items-center gap-2">
              <Scale className="w-3.5 h-3.5" />
              <span>Official Headnote / Syllabus</span>
            </h3>
            <p className="text-xs text-slate-300 leading-relaxed whitespace-pre-line font-serif">
              {judgment.headnote_text}
            </p>
          </div>
        )}

        {/* Indexable Text / Full Judgment */}
        {judgment.indexable_text ? (
          <div className="space-y-3 pt-4 border-t border-slate-800">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">
              Indexable Judgment Content
            </h3>
            <div className="p-5 rounded-xl bg-slate-950 border border-slate-800 max-h-96 overflow-y-auto text-xs text-slate-300 leading-relaxed font-mono whitespace-pre-wrap">
              {judgment.indexable_text}
            </div>
          </div>
        ) : (
          <div className="p-4 rounded-xl bg-slate-950/40 border border-slate-800 text-xs text-slate-500 text-center">
            Detailed judgment text is not populated in this sample record.
          </div>
        )}

        {/* Provenance Metadata Footer */}
        <div className="pt-4 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-3 text-[11px] text-slate-500">
          <div>
            <span>Dataset Provenance: </span>
            <span className="text-slate-400 font-mono">{judgment.source_dataset}</span>
            {judgment.external_id && <span> ({judgment.external_id})</span>}
          </div>

          {judgment.source_pdf_s3_url && (
            <a
              href={judgment.source_pdf_s3_url}
              target="_blank"
              rel="noreferrer"
              className="text-amber-400 hover:underline flex items-center gap-1 font-semibold"
            >
              <span>View Source PDF</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          )}
        </div>
      </div>

      {/* Part 2 AI Summary Module Interface Banner */}
      <div className="p-6 rounded-2xl bg-slate-900/40 border border-amber-500/20 flex items-start gap-4">
        <div className="p-2.5 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20 shrink-0">
          <Sparkles className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-sm font-bold text-white">AI Judgment Summarization Engine (PART 2)</h3>
          <p className="text-xs text-slate-400 mt-1 leading-relaxed">
            Automatic multi-issue extraction, held reasoning synthesis, and cross-citation hyperlinking for this judgment will be activated in Part 2 via the backend summarizer service.
          </p>
        </div>
      </div>
    </div>
  );
};
