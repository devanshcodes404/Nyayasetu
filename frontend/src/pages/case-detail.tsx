import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { apiClient } from '../lib/api-client';
import { LegalCase, LegalDocument } from '../types/api';
import { formatDate } from '../lib/utils';
import {
  ArrowLeft,
  Calendar,
  FileText,
  Upload,
  Trash2,
  Sparkles,
} from 'lucide-react';

export const CaseDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [legalCase, setLegalCase] = useState<LegalCase | null>(null);
  const [documents, setDocuments] = useState<LegalDocument[]>([]);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    Promise.all([
      apiClient.get<LegalCase>(`/cases/${id}`),
      apiClient.get<LegalDocument[]>(`/documents?case_id=${id}`),
    ])
      .then(([caseData, docsData]) => {
        setLegalCase(caseData);
        setDocuments(docsData);
      })
      .catch((err) => {
        console.error('Failed to load case detail', err);
        navigate('/cases');
      })
      .finally(() => setLoading(false));
  }, [id]);

  const handleDelete = async () => {
    if (!id || !window.confirm('Are you sure you want to delete this case brief?')) return;
    setDeleting(true);
    try {
      await apiClient.delete(`/cases/${id}`);
      navigate('/cases');
    } catch (err) {
      alert('Failed to delete case.');
      setDeleting(false);
    }
  };

  if (loading) {
    return (
      <div className="py-20 flex justify-center items-center">
        <div className="w-8 h-8 border-4 border-amber-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!legalCase) return null;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <button
          onClick={() => navigate('/cases')}
          className="inline-flex items-center gap-2 text-xs font-semibold text-slate-400 hover:text-slate-200 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to My Cases</span>
        </button>

        <button
          onClick={handleDelete}
          disabled={deleting}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-rose-500/10 text-rose-400 hover:bg-rose-500/20 text-xs font-semibold border border-rose-500/20 transition-colors"
        >
          <Trash2 className="w-3.5 h-3.5" />
          <span>{deleting ? 'Deleting...' : 'Delete Brief'}</span>
        </button>
      </div>

      {/* Case Header Card */}
      <div className="p-6 md:p-8 rounded-2xl bg-slate-900 border border-slate-800 space-y-6">
        <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 font-bold">
                {legalCase.case_number}
              </span>
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-medium">
                {legalCase.status}
              </span>
            </div>
            <h1 className="text-2xl font-bold text-white tracking-tight">{legalCase.title}</h1>
            <p className="text-xs text-slate-400">{legalCase.court} • {legalCase.jurisdiction} Jurisdiction</p>
          </div>

          {legalCase.next_hearing_date && (
            <div className="p-3 rounded-xl bg-slate-950 border border-amber-500/30 flex items-center gap-3 shrink-0">
              <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400">
                <Calendar className="w-4 h-4" />
              </div>
              <div>
                <span className="text-[10px] uppercase tracking-wider text-slate-400 block font-semibold">
                  Next Hearing Date
                </span>
                <span className="text-xs font-bold text-amber-400">
                  {formatDate(legalCase.next_hearing_date)}
                </span>
              </div>
            </div>
          )}
        </div>

        {/* Parties Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 p-4 rounded-xl bg-slate-950 border border-slate-800/80">
          <div>
            <span className="text-[11px] text-slate-500 uppercase tracking-wider font-semibold block">
              Client Representation
            </span>
            <span className="text-sm font-semibold text-slate-200 mt-0.5 block">
              {legalCase.client_name}
            </span>
          </div>
          <div>
            <span className="text-[11px] text-slate-500 uppercase tracking-wider font-semibold block">
              Opposing Party
            </span>
            <span className="text-sm font-semibold text-slate-200 mt-0.5 block">
              {legalCase.opposing_party}
            </span>
          </div>
        </div>

        {/* Case Notes */}
        {legalCase.description && (
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
              Brief Overview & Statutory Grounds
            </h3>
            <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/50 p-4 rounded-xl border border-slate-800">
              {legalCase.description}
            </p>
          </div>
        )}
      </div>

      {/* Associated Documents */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <FileText className="w-4 h-4 text-amber-400" />
            <h2 className="text-sm font-bold text-white uppercase tracking-wider">
              Case Brief Documents ({documents.length})
            </h2>
          </div>
          <Link
            to="/documents"
            className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg border border-slate-700 transition-colors"
          >
            <Upload className="w-3.5 h-3.5 text-amber-400" />
            <span>Upload Document</span>
          </Link>
        </div>

        {documents.length > 0 ? (
          <div className="divide-y divide-slate-800 border border-slate-800 rounded-xl overflow-hidden bg-slate-950">
            {documents.map((doc) => (
              <div key={doc.id} className="p-4 flex items-center justify-between gap-4">
                <div className="min-w-0">
                  <span className="text-xs font-semibold text-slate-200 block truncate">
                    {doc.title}
                  </span>
                  <span className="text-[10px] text-slate-500 font-mono mt-0.5 block">
                    {doc.original_filename} • {doc.page_count ?? 1} pages • Status: {doc.processing_status}
                  </span>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    {doc.text_availability_status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-500 py-6 text-center">
            No documents linked to this case brief yet.
          </p>
        )}
      </div>

      {/* Part 2 AI Precedent Insights Placeholder Card */}
      <div className="p-6 rounded-2xl bg-slate-900/40 border border-amber-500/20 flex items-start gap-4">
        <div className="p-2.5 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20 shrink-0">
          <Sparkles className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-sm font-bold text-white">Precedent Matching & Similar Case Analysis (PART 2)</h3>
          <p className="text-xs text-slate-400 mt-1 leading-relaxed">
            NyayaSetu AI will cross-reference this case's statutory provisions and court jurisdiction against the 17.1M Indian case-law dataset using pgvector embeddings and LLM reranking in Part 2.
          </p>
        </div>
      </div>
    </div>
  );
};
