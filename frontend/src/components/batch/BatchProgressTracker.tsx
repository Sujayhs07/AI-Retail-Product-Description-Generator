import React, { useState } from 'react';
import { BatchJob } from '../../types';
import { StatusBadge } from '../common/StatusBadge';
import { exportApi } from '../../api';
import {
  Play,
  RotateCw,
  CheckCircle2,
  AlertTriangle,
  FileSpreadsheet,
  FileCode,
  Layers,
  Sparkles
} from 'lucide-react';

interface BatchProgressTrackerProps {
  job: BatchJob;
  onStartGeneration: (options: { tone: string; language: string; word_count_preference: string }) => void;
  onRetryFailed: () => void;
  isProcessing: boolean;
}

export const BatchProgressTracker: React.FC<BatchProgressTrackerProps> = ({
  job,
  onStartGeneration,
  onRetryFailed,
  isProcessing,
}) => {
  const [tone, setTone] = useState('Professional');
  const [language, setLanguage] = useState('English');
  const [wordCount, setWordCount] = useState('Medium');

  const percentage = job.total_products > 0
    ? Math.round((job.processed_products / job.total_products) * 100)
    : 0;

  return (
    <div className="space-y-6">
      {/* Overview Header Card */}
      <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 shadow-sm space-y-5">
        <div className="flex flex-wrap items-center justify-between gap-3 pb-4 border-b border-slate-100 dark:border-slate-800">
          <div>
            <div className="flex items-center gap-2">
              <Layers className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              <h3 className="text-base font-bold text-slate-900 dark:text-white">
                Batch Job: {job.file_name}
              </h3>
              <StatusBadge status={job.status} />
            </div>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              File type: {job.file_type.toUpperCase()} • Created: {new Date(job.created_at).toLocaleTimeString()}
            </p>
          </div>

          <div className="flex items-center gap-2">
            {job.status === 'completed' && (
              <>
                <a
                  href={exportApi.getBatchCsvUrl(job.id)}
                  download
                  className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-700 dark:text-slate-200 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 rounded-lg transition-colors"
                >
                  <FileSpreadsheet className="w-3.5 h-3.5 text-emerald-500" />
                  Export CSV
                </a>
                <a
                  href={exportApi.getBatchJsonUrl(job.id)}
                  download
                  className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-700 dark:text-slate-200 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 rounded-lg transition-colors"
                >
                  <FileCode className="w-3.5 h-3.5 text-cyan-500" />
                  Export JSON
                </a>
              </>
            )}

            {job.failed_products > 0 && job.status !== 'processing' && (
              <button
                onClick={onRetryFailed}
                className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-bold text-amber-800 dark:text-amber-300 bg-amber-100 dark:bg-amber-950/60 border border-amber-300 dark:border-amber-800 hover:bg-amber-200 rounded-lg transition-colors cursor-pointer"
              >
                <RotateCw className="w-3.5 h-3.5" /> Retry {job.failed_products} Failed
              </button>
            )}
          </div>
        </div>

        {/* Progress Bar */}
        <div>
          <div className="flex justify-between text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
            <span>Overall Batch Progress</span>
            <span>{percentage}% ({job.processed_products} / {job.total_products} items)</span>
          </div>
          <div className="w-full h-3 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden p-0.5 border border-slate-200 dark:border-slate-700">
            <div
              className="h-full bg-gradient-to-r from-blue-600 to-cyan-500 rounded-full transition-all duration-300"
              style={{ width: `${percentage}%` }}
            />
          </div>
        </div>

        {/* Summary Counter Badges */}
        <div className="grid grid-cols-4 gap-3 text-center">
          <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800">
            <span className="text-[10px] font-bold text-slate-400 uppercase">Total Rows</span>
            <p className="text-lg font-bold text-slate-900 dark:text-white">{job.total_products}</p>
          </div>
          <div className="p-3 rounded-lg bg-blue-50/50 dark:bg-blue-950/30 border border-blue-100 dark:border-blue-900">
            <span className="text-[10px] font-bold text-blue-500 uppercase">Processed</span>
            <p className="text-lg font-bold text-blue-700 dark:text-blue-300">{job.processed_products}</p>
          </div>
          <div className="p-3 rounded-lg bg-emerald-50/50 dark:bg-emerald-950/30 border border-emerald-100 dark:border-emerald-900">
            <span className="text-[10px] font-bold text-emerald-500 uppercase">Successful</span>
            <p className="text-lg font-bold text-emerald-700 dark:text-emerald-300">{job.successful_products}</p>
          </div>
          <div className="p-3 rounded-lg bg-rose-50/50 dark:bg-rose-950/30 border border-rose-100 dark:border-rose-900">
            <span className="text-[10px] font-bold text-rose-500 uppercase">Failed / Errors</span>
            <p className="text-lg font-bold text-rose-700 dark:text-rose-300">{job.failed_products}</p>
          </div>
        </div>

        {/* Start Generation Form Controls */}
        {job.status === 'pending' && (
          <div className="p-4 rounded-xl bg-blue-50/60 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-800 space-y-4">
            <h4 className="text-xs font-bold text-blue-950 dark:text-blue-200 flex items-center gap-1.5">
              <Sparkles className="w-4 h-4 text-blue-600 dark:text-blue-400" /> Batch Copywriting Settings
            </h4>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Shared Tone</label>
                <select
                  value={tone}
                  onChange={(e) => setTone(e.target.value)}
                  className="w-full px-3 py-1.5 text-xs rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white"
                >
                  <option value="Professional">Professional</option>
                  <option value="Premium / Luxury">Premium / Luxury</option>
                  <option value="Friendly">Friendly</option>
                  <option value="Minimal">Minimal</option>
                  <option value="Technical">Technical</option>
                  <option value="Playful">Playful</option>
                  <option value="Eco-conscious">Eco-conscious</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Target Language</label>
                <select
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  className="w-full px-3 py-1.5 text-xs rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white"
                >
                  <option value="English">English</option>
                  <option value="Spanish">Spanish</option>
                  <option value="French">French</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Word Count</label>
                <select
                  value={wordCount}
                  onChange={(e) => setWordCount(e.target.value)}
                  className="w-full px-3 py-1.5 text-xs rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white"
                >
                  <option value="Short">Short (40-60 words)</option>
                  <option value="Medium">Medium (80-120 words)</option>
                  <option value="Long">Long (150-200 words)</option>
                </select>
              </div>
            </div>

            <button
              onClick={() => onStartGeneration({ tone, language, word_count_preference: wordCount })}
              disabled={isProcessing}
              className="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-bold shadow-md flex items-center justify-center gap-2 cursor-pointer"
            >
              <Play className="w-4 h-4" /> Start Batch AI Generation ({job.total_products} products)
            </button>
          </div>
        )}
      </div>

      {/* Itemized Table */}
      {job.items && job.items.length > 0 && (
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-sm overflow-hidden">
          <div className="px-5 py-3.5 bg-slate-50 dark:bg-slate-800/80 border-b border-slate-200 dark:border-slate-800 font-bold text-xs text-slate-700 dark:text-slate-300">
            Batch Items Details
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-100/60 dark:bg-slate-800/40 text-slate-500 border-b border-slate-200 dark:border-slate-800 font-semibold uppercase tracking-wider">
                <tr>
                  <th className="px-4 py-3">Row #</th>
                  <th className="px-4 py-3">Product ID</th>
                  <th className="px-4 py-3">Status</th>
                  <th className="px-4 py-3">Details / Errors</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                {job.items.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-800/30">
                    <td className="px-4 py-3 font-mono text-slate-500">#{item.row_number}</td>
                    <td className="px-4 py-3 font-medium text-slate-900 dark:text-white">
                      {item.product_id ? `Product #${item.product_id}` : 'Unassigned'}
                    </td>
                    <td className="px-4 py-3">
                      <StatusBadge status={item.status} size="sm" />
                    </td>
                    <td className="px-4 py-3 text-slate-600 dark:text-slate-400">
                      {item.error_message ? (
                        <span className="text-rose-600 dark:text-rose-400 font-semibold flex items-center gap-1">
                          <AlertTriangle className="w-3.5 h-3.5 shrink-0" /> {item.error_message}
                        </span>
                      ) : item.status === 'completed' ? (
                        <span className="text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
                          <CheckCircle2 className="w-3.5 h-3.5" /> Description Generated & Saved
                        </span>
                      ) : (
                        'Awaiting processing...'
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
