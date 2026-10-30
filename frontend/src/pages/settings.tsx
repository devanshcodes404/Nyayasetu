import React, { useEffect, useState } from 'react';
import { useAuth } from '../hooks/use-auth';
import { apiClient } from '../lib/api-client';
import { DatasetStatus } from '../types/api';
import { Database, Shield, User } from 'lucide-react';

export const SettingsPage: React.FC = () => {
  const { user } = useAuth();
  const [datasetStatus, setDatasetStatus] = useState<DatasetStatus | null>(null);

  useEffect(() => {
    apiClient
      .get<DatasetStatus>('/dataset/status')
      .then((data) => setDatasetStatus(data))
      .catch((err) => console.error('Failed to load dataset status', err));
  }, []);

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white">Platform Settings & Status</h1>
        <p className="text-xs text-slate-400 mt-1">
          Review advocate profile details, environment configuration, and dataset pipeline state.
        </p>
      </div>

      {/* User Profile */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4">
        <div className="flex items-center gap-2">
          <User className="w-4 h-4 text-amber-400" />
          <h2 className="text-sm font-bold text-white uppercase tracking-wider">
            Advocate Profile
          </h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
          <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
            <span className="text-slate-500 uppercase font-semibold text-[10px] block">Full Name</span>
            <span className="text-slate-200 font-medium mt-0.5 block">{user?.full_name}</span>
          </div>

          <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
            <span className="text-slate-500 uppercase font-semibold text-[10px] block">Email Address</span>
            <span className="text-slate-200 font-medium mt-0.5 block">{user?.email}</span>
          </div>
        </div>
      </div>

      {/* Hugging Face Corpus Pipeline State */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4">
        <div className="flex items-center gap-2">
          <Database className="w-4 h-4 text-amber-400" />
          <h2 className="text-sm font-bold text-white uppercase tracking-wider">
            Dataset Ingestion Pipeline Status
          </h2>
        </div>

        {datasetStatus ? (
          <div className="space-y-4 text-xs">
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
                <span className="text-slate-500 text-[10px] uppercase font-semibold block">Total Ingested</span>
                <span className="text-base font-bold text-white mt-0.5 block">
                  {datasetStatus.total_judgments_imported}
                </span>
              </div>

              <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
                <span className="text-slate-500 text-[10px] uppercase font-semibold block">Full Text Available</span>
                <span className="text-base font-bold text-emerald-400 mt-0.5 block">
                  {datasetStatus.judgments_with_full_text}
                </span>
              </div>

              <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
                <span className="text-slate-500 text-[10px] uppercase font-semibold block">Headnotes Only</span>
                <span className="text-base font-bold text-blue-400 mt-0.5 block">
                  {datasetStatus.judgments_with_headnotes}
                </span>
              </div>

              <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
                <span className="text-slate-500 text-[10px] uppercase font-semibold block">Courts Represented</span>
                <span className="text-base font-bold text-amber-400 mt-0.5 block">
                  {datasetStatus.courts_represented}
                </span>
              </div>
            </div>

            <div className="p-3 rounded-lg bg-slate-950 border border-slate-800 font-mono text-[11px] text-slate-400 space-y-1">
              <div>Source Dataset: <span className="text-slate-200">{datasetStatus.dataset_id}</span></div>
              <div>Database Backend: <span className="text-slate-200">{datasetStatus.storage_type}</span></div>
              <div>Search Index Status: <span className="text-emerald-400">{datasetStatus.is_ready_for_search ? 'Active & Ready' : 'Empty'}</span></div>
            </div>
          </div>
        ) : (
          <p className="text-xs text-slate-500">Loading dataset pipeline metrics...</p>
        )}
      </div>

      {/* Deployment & Security Notice */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-3">
        <div className="flex items-center gap-2">
          <Shield className="w-4 h-4 text-amber-400" />
          <h2 className="text-sm font-bold text-white uppercase tracking-wider">
            Vercel Deployment Architecture
          </h2>
        </div>
        <p className="text-xs text-slate-400 leading-relaxed">
          NyayaSetu AI is configured for dual-project deployment on Vercel: frontend React SPA on Vite, and backend FastAPI on Python 3.12 Serverless Functions with Neon PostgreSQL and Vercel Blob private document storage.
        </p>
      </div>
    </div>
  );
};
