import React, { useState } from 'react';
import { ProductForm } from '../components/generation/ProductForm';
import { ResultCard } from '../components/generation/ResultCard';
import { Product, GeneratedContent } from '../types';
import { generationApi } from '../api';
import {
  Wand2,
  Sparkles,
  CheckCircle,
  Cpu,
  Layers,
  ArrowRight,
  ShieldCheck,
  Zap,
  Split,
  Eye
} from 'lucide-react';

export const GeneratePage: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<GeneratedContent | null>(null);
  const [currentProduct, setCurrentProduct] = useState<Product | null>(null);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 3500);
  };

  const handleGenerate = async (
    product: Product,
    options: { tone: string; language: string; word_count_preference: string; engine: string }
  ) => {
    setIsLoading(true);
    setCurrentProduct(product);
    try {
      const res = await generationApi.generateDescription({
        product,
        tone: options.tone,
        language: options.language,
        word_count_preference: options.word_count_preference,
        engine: options.engine,
        save_to_catalog: true,
      });

      setResult(res.generated_content);
      showToast('🎉 Perfect description evaluated & generated!');
    } catch (err: any) {
      alert(`Generation failed: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleApprove = async (id: number) => {
    try {
      const updated = await generationApi.approveContent(id);
      setResult(updated);
      showToast('✅ Description approved and pushed to catalog!');
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleNeedsReview = async (id: number) => {
    try {
      const updated = await generationApi.markNeedsReview(id);
      setResult(updated);
      showToast('⚠️ Marked for compliance review.');
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleUpdate = async (id: number, update: Partial<GeneratedContent>) => {
    try {
      const updated = await generationApi.updateContent(id, update);
      setResult(updated);
      showToast('💾 Copy changes saved successfully!');
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleRegenerate = async () => {
    if (!result?.id || !result?.product_id) return;
    setIsLoading(true);
    try {
      const updated = await generationApi.regenerateDescription({
        product_id: result.product_id,
        content_id: result.id,
        tone: result.tone,
        language: result.language,
        word_count_preference: result.word_count_preference,
      });
      setResult(updated);
      showToast('🔄 Copy re-evaluated and refreshed!');
    } catch (err: any) {
      alert(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-300 relative">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed top-20 right-6 z-50 flex items-center gap-2.5 px-4 py-3 rounded-2xl bg-slate-900/95 dark:bg-slate-800 text-white text-xs font-bold shadow-2xl border border-slate-700 backdrop-blur-md animate-in fade-in slide-in-from-top-3">
          <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Hero Header & Workflow Stepper */}
      <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="p-1.5 rounded-xl bg-gradient-to-tr from-blue-600 to-cyan-500 text-white shadow-xs">
                <Wand2 className="w-4 h-4" />
              </span>
              <h1 className="text-lg sm:text-xl font-black text-slate-900 dark:text-white tracking-tight">
                Dual-AI Copywriting Studio
              </h1>
            </div>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              Input retail attributes, benchmark Claude 3.5 Sonnet against Gemini 3.5 Lite, and receive optimal copy.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-blue-50 dark:bg-blue-950/70 text-blue-700 dark:text-blue-300 border border-blue-200/80 dark:border-blue-800/80">
              <Zap className="w-3.5 h-3.5 text-cyan-500" />
              Zero-Shot Quality Scoring
            </span>
          </div>
        </div>

        {/* Visual Stepper Tracker */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-3 border-t border-slate-100 dark:border-slate-800 text-xs font-semibold">
          <div className={`p-3 rounded-xl border flex items-center gap-2.5 transition-all ${
            !result
              ? 'border-blue-500 bg-blue-50/70 dark:bg-blue-950/40 text-blue-900 dark:text-blue-200 ring-1 ring-blue-500/20'
              : 'border-slate-200 dark:border-slate-800 text-slate-500 dark:text-slate-400'
          }`}>
            <span className="h-6 w-6 rounded-lg bg-blue-600 text-white font-bold flex items-center justify-center text-xs shrink-0">1</span>
            <div>
              <div className="font-bold text-slate-900 dark:text-white">Structured Input</div>
              <div className="text-[10px] text-slate-500 dark:text-slate-400">Attributes & Keywords</div>
            </div>
          </div>

          <div className={`p-3 rounded-xl border flex items-center gap-2.5 transition-all ${
            isLoading
              ? 'border-cyan-500 bg-cyan-50/70 dark:bg-cyan-950/40 text-cyan-900 dark:text-cyan-200 ring-1 ring-cyan-500/20'
              : 'border-slate-200 dark:border-slate-800 text-slate-500 dark:text-slate-400'
          }`}>
            <span className="h-6 w-6 rounded-lg bg-cyan-600 text-white font-bold flex items-center justify-center text-xs shrink-0">2</span>
            <div>
              <div className="font-bold text-slate-900 dark:text-white">Dual-AI Arbiter</div>
              <div className="text-[10px] text-slate-500 dark:text-slate-400">Claude vs. Gemini Arena</div>
            </div>
          </div>

          <div className={`p-3 rounded-xl border flex items-center gap-2.5 transition-all ${
            result
              ? 'border-emerald-500 bg-emerald-50/70 dark:bg-emerald-950/40 text-emerald-900 dark:text-emerald-200 ring-1 ring-emerald-500/20'
              : 'border-slate-200 dark:border-slate-800 text-slate-500 dark:text-slate-400'
          }`}>
            <span className="h-6 w-6 rounded-lg bg-emerald-600 text-white font-bold flex items-center justify-center text-xs shrink-0">3</span>
            <div>
              <div className="font-bold text-slate-900 dark:text-white">Storefront Preview</div>
              <div className="text-[10px] text-slate-500 dark:text-slate-400">Approve & Catalog Push</div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Form & Results Workspace Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column: Input Form */}
        <div className="lg:col-span-6 space-y-6">
          <ProductForm onGenerate={handleGenerate} isLoading={isLoading} />
        </div>

        {/* Right Column: Results & Interactive Preview */}
        <div className="lg:col-span-6 space-y-6">
          {result ? (
            <ResultCard
              content={result}
              onApprove={handleApprove}
              onNeedsReview={handleNeedsReview}
              onUpdate={handleUpdate}
              onRegenerate={handleRegenerate}
            />
          ) : (
            <div className="rounded-2xl border border-dashed border-slate-300 dark:border-slate-700 bg-white/60 dark:bg-slate-900/60 p-10 text-center flex flex-col items-center justify-center space-y-4 min-h-[460px] shadow-sm">
              <div className="h-16 w-16 rounded-2xl bg-gradient-to-tr from-blue-600/10 via-indigo-600/10 to-cyan-500/10 border border-blue-500/20 flex items-center justify-center text-blue-600 dark:text-cyan-400 animate-float">
                <Sparkles className="w-8 h-8" />
              </div>

              <div className="space-y-1.5 max-w-sm">
                <h3 className="text-base font-extrabold text-slate-900 dark:text-white">
                  Awaiting Product Input
                </h3>
                <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                  Select a <strong>1-Click Demo Profile</strong> on the left or enter custom product specs to start generation.
                </p>
              </div>

              {/* Informational feature badges */}
              <div className="grid grid-cols-2 gap-2 text-left pt-3 w-full max-w-md">
                <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/80 text-xs">
                  <div className="font-bold text-slate-900 dark:text-white flex items-center gap-1.5 mb-1">
                    <Split className="w-3.5 h-3.5 text-blue-500" /> Model Arena
                  </div>
                  <p className="text-[10px] text-slate-500 dark:text-slate-400">
                    Auto-evaluates both Claude and Gemini to pick the strongest copy.
                  </p>
                </div>

                <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/80 text-xs">
                  <div className="font-bold text-slate-900 dark:text-white flex items-center gap-1.5 mb-1">
                    <Eye className="w-3.5 h-3.5 text-cyan-500" /> Storefront Preview
                  </div>
                  <p className="text-[10px] text-slate-500 dark:text-slate-400">
                    See exactly how descriptions look on a real retail storefront.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
