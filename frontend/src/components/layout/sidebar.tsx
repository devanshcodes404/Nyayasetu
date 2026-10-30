import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Briefcase,
  Search,
  BookOpen,
  FileText,
  Quote,
  TrendingUp,
  Settings,
  Scale,
} from 'lucide-react';
import { cn } from '../../lib/utils';

interface NavItem {
  name: string;
  href: string;
  icon: React.ElementType;
}

const navItems: NavItem[] = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'My Cases', href: '/cases', icon: Briefcase },
  { name: 'Judgments Corpus', href: '/judgments', icon: BookOpen },
  { name: 'Case Documents', href: '/documents', icon: FileText },
  { name: 'Legal Research', href: '/research', icon: Search },
  { name: 'Citations', href: '/citations', icon: Quote },
  { name: 'Outcome Insights', href: '/insights', icon: TrendingUp },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export const Sidebar: React.FC = () => {
  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col shrink-0 min-h-screen">
      {/* Brand Header */}
      <div className="h-16 flex items-center px-6 gap-3 border-b border-slate-800">
        <img src="/logo.svg" alt="NyayaSetu AI Logo" className="w-8 h-8" />
        <div className="flex flex-col">
          <span className="font-bold text-base tracking-wide text-white flex items-center gap-1.5">
            NyayaSetu <span className="text-amber-500 font-extrabold text-xs uppercase px-1.5 py-0.5 rounded bg-amber-500/10 border border-amber-500/20">AI</span>
          </span>
          <span className="text-[10px] text-slate-400 font-medium">Indian Case Law & Court SaaS</span>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="p-4 space-y-1.5 flex-1">
        <div className="px-3 pb-2 text-[11px] font-semibold uppercase tracking-wider text-slate-500">
          Core Workspace
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.name}
              to={item.href}
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-colors',
                  isActive
                    ? 'bg-amber-500/15 text-amber-400 border border-amber-500/30'
                    : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
                )
              }
            >
              <Icon className="w-4 h-4 shrink-0" />
              <span>{item.name}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* Dataset Provenance Pill */}
      <div className="p-4 border-t border-slate-800">
        <div className="p-3 rounded-lg bg-slate-950/70 border border-slate-800 text-xs">
          <div className="flex items-center gap-1.5 text-amber-400 font-semibold mb-1">
            <Scale className="w-3.5 h-3.5" />
            <span>Public Corpus</span>
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            Powered by Sumitedu Indian Case-Laws & indexed legal records.
          </p>
        </div>
      </div>
    </aside>
  );
};

