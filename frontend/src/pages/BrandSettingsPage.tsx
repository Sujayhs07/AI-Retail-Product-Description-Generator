import React, { useState, useEffect } from 'react';
import { settingsApi } from '../api';
import { BrandSettings } from '../types';
import { Sliders, Save, RotateCcw, Code, Sparkles, Check, Plus, X, Cpu, Scale } from 'lucide-react';

export const BrandSettingsPage: React.FC = () => {
  const [settings, setSettings] = useState<BrandSettings | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);

  // Dynamic Tags Input
  const [preferredInput, setPreferredInput] = useState('');
  const [prohibitedInput, setProhibitedInput] = useState('');

  useEffect(() => {
    settingsApi
      .getBrandSettings()
      .then(setSettings)
      .finally(() => setIsLoading(false));
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!settings) return;
    setIsSaving(true);
    try {
      const updated = await settingsApi.updateBrandSettings(settings);
      setSettings(updated);
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
    } catch (err: any) {
      alert(`Save error: ${err.message}`);
    } finally {
      setIsSaving(false);
    }
  };

  const handleReset = async () => {
    if (confirm('Reset brand settings to default rules?')) {
      setIsLoading(true);
      try {
        const res = await settingsApi.resetBrandSettings();
        setSettings(res);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const addPreferred = () => {
    if (preferredInput.trim() && settings) {
      setSettings({ ...settings, preferred_words: [...settings.preferred_words, preferredInput.trim()] });
      setPreferredInput('');
    }
  };

  const removePreferred = (idx: number) => {
    if (settings) {
      setSettings({ ...settings, preferred_words: settings.preferred_words.filter((_, i) => i !== idx) });
    }
  };

  const addProhibited = () => {
    if (prohibitedInput.trim() && settings) {
      setSettings({ ...settings, prohibited_words: [...settings.prohibited_words, prohibitedInput.trim()] });
      setProhibitedInput('');
    }
  };

  const removeProhibited = (idx: number) => {
    if (settings) {
      setSettings({ ...settings, prohibited_words: settings.prohibited_words.filter((_, i) => i !== idx) });
    }
  };

  if (isLoading || !settings) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400">
        <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  // System Prompt Preview Text
  const promptPreview = `You are CatalogCraft AI, an expert e-commerce copywriter for ${settings.brand_name}.

CRITICAL BRAND VOICE & COMPLIANCE RULES:
- Brand Voice: ${settings.brand_voice}
- Prohibited Terms (STRICT PENALTY IF USED): ${settings.prohibited_words.join(', ') || 'None'}
- Preferred Vocabulary: ${settings.preferred_words.join(', ') || 'None'}
- Mandatory Legal Disclaimer: ${settings.mandatory_disclaimer || 'None'}
- Keyword Policy: ${settings.keyword_policy} (Max ${settings.max_keywords} keywords)
- Promotional Claims Permitted: ${settings.allow_promotional_claims ? 'Yes' : 'No (Strict factual focus)'}
- Include Feature Bullets: ${settings.include_feature_bullets ? 'Yes' : 'No'}
`;

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Title Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200 dark:border-slate-800">
        <div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <Sliders className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            Brand Voice & Content Rules Configuration
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Configure enterprise vocabulary, prohibited terms, legal disclaimers, and default copywriting constraints
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={handleReset}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 hover:bg-slate-100 rounded-lg transition-colors cursor-pointer"
          >
            <RotateCcw className="w-3.5 h-3.5" /> Reset Defaults
          </button>
        </div>
      </div>

      <form onSubmit={handleSave} className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column: Form Settings */}
        <div className="lg:col-span-7 space-y-6">
          <div className="p-5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
              1. Brand Identity & Voice
            </h3>

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Brand Name
                </label>
                <input
                  type="text"
                  value={settings.brand_name}
                  onChange={(e) => setSettings({ ...settings, brand_name: e.target.value })}
                  className="w-full px-3 py-2 text-sm rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                  Brand Voice Description
                </label>
                <textarea
                  rows={3}
                  value={settings.brand_voice}
                  onChange={(e) => setSettings({ ...settings, brand_voice: e.target.value })}
                  className="w-full px-3 py-2 text-sm rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white outline-none"
                />
              </div>
            </div>
          </div>

          <div className="p-5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
              2. Vocabulary Guardrails
            </h3>

            {/* Preferred Words */}
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Preferred Vocabulary / Phrases
              </label>
              <div className="flex gap-2 mb-2">
                <input
                  type="text"
                  placeholder="e.g. innovative, sustainable"
                  value={preferredInput}
                  onChange={(e) => setPreferredInput(e.target.value)}
                  onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addPreferred(); } }}
                  className="flex-1 px-3 py-1.5 text-xs rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white outline-none"
                />
                <button
                  type="button"
                  onClick={addPreferred}
                  className="px-3 py-1.5 bg-blue-600 text-white rounded-lg text-xs font-bold flex items-center gap-1"
                >
                  <Plus className="w-3.5 h-3.5" /> Add
                </button>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {settings.preferred_words.map((w, i) => (
                  <span key={i} className="inline-flex items-center gap-1 px-2.5 py-1 rounded text-xs font-medium bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800">
                    {w}
                    <button type="button" onClick={() => removePreferred(i)} className="hover:text-rose-500">
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                ))}
              </div>
            </div>

            {/* Prohibited Words */}
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Prohibited Words / Banned Phrases
              </label>
              <div className="flex gap-2 mb-2">
                <input
                  type="text"
                  placeholder="e.g. cheap, guaranteed #1"
                  value={prohibitedInput}
                  onChange={(e) => setProhibitedInput(e.target.value)}
                  onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addProhibited(); } }}
                  className="flex-1 px-3 py-1.5 text-xs rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white outline-none"
                />
                <button
                  type="button"
                  onClick={addProhibited}
                  className="px-3 py-1.5 bg-rose-600 text-white rounded-lg text-xs font-bold flex items-center gap-1"
                >
                  <Plus className="w-3.5 h-3.5" /> Add
                </button>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {settings.prohibited_words.map((w, i) => (
                  <span key={i} className="inline-flex items-center gap-1 px-2.5 py-1 rounded text-xs font-medium bg-rose-50 dark:bg-rose-950/60 text-rose-700 dark:text-rose-300 border border-rose-200 dark:border-rose-800">
                    {w}
                    <button type="button" onClick={() => removeProhibited(i)} className="hover:text-rose-500">
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Mandatory Legal Disclaimer
              </label>
              <input
                type="text"
                value={settings.mandatory_disclaimer || ''}
                onChange={(e) => setSettings({ ...settings, mandatory_disclaimer: e.target.value })}
                className="w-full px-3 py-2 text-xs rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white outline-none"
              />
            </div>
          </div>

          <div className="p-5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
              3. Default Controls & Flags
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Default Tone</label>
                <select
                  value={settings.default_tone}
                  onChange={(e) => setSettings({ ...settings, default_tone: e.target.value })}
                  className="w-full p-2 text-xs rounded border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white"
                >
                  <option value="Professional">Professional</option>
                  <option value="Premium / Luxury">Premium / Luxury</option>
                  <option value="Friendly">Friendly</option>
                  <option value="Minimal">Minimal</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Default Word Count</label>
                <select
                  value={settings.default_word_count}
                  onChange={(e) => setSettings({ ...settings, default_word_count: e.target.value })}
                  className="w-full p-2 text-xs rounded border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white"
                >
                  <option value="Short">Short (40-60)</option>
                  <option value="Medium">Medium (80-120)</option>
                  <option value="Long">Long (150-200)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Max Keywords</label>
                <input
                  type="number"
                  value={settings.max_keywords}
                  onChange={(e) => setSettings({ ...settings, max_keywords: Number(e.target.value) })}
                  className="w-full p-2 text-xs rounded border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white"
                />
              </div>
            </div>

            <div className="flex flex-col gap-2 pt-2 text-xs">
              <label className="flex items-center gap-2 text-slate-700 dark:text-slate-300 font-semibold cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.allow_promotional_claims}
                  onChange={(e) => setSettings({ ...settings, allow_promotional_claims: e.target.checked })}
                  className="accent-blue-600 rounded h-4 w-4"
                />
                Allow Promotional Claims (Disables strict factual enforcement warning)
              </label>

              <label className="flex items-center gap-2 text-slate-700 dark:text-slate-300 font-semibold cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.include_feature_bullets}
                  onChange={(e) => setSettings({ ...settings, include_feature_bullets: e.target.checked })}
                  className="accent-blue-600 rounded h-4 w-4"
                />
                Always generate structured Key Highlights bullet list
              </label>
            </div>
          </div>

          <button
            type="submit"
            disabled={isSaving}
            className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm rounded-xl shadow-lg flex items-center justify-center gap-2 cursor-pointer transition-all"
          >
            {savedSuccess ? (
              <>
                <Check className="w-4 h-4 text-emerald-300" /> Settings Saved!
              </>
            ) : (
              <>
                <Save className="w-4 h-4" /> Save Brand Voice Rules
              </>
            )}
          </button>
        </div>

        {/* Right Column: Live System Prompt Inspector */}
        <div className="lg:col-span-5 space-y-6">
          <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-950 text-slate-100 p-5 shadow-sm space-y-3 font-mono">
            <div className="flex items-center justify-between pb-2 border-b border-slate-800">
              <span className="text-xs font-bold text-cyan-400 flex items-center gap-1.5">
                <Code className="w-4 h-4" /> Live AI System Prompt Preview
              </span>
              <span className="text-[10px] text-slate-500">Auto-assembled</span>
            </div>
            <pre className="text-[11px] leading-relaxed whitespace-pre-wrap text-slate-300 overflow-x-auto max-h-[350px]">
              {promptPreview}
            </pre>
          </div>

          {/* AI Providers Overview Card */}
          <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-sm space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <Scale className="w-4 h-4 text-blue-500" /> Multi-Model Evaluation Engine
            </h4>
            <div className="space-y-2 text-xs">
              <div className="p-3 rounded-lg border border-purple-200/80 dark:border-purple-800/60 bg-purple-50/50 dark:bg-purple-950/30 flex items-start gap-2.5">
                <Cpu className="w-4 h-4 text-purple-600 dark:text-purple-400 shrink-0 mt-0.5" />
                <div>
                  <div className="font-bold text-slate-900 dark:text-white flex items-center gap-1.5">
                    Anthropic Claude
                    <span className="text-[10px] px-1.5 py-0.2 rounded font-mono bg-purple-100 dark:bg-purple-900/60 text-purple-700 dark:text-purple-300">claude-3-5-sonnet</span>
                  </div>
                  <p className="text-[11px] text-slate-600 dark:text-slate-400 mt-0.5">
                    Focuses on natural brand voice narrative, sensory detail, and nuanced guardrail compliance.
                  </p>
                </div>
              </div>

              <div className="p-3 rounded-lg border border-cyan-200/80 dark:border-cyan-800/60 bg-cyan-50/50 dark:bg-cyan-950/30 flex items-start gap-2.5">
                <Sparkles className="w-4 h-4 text-cyan-600 dark:text-cyan-400 shrink-0 mt-0.5" />
                <div>
                  <div className="font-bold text-slate-900 dark:text-white flex items-center gap-1.5">
                    Google Gemini
                    <span className="text-[10px] px-1.5 py-0.2 rounded font-mono bg-cyan-100 dark:bg-cyan-900/60 text-cyan-700 dark:text-cyan-300">gemini-2.5-flash-lite</span>
                  </div>
                  <p className="text-[11px] text-slate-600 dark:text-slate-400 mt-0.5">
                    Focuses on high-speed structured attributes, razor-sharp SEO titles, and crisp conversion hooks.
                  </p>
                </div>
              </div>
            </div>
            <p className="text-[11px] text-slate-500 dark:text-slate-400 italic">
              When generating descriptions, the Dual-AI Arbiter evaluates both models across Completeness, SEO, Readability, and Brand Tone to decide and deliver the perfect description.
            </p>
          </div>
        </div>

      </form>
    </div>
  );
};
