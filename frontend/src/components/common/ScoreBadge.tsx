import React from 'react';
import { getScoreColorClass } from '../../lib/utils';

interface ScoreBadgeProps {
  score?: number;
  label?: string;
  size?: 'sm' | 'md' | 'lg';
}

export const ScoreBadge: React.FC<ScoreBadgeProps> = ({ score, label, size = 'md' }) => {
  const numScore = typeof score === 'number' && !isNaN(score) ? score : 0;
  const colors = getScoreColorClass(numScore);

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs font-semibold',
    md: 'px-2.5 py-1 text-xs font-bold',
    lg: 'px-3 py-1.5 text-sm font-bold',
  }[size];

  return (
    <div className="inline-flex items-center gap-1.5">
      {label && <span className="text-xs font-medium text-slate-500 dark:text-slate-400">{label}:</span>}
      <span
        className={`inline-flex items-center rounded-full border ${colors.bg} ${colors.text} ${colors.border} ${sizeClasses}`}
      >
        <span className={`mr-1.5 h-1.5 w-1.5 rounded-full ${colors.badgeBg}`} />
        {numScore.toFixed(0)} / 100
      </span>
    </div>
  );
};
