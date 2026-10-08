import React from 'react';
import { NavLink, Link } from 'react-router-dom';
import {
  LayoutDashboard,
  Wand2,
  Layers,
  ShoppingBag,
  BarChart3,
  Sliders,
  ShieldCheck,
  HelpCircle,
  Sparkles,
  ChevronRight,
  PlusCircle,
  Cpu,
  Zap
} from 'lucide-react';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const navItems = [
    { path: '/', label: 'Overview Dashboard', icon: <LayoutDashboard className="w-4 h-4" /> },
    { path: '/generate', label: 'Copywriting Studio', icon: <Wand2 className="w-4 h-4" />, badge: 'Dual-AI' },
    { path: '/batch', label: 'Batch Generation', icon: <Layers className="w-4 h-4" /> },
    { path: '/catalogue', label: 'Product Catalog', icon: <ShoppingBag className="w-4 h-4" /> },
    { path: '/analytics', label: 'Quality Analytics', icon: <BarChart3 className="w-4 h-4" /> },
    { path: '/brand-settings', label: 'Brand Voice Guardrails', icon: <Sliders className="w-4 h-4" /> },
    { path: '/responsible-ai', label: 'Responsible AI & Safety', icon: <ShieldCheck className="w-4 h-4" /> },
    { path: '/help', label: 'Docs & System Guide', icon: <HelpCircle className="w-4 h-4" /> },
  ];

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-slate-950/70 backdrop-blur-sm md:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={`fixed top-0 left-0 z-50 h-full w-68 bg-slate-950/95 backdrop-blur-xl text-slate-100 flex flex-col justify-between border-r border-slate-800/80 transition-transform duration-300 ease-in-out md:static md:translate-x-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex flex-col flex-1 overflow-y-auto">
          {/* Brand Header */}
          <div className="px-5 py-5 border-b border-slate-800/60 bg-gradient-to-b from-slate-900/60 to-transparent">
            <Link to="/" onClick={onClose} className="flex items-center gap-3 group">
              <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-cyan-400 p-0.5 shadow-lg shadow-blue-500/25 group-hover:scale-105 transition-transform duration-200">
                <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
                  <Sparkles className="w-5 h-5 text-cyan-400 animate-pulse" />
                </div>
              </div>
              <div>
                <div className="flex items-center gap-1.5">
                  <span className="font-extrabold text-base tracking-tight text-white group-hover:text-cyan-300 transition-colors">
                    CatalogCraft
                  </span>
                  <span className="text-[10px] font-black uppercase tracking-wider px-1.5 py-0.5 rounded bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow-xs">
                    AI
                  </span>
                </div>
                <p className="text-[10px] text-slate-400 font-medium">Enterprise Product Copy Engine</p>
              </div>
            </Link>

            {/* Quick Action Generate Button */}
            <div className="mt-4">
              <Link
                to="/generate"
                onClick={onClose}
                className="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs font-bold text-white bg-gradient-to-r from-blue-600 via-indigo-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 shadow-md shadow-blue-600/25 transition-all duration-200 hover:shadow-blue-500/40 cursor-pointer"
              >
                <PlusCircle className="w-3.5 h-3.5" />
                <span>New Description</span>
              </Link>
            </div>
          </div>

          {/* Navigation Items */}
          <nav className="p-3.5 space-y-1 flex-1">
            <div className="px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider text-slate-500">
              Workspace Navigation
            </div>
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={onClose}
                className={({ isActive }) =>
                  `flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-semibold transition-all duration-150 ${
                    isActive
                      ? 'bg-blue-600/90 text-white shadow-md shadow-blue-600/30 border border-blue-500/40'
                      : 'text-slate-400 hover:text-white hover:bg-slate-900/90 hover:border-slate-800 border border-transparent'
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    <div className="flex items-center gap-2.5">
                      <span className={isActive ? 'text-white' : 'text-slate-400 group-hover:text-cyan-400'}>
                        {item.icon}
                      </span>
                      <span>{item.label}</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      {item.badge && (
                        <span className="text-[9px] font-bold px-1.5 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-400/30">
                          {item.badge}
                        </span>
                      )}
                      {isActive && <ChevronRight className="w-3.5 h-3.5 text-blue-200" />}
                    </div>
                  </>
                )}
              </NavLink>
            ))}
          </nav>
        </div>

        {/* Live Model Arena Status Footer */}
        <div className="p-3.5 m-3 rounded-xl bg-slate-900/80 border border-slate-800/80 space-y-2.5 shadow-inner">
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1">
              <Cpu className="w-3 h-3 text-cyan-400" /> Active AI Arbiter
            </span>
            <span className="flex h-2 w-2 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
            </span>
          </div>

          <div className="space-y-1.5 text-[11px]">
            <div className="flex items-center justify-between text-slate-300">
              <span className="flex items-center gap-1.5 text-purple-300 font-medium">
                <span className="w-1.5 h-1.5 rounded-full bg-purple-400" /> Claude 3.5 Sonnet
              </span>
              <span className="text-[9px] text-slate-400 font-mono">Narrative</span>
            </div>
            <div className="flex items-center justify-between text-slate-300">
              <span className="flex items-center gap-1.5 text-cyan-300 font-medium">
                <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" /> Gemini 3.5 Lite
              </span>
              <span className="text-[9px] text-slate-400 font-mono">Structured</span>
            </div>
          </div>

          <div className="pt-2 border-t border-slate-800 text-[10px] text-slate-400 flex items-center justify-between">
            <span>Enterprise Edition</span>
            <span className="text-emerald-400 font-medium flex items-center gap-1">
              <Zap className="w-2.5 h-2.5" /> Production Ready
            </span>
          </div>
        </div>
      </aside>
    </>
  );
};
