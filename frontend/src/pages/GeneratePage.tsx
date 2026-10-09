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
  Eye,
  AlertTriangle,
  KeyRound,
  X
} from 'lucide-react';

export const GeneratePage: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<GeneratedContent | null>(null);
  const [currentProduct, setCurrentProduct] = useState<Product | null>(null);
  const [toastMessage, setToastMessage] = useState<string | null>(null);
  const [toastType, setToastType] = useState<'success' | 'warning'>('success');
  const [isApiKeyModalOpen, setIsApiKeyModalOpen] = useState(false);
  const [apiKeyNoticeData, setApiKeyNoticeData] = useState<{
    missingProviders: string[];
    message?: string;
  } | null>(null);
  const [suppressKeyModal, setSuppressKeyModal] = useState(false);

  const showToast = (msg: string, type: 'success' | 'warning' = 'success') => {
    setToastMessage(msg);
    setToastType(type);
    setTimeout(() => setToastMessage(null), 4000);
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

      const notice = res.generated_content.api_key_notice;
      const isMockSource = res.generated_content.generation_source === 'mock' ||
        res.generated_content.generation_source === 'dual_decided_mock' ||
        (Array.isArray(res.generated_content.candidates_data) &&
          res.generated_content.candidates_data.some((c: any) => c.source === 'mock'));

      if (notice?.is_missing || isMockSource) {
        const providers = notice?.missing_providers && notice.missing_providers.length > 0
          ? notice.missing_providers
          : ['Google Gemini', 'Anthropic Claude'];
        setApiKeyNoticeData({
          missingProviders: providers,
          message: notice?.message || 'API key is empty. Switched to offline Deterministic Mock Generator.',
        });

        if (!suppressKeyModal) {
          setIsApiKeyModalOpen(true);
        }
        showToast('⚠️ API key is empty. Switched to offline Mock Generator.', 'warning');
      } else {
        showToast('🎉 Perfect description evaluated & generated!', 'success');
      }
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
      showToast('⚠️ Marked for compliance review.', 'warning');
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
      if (updated.api_key_notice?.is_missing) {
        showToast('⚠️ API key is empty. Switched to offline Mock Generator.', 'warning');
      } else {
        showToast('🔄 Copy re-evaluated and refreshed!');
      }
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
        <div className={`fixed top-20 right-6 z-50 flex items-center gap-2.5 px-4 py-3 rounded-2xl text-white text-xs font-bold shadow-2xl border backdrop-blur-md animate-in fade-in slide-in-from-top-3 ${
          toastType === 'warning'
            ? 'bg-amber-950/95 border-amber-500/50 text-amber-100'
            : 'bg-slate-900/95 dark:bg-slate-800 border-slate-700'
        }`}>
          {toastType === 'warning' ? (
            <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
          ) : (
            <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
          )}
          <span>{toastMessage}</span>
        </div>
      )}

      {/* API Key Missing / Mock Generator Fallback Modal Popup */}
      {isApiKeyModalOpen && apiKeyNoticeData && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="relative w-full max-w-lg rounded-2xl border border-amber-300 dark:border-amber-700/80 bg-white dark:bg-slate-900 p-6 shadow-2xl space-y-4 animate-in zoom-in-95 duration-200">
            <button
              type="button"
              onClick={() => setIsApiKeyModalOpen(false)}
              className="absolute top-4 right-4 p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-start gap-3.5">
              <div className="p-3 rounded-2xl bg-amber-500/15 border border-amber-500/30 text-amber-600 dark:text-amber-400 shrink-0">
                <KeyRound className="w-6 h-6" />
              </div>
              <div className="space-y-1">
                <h3 className="text-base font-black text-slate-900 dark:text-white">
                  API Key is Empty — Mock Generator Activated
                </h3>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  Fallback option activated so you can test complete copywriting without interruption.
                </p>
              </div>
            </div>

            <div className="p-3.5 rounded-xl bg-amber-50/80 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900/60 text-xs text-amber-900 dark:text-amber-200 space-y-2">
              <p className="leading-relaxed">
                No active API key was found in <code className="px-1.5 py-0.5 rounded bg-amber-100 dark:bg-amber-900/80 font-mono font-bold text-[11px]">backend/.env</code> for:{' '}
                <strong>{apiKeyNoticeData.missingProviders.join(' and ')}</strong>.
              </p>
              <p className="leading-relaxed">
                CatalogCraft automatically activated the <strong>Deterministic Mock Generator</strong> option. Realistic descriptions, SEO tags, bullet points, and 4D quality scores were generated offline without needing cloud API credits.
              </p>
            </div>

            <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 text-xs space-y-1.5">
              <div className="font-bold text-slate-900 dark:text-white flex items-center gap-1.5 text-[11px]">
                <span>Want to use live Google Gemini or Anthropic Claude?</span>
              </div>
              <p className="text-[11px] text-slate-500 dark:text-slate-400">
                Configure your API keys inside <code className="font-mono text-blue-600 dark:text-blue-400">backend/.env</code>:
              </p>
              <pre className="p-2.5 rounded-lg bg-slate-900 text-slate-100 text-[10px] font-mono overflow-x-auto leading-relaxed">
GEMINI_API_KEY=AIzaSy...
ANTHROPIC_API_KEY=sk-ant-api03-...
              </pre>
            </div>

            <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-2">
              <label className="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400 cursor-pointer select-none">
                <input
                  type="checkbox"
                  checked={suppressKeyModal}
                  onChange={(e) => setSuppressKeyModal(e.target.checked)}
                  className="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                />
                <span>Don't show this popup again this session</span>
              </label>

              <button
                type="button"
                onClick={() => setIsApiKeyModalOpen(false)}
                className="w-full sm:w-auto px-5 py-2.5 rounded-xl text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 shadow-md cursor-pointer transition-all"
              >
                Continue with Mock Generator
              </button>
            </div>
          </div>
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
