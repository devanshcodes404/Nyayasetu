import React, { useEffect, useState } from 'react';
import { apiClient } from '../lib/api-client';
import { LegalDocument, LegalCase } from '../types/api';
import { formatFileSize, formatDate } from '../lib/utils';
import {
  FileText,
  Upload,
  Trash2,
  AlertCircle,
  CheckCircle2,
} from 'lucide-react';

export const DocumentsPage: React.FC = () => {
  const [documents, setDocuments] = useState<LegalDocument[]>([]);
  const [cases, setCases] = useState<LegalCase[]>([]);
  const [loading, setLoading] = useState(true);

  // Upload Form State
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [docTitle, setDocTitle] = useState('');
  const [selectedCaseId, setSelectedCaseId] = useState<string>('');
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [docsData, casesData] = await Promise.all([
        apiClient.get<LegalDocument[]>('/documents'),
        apiClient.get<LegalCase[]>('/cases'),
      ]);
      setDocuments(docsData);
      setCases(casesData);
    } catch (err) {
      console.error('Failed to load documents', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const f = e.target.files[0];
      setSelectedFile(f);
      if (!docTitle) {
        setDocTitle(f.name.replace(/\.[^/.]+$/, ''));
      }
    }
  };

  const handleUploadSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) {
      setUploadMessage({ type: 'error', text: 'Please select a document file to upload.' });
      return;
    }

    setUploading(true);
    setUploadMessage(null);

    const formData = new FormData();
    formData.append('file', selectedFile);
    if (docTitle) formData.append('title', docTitle);
    if (selectedCaseId) formData.append('case_id', selectedCaseId);

    try {
      await apiClient.post('/documents/upload', formData);
      setUploadMessage({ type: 'success', text: 'Document uploaded, parsed, and stored successfully!' });
      setSelectedFile(null);
      setDocTitle('');
      setSelectedCaseId('');
      fetchData();
    } catch (err: any) {
      setUploadMessage({ type: 'error', text: err.message || 'Document upload failed.' });
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (docId: number) => {
    if (!window.confirm('Are you sure you want to delete this document?')) return;
    try {
      await apiClient.delete(`/documents/${docId}`);
      fetchData();
    } catch (err) {
      alert('Failed to delete document.');
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white">Case Documents Vault</h1>
        <p className="text-xs text-slate-400 mt-1">
          Upload brief petitions, affidavits, and orders (PDF, DOCX, TXT) with automatic text extraction.
        </p>
      </div>

      {/* Upload Box */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4">
        <div className="flex items-center gap-2">
          <Upload className="w-4 h-4 text-amber-400" />
          <h2 className="text-sm font-bold text-white uppercase tracking-wider">
            Upload & Parse New Document
          </h2>
        </div>

        {uploadMessage && (
          <div
            className={`p-3 rounded-lg text-xs flex items-center gap-2 ${
              uploadMessage.type === 'success'
                ? 'bg-emerald-500/10 border border-emerald-500/20 text-emerald-400'
                : 'bg-rose-500/10 border border-rose-500/20 text-rose-400'
            }`}
          >
            {uploadMessage.type === 'success' ? (
              <CheckCircle2 className="w-4 h-4 shrink-0" />
            ) : (
              <AlertCircle className="w-4 h-4 shrink-0" />
            )}
            <span>{uploadMessage.text}</span>
          </div>
        )}

        <form onSubmit={handleUploadSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                File (PDF, DOCX, TXT - max 4MB)
              </label>
              <input
                type="file"
                accept=".pdf,.docx,.txt"
                onChange={handleFileChange}
                className="w-full text-xs text-slate-400 file:mr-3 file:py-2 file:px-3 file:rounded-md file:border-0 file:text-xs file:font-semibold file:bg-slate-800 file:text-slate-200 hover:file:bg-slate-700 cursor-pointer"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                Document Title
              </label>
              <input
                type="text"
                value={docTitle}
                onChange={(e) => setDocTitle(e.target.value)}
                placeholder="e.g. Writ Petition Ground Brief"
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-amber-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                Link to Case Brief (Optional)
              </label>
              <select
                value={selectedCaseId}
                onChange={(e) => setSelectedCaseId(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-amber-500"
              >
                <option value="">Unlinked / Standalone</option>
                {cases.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.case_number} - {c.title}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={uploading || !selectedFile}
              className="px-5 py-2.5 rounded-lg text-xs font-semibold bg-amber-500 hover:bg-amber-400 text-slate-950 flex items-center gap-2 shadow-lg shadow-amber-500/10 disabled:opacity-40"
            >
              <Upload className="w-3.5 h-3.5" />
              <span>{uploading ? 'Parsing & Encrypting...' : 'Upload Document'}</span>
            </button>
          </div>
        </form>
      </div>

      {/* Documents Vault Table */}
      <div className="space-y-4">
        <h2 className="text-sm font-bold text-white uppercase tracking-wider">
          Private Stored Documents ({documents.length})
        </h2>

        {loading ? (
          <div className="py-20 flex justify-center items-center">
            <div className="w-8 h-8 border-4 border-amber-500 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : documents.length > 0 ? (
          <div className="rounded-xl border border-slate-800 overflow-hidden bg-slate-900">
            <div className="divide-y divide-slate-800">
              {documents.map((doc) => (
                <div key={doc.id} className="p-5 flex items-center justify-between gap-4">
                  <div className="min-w-0 space-y-1">
                    <div className="flex items-center gap-2">
                      <FileText className="w-4 h-4 text-amber-400 shrink-0" />
                      <span className="font-semibold text-sm text-slate-200 truncate">
                        {doc.title}
                      </span>
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
                        {formatFileSize(doc.file_size)}
                      </span>
                    </div>

                    <div className="text-xs text-slate-500 flex flex-wrap items-center gap-3">
                      <span>{doc.original_filename}</span>
                      <span>•</span>
                      <span>{doc.page_count ?? 1} pages</span>
                      <span>•</span>
                      <span>Uploaded {formatDate(doc.created_at)}</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 shrink-0">
                    <span
                      className={`text-[10px] px-2.5 py-1 rounded-full font-medium border ${
                        doc.text_availability_status === 'FullText'
                          ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                          : doc.text_availability_status === 'ScannedImage'
                          ? 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                          : 'bg-slate-800 text-slate-400 border-slate-700'
                      }`}
                    >
                      {doc.text_availability_status}
                    </span>

                    <button
                      onClick={() => handleDelete(doc.id)}
                      className="p-1.5 text-slate-500 hover:text-rose-400 rounded-md hover:bg-slate-800 transition-colors"
                      title="Delete Document"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="text-center py-20 border border-dashed border-slate-800 rounded-xl bg-slate-900/40">
            <FileText className="w-10 h-10 text-slate-600 mx-auto mb-3" />
            <h3 className="text-sm font-semibold text-slate-300">No documents stored</h3>
            <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
              Upload your brief PDFs or DOCX files above to start extracting text.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
