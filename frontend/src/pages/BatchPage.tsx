import React, { useState } from 'react';
import { FileUploader } from '../components/batch/FileUploader';
import { BatchProgressTracker } from '../components/batch/BatchProgressTracker';
import { batchApi } from '../api';
import { BatchJob } from '../types';
import { Layers, RefreshCw } from 'lucide-react';

export const BatchPage: React.FC = () => {
  const [currentJob, setCurrentJob] = useState<BatchJob | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleFileUpload = async (file: File) => {
    setIsLoading(true);
    try {
      const job = await batchApi.uploadBatchFile(file);
      setCurrentJob(job);
    } catch (err: any) {
      alert(`Upload error: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStartGeneration = async (options: { tone: string; language: string; word_count_preference: string }) => {
    if (!currentJob) return;
    setIsProcessing(true);
    try {
      await batchApi.startBatchGeneration(currentJob.id, options);
      // Refresh Job Status
      const updated = await batchApi.getBatchJob(currentJob.id);
      setCurrentJob(updated);
    } catch (err: any) {
      alert(`Batch processing error: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleRetryFailed = async () => {
    if (!currentJob) return;
    setIsProcessing(true);
    try {
      await batchApi.retryFailedItems(currentJob.id);
      const updated = await batchApi.getBatchJob(currentJob.id);
      setCurrentJob(updated);
    } catch (err: any) {
      alert(`Retry error: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200 dark:border-slate-800">
        <div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <Layers className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            Batch Product Description Generator
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Upload CSV or JSON files to generate hundreds of retail descriptions concurrently
          </p>
        </div>

        {currentJob && (
          <button
            onClick={() => setCurrentJob(null)}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 hover:bg-slate-100 rounded-lg transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" /> Upload New Batch
          </button>
        )}
      </div>

      {!currentJob ? (
        <FileUploader onFileUpload={handleFileUpload} isLoading={isLoading} />
      ) : (
        <BatchProgressTracker
          job={currentJob}
          onStartGeneration={handleStartGeneration}
          onRetryFailed={handleRetryFailed}
          isProcessing={isProcessing}
        />
      )}
    </div>
  );
};
