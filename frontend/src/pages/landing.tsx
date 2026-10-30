import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, BookOpen, Briefcase, Sparkles, ArrowRight } from 'lucide-react';

export const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-amber-500 selection:text-slate-900">
      {/* Top Navigation */}
      <header className="h-20 border-b border-slate-800/80 px-8 flex items-center justify-between max-w-7xl mx-auto w-full">
        <div className="flex items-center gap-3">
          <img src="/logo.svg" alt="NyayaSetu AI" className="w-9 h-9" />
          <span className="font-extrabold text-xl tracking-tight text-white">
            NyayaSetu <span className="text-amber-500">AI</span>
          </span>
        </div>
        <div className="flex items-center gap-4">
          <Link
            to="/login"
            className="text-sm font-medium text-slate-300 hover:text-white px-4 py-2 rounded-lg hover:bg-slate-900 transition-colors"
          >
            Sign In
          </Link>
          <Link
            to="/register"
            className="text-sm font-semibold text-slate-950 bg-amber-500 hover:bg-amber-400 px-5 py-2.5 rounded-lg transition-colors shadow-lg shadow-amber-500/20"
          >
            Create Advocate Account
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-6 max-w-5xl mx-auto text-center flex-1 flex flex-col justify-center items-center">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-semibold mb-6">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Part 1: Full-Stack Platform & Indian Case-Law Corpus</span>
        </div>

        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight text-white mb-6 leading-tight">
          Modern Court Case Management & Legal Intelligence for Indian Law
        </h1>

        <p className="text-lg md:text-xl text-slate-400 max-w-3xl mb-10 leading-relaxed">
          Manage court briefs, track hearing schedules, parse case documents, and search the public Indian judgment corpus.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center w-full max-w-md">
          <Link
            to="/register"
            className="flex items-center justify-center gap-2 font-semibold bg-amber-500 hover:bg-amber-400 text-slate-950 px-6 py-3.5 rounded-xl transition-colors shadow-xl shadow-amber-500/20"
          >
            <span>Get Started</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
          <Link
            to="/judgments"
            className="flex items-center justify-center gap-2 font-semibold bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 px-6 py-3.5 rounded-xl transition-colors"
          >
            <BookOpen className="w-4 h-4 text-amber-400" />
            <span>Search Case Law Corpus</span>
          </Link>
        </div>

        {/* Feature Grid */}
        <div className="grid md:grid-cols-3 gap-6 text-left mt-20 w-full">
          <div className="p-6 rounded-xl bg-slate-900/60 border border-slate-800">
            <div className="w-10 h-10 rounded-lg bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400 mb-4">
              <Briefcase className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-base text-slate-100 mb-2">Court Case Management</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Track docket numbers, hearing dates, courts, and clients with strict owner-level multi-tenancy.
            </p>
          </div>

          <div className="p-6 rounded-xl bg-slate-900/60 border border-slate-800">
            <div className="w-10 h-10 rounded-lg bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400 mb-4">
              <BookOpen className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-base text-slate-100 mb-2">Indian Case-Law Corpus</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Real judgment search by party names, neutral citations, courts, and decision years powered by PostgreSQL indexing.
            </p>
          </div>

          <div className="p-6 rounded-xl bg-slate-900/60 border border-slate-800">
            <div className="w-10 h-10 rounded-lg bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400 mb-4">
              <Shield className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-base text-slate-100 mb-2">Private Document Vault</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              PDF/DOCX text parsing and private Vercel Blob storage with strict document isolation.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 py-8 px-6 text-center text-xs text-slate-500">
        <p>© 2026 NyayaSetu AI. Independent legal-tech research platform. Not affiliated with government departments or courts of India.</p>
      </footer>
    </div>
  );
};
