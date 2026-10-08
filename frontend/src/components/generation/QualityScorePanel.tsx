import React from 'react';
import { ScoreBadge } from '../common/ScoreBadge';
import { ShieldCheck, Search, BookOpen, Sparkles, AlertTriangle } from 'lucide-react';

interface QualityScorePanelProps {
  qualityScore: number;
  completenessScore: number;
  seoScore: number;
  readabilityScore: number;
  brandToneScore: number;
  warnings?: string[];
  recommendations?: string[];
}

export const QualityScorePanel: React.FC<QualityScorePanelProps> = ({
  qualityScore,
  completenessScore,
  seoScore,
  readabilityScore,
  brandToneScore,
  warnings = [],
  recommendations = []
}) => {
  const subMetrics = [
    { label: 'Completeness', score: completenessScore, icon: <ShieldCheck className="w-4 h-4 text-blue-500" /> },
    { label: 'SEO Optimization', score: seoScore, icon: <Search className="w-4 h-4 text-emerald-500" /> },
    { label: 'Readability', score: readabilityScore, icon: <BookOpen className="w-4 h-4 text-purple-500" /> },
    { label: 'Brand Alignment', score: brandToneScore, icon: <Sparkles className="w-4 h-4 text-cyan-500" /> },
  ];

  return (
    <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-sm space-y-4">
      <div className="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
        <div>
          <h3 className="text-sm font-bold text-slate-900 dark:text-white">Content Quality Score</h3>
          <p className="text-xs text-slate-500 dark:text-slate-400">Automated 4-dimension copy evaluation</p>
        </div>
        <ScoreBadge score={qualityScore} size="lg" />
      </div>

      {/* Sub Scores Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {subMetrics.map((m) => (
          <div
            key={m.label}
            className="p-3 rounded-lg bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800 flex flex-col justify-between"
          >
            <div className="flex items-center gap-1.5 text-xs text-slate-600 dark:text-slate-400 font-medium mb-1">
              {m.icon}
              <span>{m.label}</span>
            </div>
            <div className="text-base font-bold text-slate-900 dark:text-white">
              {(m.score ?? 0).toFixed(0)} <span className="text-xs font-normal text-slate-400">/ 100</span>
            </div>
          </div>
        ))}
      </div>

      {/* Warnings & Recommendations */}
      {(warnings.length > 0 || recommendations.length > 0) && (
        <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 space-y-2">
          <h4 className="text-xs font-bold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-500" />
            Recommendations & Warnings ({warnings.length + recommendations.length})
          </h4>
          <ul className="space-y-1.5 text-xs text-slate-600 dark:text-slate-400">
            {warnings.map((w, idx) => (
              <li key={`warn-${idx}`} className="flex items-start gap-2 bg-amber-50/60 dark:bg-amber-950/20 p-2 rounded-md border border-amber-200/50 dark:border-amber-800/50 text-amber-800 dark:text-amber-300">
                <span className="font-bold text-amber-500">•</span>
                <span>{w}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
