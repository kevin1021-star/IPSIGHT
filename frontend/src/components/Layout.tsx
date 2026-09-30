import { NavLink, useNavigate } from 'react-router-dom';
import {
  Shield,
  LayoutDashboard,
  Upload,
  FileText,
  LogOut,
  ChevronRight,
  Wifi,
  User,
} from 'lucide-react';
import { clsx } from 'clsx';
import { useAuth } from '../lib/auth';
import type { ReactNode } from 'react';

interface NavItem {
  to: string;
  icon: ReactNode;
  label: string;
}

const NAV_ITEMS: NavItem[] = [
  { to: '/',        icon: <LayoutDashboard size={18} />, label: 'Dashboard'       },
  { to: '/upload',  icon: <Upload size={18} />,          label: 'New Assessment'  },
  { to: '/reports', icon: <FileText size={18} />,        label: 'Reports'         },
];

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="flex h-screen bg-[#0a0f1e] text-slate-100 overflow-hidden">
      {/* ── Sidebar (Desktop) ─────────────────────────────────────────── */}
      <aside className="w-64 flex-shrink-0 hidden md:flex flex-col bg-slate-950/90 border-r border-slate-800/80 backdrop-blur-md">
        {/* Logo */}
        <div className="flex items-center gap-3 px-5 py-5 border-b border-slate-800/80">
          <div className="relative">
            <div className="w-10 h-10 rounded-xl bg-cyan-500/20 border border-cyan-400/50 flex items-center justify-center">
              <Shield size={22} className="text-cyan-400" />
            </div>
            <span className="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse" />
          </div>
          <div>
            <p className="text-sm font-black tracking-widest text-cyan-400 uppercase leading-none">
              IP<span className="text-white">SIGHT</span>
            </p>
            <p className="text-[10px] font-semibold tracking-wider text-slate-400 uppercase leading-none mt-1">
              Team Praxis · IIT Jodhpur
            </p>
          </div>
        </div>

        {/* Status indicator */}
        <div className="mx-4 mt-4 px-3 py-2 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center gap-2">
          <Wifi size={13} className="text-emerald-400 flex-shrink-0" />
          <span className="text-xs text-emerald-400 font-medium">SecOps Node Active</span>
          <div className="ml-auto w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-3 py-4 space-y-1.5 overflow-y-auto">
          {NAV_ITEMS.map(({ to, icon, label }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                clsx(
                  'group flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200',
                  isActive
                    ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm shadow-cyan-500/10'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60',
                )
              }
            >
              {({ isActive }) => (
                <>
                  <span className={isActive ? 'text-cyan-400' : 'text-slate-500 group-hover:text-slate-300'}>
                    {icon}
                  </span>
                  <span className="flex-1">{label}</span>
                  {isActive && (
                    <ChevronRight size={14} className="text-cyan-400 opacity-80" />
                  )}
                </>
              )}
            </NavLink>
          ))}
        </nav>

        {/* User area */}
        <div className="p-3 border-t border-slate-800/80">
          <div className="flex items-center gap-3 px-3 py-2.5 rounded-lg bg-slate-900/60 border border-slate-800">
            <div className="w-8 h-8 rounded-full bg-cyan-600/30 border border-cyan-500/40 flex items-center justify-center flex-shrink-0">
              <User size={14} className="text-cyan-300" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-semibold text-slate-200 truncate">
                {user?.email ?? 'analyst@praxis.iitj.ac.in'}
              </p>
              <p className="text-[10px] text-cyan-400/80 font-mono">SecOps Lead Analyst</p>
            </div>
            <button
              onClick={handleLogout}
              title="Logout"
              className="text-slate-400 hover:text-red-400 transition-colors p-1.5 rounded-lg hover:bg-slate-800"
            >
              <LogOut size={15} />
            </button>
          </div>
        </div>
      </aside>

      {/* ── Main Content Area ────────────────────────────────────────── */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top bar */}
        <header className="flex items-center justify-between px-4 md:px-6 py-3.5 border-b border-slate-800/80 bg-slate-950/60 backdrop-blur-md flex-shrink-0">
          <div className="flex items-center gap-3">
            <div className="md:hidden flex items-center gap-2">
              <div className="w-7 h-7 rounded-lg bg-cyan-500/20 border border-cyan-400/40 flex items-center justify-center">
                <Shield size={16} className="text-cyan-400" />
              </div>
              <span className="font-bold text-sm text-cyan-400">IPsight</span>
            </div>
            <div className="hidden md:flex items-center gap-2">
              <div className="w-1.5 h-4 rounded-full bg-cyan-400" />
              <span className="text-xs text-slate-400 uppercase tracking-widest font-semibold">
                AI-Powered IPsec Security Assessment Framework
              </span>
            </div>
          </div>
          
          {/* Top navigation for Mobile */}
          <div className="flex md:hidden items-center gap-2">
            {NAV_ITEMS.map(({ to, label }) => (
              <NavLink
                key={to}
                to={to}
                end={to === '/'}
                className={({ isActive }) =>
                  clsx(
                    'px-2.5 py-1 rounded-md text-xs font-semibold',
                    isActive ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40' : 'text-slate-400',
                  )
                }
              >
                {label}
              </NavLink>
            ))}
            <button onClick={handleLogout} className="p-1.5 text-slate-400 hover:text-red-400">
              <LogOut size={14} />
            </button>
          </div>

          <div className="hidden md:flex items-center gap-4">
            <span className="text-xs text-slate-400 font-mono bg-slate-900 px-2 py-0.5 rounded border border-slate-800">
              SIH 2026 · PS: SIH26160
            </span>
            <div className="flex items-center gap-1.5 text-xs text-emerald-400 font-medium">
              <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span>100% Offline Ready</span>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto p-4 md:p-6 bg-[#0a0f1e]">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
