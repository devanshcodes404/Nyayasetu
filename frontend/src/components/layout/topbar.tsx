import React from 'react';
import { useAuth } from '../../hooks/use-auth';
import { LogOut, Bell, Search } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const Topbar: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <header className="h-16 bg-slate-900/60 backdrop-blur-md border-b border-slate-800 px-6 flex items-center justify-between sticky top-0 z-20">
      {/* Quick Search Shortcut */}
      <div className="flex items-center gap-2 max-w-md w-full">
        <div className="relative w-full">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search judgments, citations, or case numbers..."
            onClick={() => navigate('/judgments')}
            readOnly
            className="w-full bg-slate-950/80 border border-slate-800 rounded-lg pl-9 pr-4 py-1.5 text-xs text-slate-200 placeholder:text-slate-500 cursor-pointer focus:outline-none focus:border-amber-500/50"
          />
        </div>
      </div>

      {/* Right User Bar */}
      <div className="flex items-center gap-4">
        <button
          title="Notifications"
          className="p-2 text-slate-400 hover:text-slate-200 rounded-lg hover:bg-slate-800 transition-colors"
        >
          <Bell className="w-4 h-4" />
        </button>

        {user && (
          <div className="flex items-center gap-3 pl-2 border-l border-slate-800">
            <div className="flex flex-col text-right">
              <span className="text-xs font-semibold text-slate-200">{user.full_name}</span>
              <span className="text-[10px] text-slate-400">{user.email}</span>
            </div>
            <div className="w-8 h-8 rounded-full bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-amber-400 font-bold text-xs">
              {user.full_name.charAt(0).toUpperCase()}
            </div>
            <button
              onClick={handleLogout}
              title="Sign Out"
              className="p-1.5 text-slate-400 hover:text-rose-400 rounded-md hover:bg-slate-800 transition-colors ml-1"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>
    </header>
  );
};
