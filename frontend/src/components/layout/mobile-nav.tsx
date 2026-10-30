import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { Menu, X, Briefcase, BookOpen, FileText, Search, LayoutDashboard } from 'lucide-react';

export const MobileNav: React.FC = () => {
  const [open, setOpen] = useState(false);

  return (
    <div className="md:hidden border-b border-slate-800 bg-slate-900 px-4 py-3 flex items-center justify-between">
      <div className="flex items-center gap-2">
        <img src="/logo.svg" alt="NyayaSetu AI" className="w-7 h-7" />
        <span className="font-bold text-sm text-white">NyayaSetu AI</span>
      </div>
      <button
        onClick={() => setOpen(!open)}
        className="p-1.5 text-slate-300 hover:text-white rounded-md bg-slate-800"
      >
        {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
      </button>

      {open && (
        <div className="absolute top-14 left-0 w-full bg-slate-900 border-b border-slate-800 p-4 space-y-2 z-50">
          <NavLink
            to="/dashboard"
            onClick={() => setOpen(false)}
            className="flex items-center gap-2 px-3 py-2 text-sm text-slate-300 hover:bg-slate-800 rounded-md"
          >
            <LayoutDashboard className="w-4 h-4" /> Dashboard
          </NavLink>
          <NavLink
            to="/cases"
            onClick={() => setOpen(false)}
            className="flex items-center gap-2 px-3 py-2 text-sm text-slate-300 hover:bg-slate-800 rounded-md"
          >
            <Briefcase className="w-4 h-4" /> My Cases
          </NavLink>
          <NavLink
            to="/judgments"
            onClick={() => setOpen(false)}
            className="flex items-center gap-2 px-3 py-2 text-sm text-slate-300 hover:bg-slate-800 rounded-md"
          >
            <BookOpen className="w-4 h-4" /> Judgments Corpus
          </NavLink>
          <NavLink
            to="/documents"
            onClick={() => setOpen(false)}
            className="flex items-center gap-2 px-3 py-2 text-sm text-slate-300 hover:bg-slate-800 rounded-md"
          >
            <FileText className="w-4 h-4" /> Case Documents
          </NavLink>
          <NavLink
            to="/research"
            onClick={() => setOpen(false)}
            className="flex items-center gap-2 px-3 py-2 text-sm text-slate-300 hover:bg-slate-800 rounded-md"
          >
            <Search className="w-4 h-4" /> Legal Research
          </NavLink>
        </div>
      )}
    </div>
  );
};

