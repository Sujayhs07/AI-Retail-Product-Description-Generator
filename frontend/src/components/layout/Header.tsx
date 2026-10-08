import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Menu, Sun, Moon, Cpu, Download, Sparkles, ChevronDown, Check, Zap, Wand2 } from 'lucide-react';
import { useTheme } from '../../hooks/useTheme';
import { analyticsApi, exportApi } from '../../api';
import { HealthStatus } from '../../types';

interface HeaderProps {
  onOpenSidebar: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onOpenSidebar }) => {
  const { theme, toggleTheme } = useTheme();
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [showExportMenu, setShowExportMenu] = useState(false);

  useEffect(() => {
    analyticsApi
      .getHealthStatus()
      .then(setHealth)
      .catch((err) => console.error('Failed to fetch health status:', err));
  }, []);

  return (
    <header className="sticky top-0 z-30 flex items-center justify-between px-5 sm:px-8 py-3.5 bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl border-b border-slate-200/80 dark:border-slate-800/80 transition-colors shadow-2xs">
      <div className="flex items-center gap-3">
        <button
          onClick={onOpenSidebar}
          className="p-2 text-slate-600 dark:text-slate-300 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 md:hidden cursor-pointer"
          aria-label="Open sidebar"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-sm sm:text-base font-extrabold text-slate-900 dark:text-white tracking-tight">
              Retail AI Studio
            </h2>
            <span className="hidden sm:inline-flex items-center gap-1 text-[11px] font-bold px-2 py-0.5 rounded-full bg-blue-50 dark:bg-blue-950/70 text-blue-600 dark:text-blue-400 border border-blue-200/80 dark:border-blue-800/80">
              <Sparkles className="w-3 h-3 text-cyan-500" />
              v1.0 Live
            </span>
          </div>
          <p className="hidden md:block text-[11px] text-slate-500 dark:text-slate-400 font-medium">
            Benchmarking <strong className="text-purple-600 dark:text-purple-400">Claude 3.5 Sonnet</strong> & <strong className="text-cyan-600 dark:text-cyan-400">Gemini 3.5 Lite</strong> for catalog-scale copy.
          </p>
        </div>
      </div>

      <div className="flex items-center gap-2.5 sm:gap-3">
        {/* Quick Studio CTA */}
        <Link
          to="/generate"
          className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold text-slate-700 dark:text-slate-200 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200/80 dark:hover:bg-slate-750 border border-slate-200 dark:border-slate-700 transition-all cursor-pointer"
        >
          <Wand2 className="w-3.5 h-3.5 text-blue-500" />
          <span>Launch Generator</span>
        </Link>

        {/* AI Engine Status Badge */}
        {health && (
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl border text-xs font-medium bg-slate-50/90 dark:bg-slate-800/80 border-slate-200 dark:border-slate-700/80 shadow-2xs">
            <Cpu className="w-3.5 h-3.5 text-blue-500 shrink-0" />
            <div className="flex items-center gap-1.5">
              <span className="text-[11px] font-bold text-slate-800 dark:text-slate-200 hidden lg:inline">
                {health.ai_mode === 'dual'
                  ? 'Dual-AI Active'
                  : health.ai_mode === 'claude'
                  ? 'Claude Active'
                  : health.ai_mode === 'gemini'
                  ? 'Gemini Active'
                  : 'Offline Mock'}
              </span>

              <div className="flex items-center gap-1">
                <span
                  title={health.anthropic_configured ? 'Anthropic Claude Online' : 'Anthropic Mock'}
                  className={`px-1.5 py-0.5 rounded text-[10px] font-bold font-mono ${
                    health.anthropic_configured
                      ? 'bg-purple-100 text-purple-700 dark:bg-purple-950/80 dark:text-purple-300'
                      : 'bg-slate-200 text-slate-600 dark:bg-slate-800 dark:text-slate-400'
                  }`}
                >
                  Claude
                </span>
                <span
                  title={health.gemini_configured ? 'Google Gemini Online' : 'Gemini Mock'}
                  className={`px-1.5 py-0.5 rounded text-[10px] font-bold font-mono ${
                    health.gemini_configured
                      ? 'bg-cyan-100 text-cyan-700 dark:bg-cyan-950/80 dark:text-cyan-300'
                      : 'bg-slate-200 text-slate-600 dark:bg-slate-800 dark:text-slate-400'
                  }`}
                >
                  Gemini
                </span>
              </div>
            </div>
          </div>
        )}

        {/* Quick Export Dropdown */}
        <div className="relative">
          <button
            onClick={() => setShowExportMenu(!showExportMenu)}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-xl border border-slate-200 dark:border-slate-700 transition-colors shadow-2xs cursor-pointer"
          >
            <Download className="w-3.5 h-3.5 text-slate-500" />
            <span className="hidden sm:inline">Export</span>
            <ChevronDown className="w-3 h-3 text-slate-400" />
          </button>

          {showExportMenu && (
            <div className="absolute right-0 mt-2 w-52 rounded-2xl bg-white dark:bg-slate-850 shadow-2xl border border-slate-200 dark:border-slate-700 p-1.5 z-50 animate-in fade-in zoom-in-95 duration-100">
              <a
                href={exportApi.getProductsCsvUrl()}
                target="_blank"
                rel="noreferrer"
                onClick={() => setShowExportMenu(false)}
                className="flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium text-slate-700 dark:text-slate-200 hover:bg-blue-50 dark:hover:bg-blue-950/50 hover:text-blue-600 dark:hover:text-blue-300 transition-colors"
              >
                <span>Export Products (CSV)</span>
                <span className="text-[10px] font-mono text-slate-400">.csv</span>
              </a>
              <a
                href={exportApi.getProductsJsonUrl()}
                target="_blank"
                rel="noreferrer"
                onClick={() => setShowExportMenu(false)}
                className="flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium text-slate-700 dark:text-slate-200 hover:bg-blue-50 dark:hover:bg-blue-950/50 hover:text-blue-600 dark:hover:text-blue-300 transition-colors"
              >
                <span>Export Products (JSON)</span>
                <span className="text-[10px] font-mono text-slate-400">.json</span>
              </a>
            </div>
          )}
        </div>

        {/* Theme Switcher */}
        <button
          onClick={toggleTheme}
          className="p-2 text-slate-600 dark:text-slate-300 bg-white dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-xl border border-slate-200 dark:border-slate-700 transition-colors cursor-pointer shadow-2xs"
          aria-label="Toggle Dark Mode"
          title={`Switch to ${theme === 'light' ? 'Dark' : 'Light'} Mode`}
        >
          {theme === 'light' ? <Moon className="w-4 h-4 text-slate-700" /> : <Sun className="w-4 h-4 text-amber-400 animate-spin-slow" />}
        </button>
      </div>
    </header>
  );
};
