import React, { useState, useEffect } from 'react';
import { GeneratedContent, CandidateOutput } from '../../types';
import { QualityScorePanel } from './QualityScorePanel';
import { StatusBadge } from '../common/StatusBadge';
import { downloadFile } from '../../lib/utils';
import {
  Copy,
  Check,
  Download,
  Edit2,
  Save,
  CheckCircle,
  AlertCircle,
  RefreshCw,
  Cpu,
  Sparkles,
  Tag,
  Trophy,
  Scale,
  Split,
  X,
  CheckCheck,
  ShoppingBag,
  Star,
  Eye,
  FileText,
  Sliders,
  Share2,
  Zap
} from 'lucide-react';

interface ResultCardProps {
  content: GeneratedContent;
  onApprove?: (id: number) => void;
  onNeedsReview?: (id: number) => void;
  onUpdate?: (id: number, update: Partial<GeneratedContent>) => void;
  onRegenerate?: () => void;
}

export const ResultCard: React.FC<ResultCardProps> = ({
  content,
  onApprove,
  onNeedsReview,
  onUpdate,
  onRegenerate,
}) => {
  const [copiedField, setCopiedField] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [viewMode, setViewMode] = useState<'structured' | 'storefront' | 'arena'>('structured');
  const [showCompareModal, setShowCompareModal] = useState(false);

  // Editable Form State
  const [title, setTitle] = useState(content.title);
  const [shortDesc, setShortDesc] = useState(content.short_description);
  const [fullDesc, setFullDesc] = useState(content.full_description);
  const [metaTitle, setMetaTitle] = useState(content.meta_title);
  const [metaDesc, setMetaDesc] = useState(content.meta_description);

  // Candidates & Decision State
  const candidates: CandidateOutput[] = content.candidates_data || [];
  const winningIdx = candidates.findIndex((c) => c.is_winner);
  const [viewedCandidateIdx, setViewedCandidateIdx] = useState<number>(winningIdx >= 0 ? winningIdx : 0);

  useEffect(() => {
    setTitle(content.title);
    setShortDesc(content.short_description);
    setFullDesc(content.full_description);
    setMetaTitle(content.meta_title);
    setMetaDesc(content.meta_description);
    if (content.candidates_data && content.candidates_data.length > 0) {
      const idx = content.candidates_data.findIndex((c) => c.is_winner);
      setViewedCandidateIdx(idx >= 0 ? idx : 0);
    }
  }, [content]);

  const copyToClipboard = (text: string, fieldName: string) => {
    navigator.clipboard.writeText(text);
    setCopiedField(fieldName);
    setTimeout(() => setCopiedField(null), 2000);
  };

  const copyAll = () => {
    const fullText = `
TITLE:
${title}

SHORT DESCRIPTION:
${shortDesc}

FULL DESCRIPTION:
${fullDesc}

KEY HIGHLIGHTS:
${(content.highlights || []).map((h) => `- ${h}`).join('\n')}

SEO META TITLE:
${metaTitle}

SEO META DESCRIPTION:
${metaDesc}
    `.trim();

    copyToClipboard(fullText, 'all');
  };

  const handleSave = () => {
    if (content.id && onUpdate) {
      onUpdate(content.id, {
        title,
        short_description: shortDesc,
        full_description: fullDesc,
        meta_title: metaTitle,
        meta_description: metaDesc,
      });
    }
    setIsEditing(false);
  };

  const handleAdoptCandidate = (cand: CandidateOutput) => {
    setTitle(cand.content.title);
    setShortDesc(cand.content.short_description);
    setFullDesc(cand.content.full_description);
    setMetaTitle(cand.content.meta_title);
    setMetaDesc(cand.content.meta_description);
    if (content.id && onUpdate) {
      onUpdate(content.id, {
        title: cand.content.title,
        short_description: cand.content.short_description,
        full_description: cand.content.full_description,
        highlights: cand.content.highlights,
        meta_title: cand.content.meta_title,
        meta_description: cand.content.meta_description,
        suggested_keywords: cand.content.suggested_keywords,
        warnings: cand.content.warnings,
        seo_score: cand.scores.seo_score,
        readability_score: cand.scores.readability_score,
        brand_tone_score: cand.scores.brand_tone_score,
        quality_score: cand.scores.quality_score,
      });
    }
  };

  const handleDownloadTxt = () => {
    const text = `${title}\n\n${shortDesc}\n\n${fullDesc}\n\nHighlights:\n${(content.highlights || []).map((h) => `- ${h}`).join('\n')}`;
    downloadFile(text, `${title.toLowerCase().replace(/\s+/g, '_')}_copy.txt`, 'txt');
  };

  const handleDownloadMd = () => {
    const md = `# ${title}\n\n> ${shortDesc}\n\n## Overview\n${fullDesc}\n\n### Key Highlights\n${(content.highlights || []).map((h) => `- ${h}`).join('\n')}\n\n### SEO Metadata\n- **Title:** ${metaTitle}\n- **Description:** ${metaDesc}\n- **Keywords:** ${(content.suggested_keywords || []).join(', ')}`;
    downloadFile(md, `${title.toLowerCase().replace(/\s+/g, '_')}_copy.md`, 'md');
  };

  const handleDownloadJson = () => {
    downloadFile(JSON.stringify(content, null, 2), `${title.toLowerCase().replace(/\s+/g, '_')}_copy.json`, 'json');
  };

  const hasDualCandidates = candidates.length >= 2;
  const currentCandidate = candidates[viewedCandidateIdx];

  return (
    <div className="space-y-6">
      {/* 🏆 Dual AI Decision Arena Banner */}
      {content.decision_rationale && (
        <div className="rounded-2xl border border-blue-200/90 dark:border-blue-800/80 bg-gradient-to-br from-blue-50/90 via-indigo-50/40 to-white dark:from-blue-950/40 dark:via-slate-900 dark:to-slate-900 p-5 shadow-sm space-y-3.5">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <span className="p-1.5 rounded-xl bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20 shadow-2xs">
                <Trophy className="w-4 h-4" />
              </span>
              <div>
                <h3 className="text-xs font-black uppercase tracking-wider text-slate-900 dark:text-white flex items-center gap-1.5">
                  Dual-AI Arbiter Decided Winner
                </h3>
                <p className="text-[10px] text-slate-500 dark:text-slate-400">
                  Anthropic Claude 3.5 Sonnet vs. Google Gemini 3.5 Lite
                </p>
              </div>
            </div>

            {hasDualCandidates && (
              <button
                type="button"
                onClick={() => setShowCompareModal(true)}
                className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-bold text-blue-700 dark:text-blue-300 bg-white dark:bg-slate-800 border border-blue-200 dark:border-blue-700 hover:bg-blue-50 dark:hover:bg-slate-700 rounded-xl transition-all cursor-pointer shadow-2xs hover:scale-102"
              >
                <Split className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400" />
                Head-to-Head Benchmark
              </button>
            )}
          </div>

          <p className="text-xs text-slate-700 dark:text-slate-300 leading-relaxed bg-white/80 dark:bg-slate-900/80 p-3.5 rounded-xl border border-blue-100 dark:border-blue-900/60 shadow-2xs">
            {content.decision_rationale}
          </p>

          {/* Interactive Candidate Tabs */}
          {hasDualCandidates && (
            <div className="space-y-2 pt-1">
              <div className="text-[11px] font-bold text-slate-600 dark:text-slate-400 flex items-center gap-1.5">
                <Scale className="w-3.5 h-3.5 text-blue-500" />
                Inspect Evaluated Model Outputs:
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                {candidates.map((cand, idx) => {
                  const isSelected = idx === viewedCandidateIdx;
                  const isClaude = cand.provider === 'anthropic';
                  return (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => setViewedCandidateIdx(idx)}
                      className={`p-3.5 rounded-2xl border text-left transition-all cursor-pointer flex items-center justify-between ${
                        isSelected
                          ? isClaude
                            ? 'border-purple-500 bg-purple-50/90 dark:bg-purple-950/40 ring-2 ring-purple-500/25 shadow-sm'
                            : 'border-cyan-500 bg-cyan-50/90 dark:bg-cyan-950/40 ring-2 ring-cyan-500/25 shadow-sm'
                          : 'border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 bg-white/90 dark:bg-slate-850'
                      }`}
                    >
                      <div className="flex items-center gap-2.5">
                        {isClaude ? (
                          <div className="p-2 rounded-xl bg-purple-100 dark:bg-purple-950 text-purple-700 dark:text-purple-300">
                            <Cpu className="w-4 h-4 shrink-0" />
                          </div>
                        ) : (
                          <div className="p-2 rounded-xl bg-cyan-100 dark:bg-cyan-950 text-cyan-700 dark:text-cyan-300">
                            <Sparkles className="w-4 h-4 shrink-0" />
                          </div>
                        )}
                        <div>
                          <div className="text-xs font-bold text-slate-900 dark:text-white flex items-center gap-1.5">
                            {cand.provider_label}
                            {cand.is_winner && (
                              <span className="text-[9px] px-1.5 py-0.5 rounded-full font-black bg-amber-100 dark:bg-amber-900/80 text-amber-800 dark:text-amber-300 flex items-center gap-0.5 shadow-2xs">
                                <Trophy className="w-2.5 h-2.5" /> Winner
                              </span>
                            )}
                          </div>
                          <div className="text-[10px] text-slate-500 dark:text-slate-400 mt-0.5">
                            SEO: {cand.scores.seo_score} • Readability: {cand.scores.readability_score} • Voice: {cand.scores.brand_tone_score}
                          </div>
                        </div>
                      </div>

                      <div className="text-right">
                        <div className="text-xs font-black text-slate-900 dark:text-white">
                          {cand.scores.quality_score}
                          <span className="text-[10px] text-slate-400 font-normal">/100</span>
                        </div>
                        <span className="text-[10px] text-blue-600 dark:text-blue-400 font-bold">
                          {isSelected ? 'Active' : 'Inspect'}
                        </span>
                      </div>
                    </button>
                  );
                })}
              </div>

              {/* Notice & Adopt button if viewing non-active candidate */}
              {currentCandidate && currentCandidate.content.title !== title && (
                <div className="flex items-center justify-between p-3 rounded-xl bg-blue-100/70 dark:bg-blue-950/70 border border-blue-200 dark:border-blue-800/80 text-xs">
                  <span className="text-blue-900 dark:text-blue-200 text-xs font-medium">
                    Viewing <strong>{currentCandidate.provider_label}</strong> alternative draft copy.
                  </span>
                  <button
                    type="button"
                    onClick={() => handleAdoptCandidate(currentCandidate)}
                    className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg text-xs flex items-center gap-1.5 cursor-pointer transition-colors shadow-sm"
                  >
                    <CheckCheck className="w-3.5 h-3.5" /> Adopt This Version
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Quality Score Breakdown */}
      <QualityScorePanel
        qualityScore={content.quality_score}
        completenessScore={content.completeness_score}
        seoScore={content.seo_score}
        readabilityScore={content.readability_score}
        brandToneScore={content.brand_tone_score}
        warnings={content.warnings}
      />

      {/* Interactive Main Content Card */}
      <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-md overflow-hidden">
        {/* Card Header & View Mode Switcher */}
        <div className="flex flex-wrap items-center justify-between gap-3 p-4 bg-slate-50/80 dark:bg-slate-850 border-b border-slate-200 dark:border-slate-800">
          {/* View Mode Tabs */}
          <div className="flex items-center gap-1 bg-slate-200/80 dark:bg-slate-800 p-1 rounded-xl">
            <button
              type="button"
              onClick={() => setViewMode('structured')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                viewMode === 'structured'
                  ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-xs'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              <FileText className="w-3.5 h-3.5" />
              <span>Copy Editor</span>
            </button>
            <button
              type="button"
              onClick={() => setViewMode('storefront')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                viewMode === 'storefront'
                  ? 'bg-white dark:bg-slate-700 text-blue-600 dark:text-blue-400 shadow-xs'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              <Eye className="w-3.5 h-3.5 text-blue-500" />
              <span>Live Storefront Preview</span>
            </button>
          </div>

          {/* Quick Action Toolbar */}
          <div className="flex flex-wrap items-center gap-2">
            <button
              onClick={copyAll}
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-bold text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-750 transition-colors cursor-pointer shadow-2xs"
            >
              {copiedField === 'all' ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
              {copiedField === 'all' ? 'Copied All!' : 'Copy All'}
            </button>

            <button
              onClick={handleDownloadMd}
              className="flex items-center gap-1 px-2.5 py-1.5 text-xs font-semibold text-slate-600 dark:text-slate-300 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl hover:bg-slate-100 transition-colors cursor-pointer shadow-2xs"
              title="Download Markdown"
            >
              <Download className="w-3.5 h-3.5" /> .MD
            </button>

            <button
              onClick={handleDownloadJson}
              className="flex items-center gap-1 px-2.5 py-1.5 text-xs font-semibold text-slate-600 dark:text-slate-300 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl hover:bg-slate-100 transition-colors cursor-pointer shadow-2xs"
              title="Download JSON"
            >
              <Download className="w-3.5 h-3.5" /> .JSON
            </button>

            {isEditing ? (
              <button
                onClick={handleSave}
                className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-xl shadow-sm transition-colors cursor-pointer"
              >
                <Save className="w-3.5 h-3.5" /> Save Changes
              </button>
            ) : (
              <button
                onClick={() => setIsEditing(true)}
                className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-bold text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl hover:bg-slate-100 transition-colors cursor-pointer shadow-2xs"
              >
                <Edit2 className="w-3.5 h-3.5" /> Edit
              </button>
            )}
          </div>
        </div>

        {/* View Mode: Live Storefront Mockup */}
        {viewMode === 'storefront' ? (
          <div className="p-6 sm:p-8 bg-slate-50/50 dark:bg-slate-950/40 space-y-6">
            <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 shadow-sm space-y-6">
              {/* Fake eCommerce Breadcrumb */}
              <div className="text-[11px] text-slate-400 flex items-center gap-2 border-b border-slate-100 dark:border-slate-800 pb-3">
                <span>Home</span>
                <span>/</span>
                <span>Catalog</span>
                <span>/</span>
                <span className="text-slate-700 dark:text-slate-300 font-medium truncate max-w-xs">{title}</span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-12 gap-8">
                {/* Storefront Image */}
                <div className="md:col-span-5 space-y-3">
                  <div className="aspect-square rounded-2xl bg-slate-100 dark:bg-slate-800 overflow-hidden border border-slate-200 dark:border-slate-700 flex items-center justify-center">
                    <img
                      src="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=600&q=80"
                      alt="Storefront Preview"
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div className="grid grid-cols-3 gap-2">
                    <div className="h-16 rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 overflow-hidden">
                      <img src="https://images.unsplash.com/photo-1544441893-675973e31985?auto=format&fit=crop&w=200&q=80" alt="Thumb" className="w-full h-full object-cover" />
                    </div>
                    <div className="h-16 rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 overflow-hidden">
                      <img src="https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?auto=format&fit=crop&w=200&q=80" alt="Thumb" className="w-full h-full object-cover" />
                    </div>
                    <div className="h-16 rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 overflow-hidden flex items-center justify-center text-xs font-bold text-slate-400">
                      +4 More
                    </div>
                  </div>
                </div>

                {/* Storefront PDP Copy */}
                <div className="md:col-span-7 space-y-4">
                  <div>
                    <div className="flex items-center gap-1.5 text-amber-500 mb-1.5">
                      {[...Array(5)].map((_, i) => (
                        <Star key={i} className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
                      ))}
                      <span className="text-xs font-bold text-slate-700 dark:text-slate-300 ml-1">4.9 / 5.0</span>
                      <span className="text-xs text-slate-400">(142 verified shopper reviews)</span>
                    </div>

                    <h1 className="text-xl sm:text-2xl font-black text-slate-900 dark:text-white tracking-tight leading-snug">
                      {title}
                    </h1>
                  </div>

                  <div className="p-3 rounded-xl bg-blue-50/60 dark:bg-blue-950/30 border border-blue-200/60 dark:border-blue-900/40">
                    <p className="text-xs font-semibold text-blue-900 dark:text-blue-200 italic">
                      "{shortDesc}"
                    </p>
                  </div>

                  {/* Price & Stock */}
                  <div className="flex items-center gap-3">
                    <span className="text-2xl font-black text-slate-900 dark:text-white">$199.99</span>
                    <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-300">
                      In Stock • Ready to Ship
                    </span>
                  </div>

                  {/* Highlights Bullet List */}
                  {content.highlights && content.highlights.length > 0 && (
                    <div className="space-y-2 pt-2">
                      <span className="text-xs font-bold text-slate-900 dark:text-white uppercase tracking-wider">
                        Key Product Highlights
                      </span>
                      <ul className="space-y-1.5 text-xs text-slate-700 dark:text-slate-300">
                        {content.highlights.map((h, i) => (
                          <li key={i} className="flex items-start gap-2">
                            <Sparkles className="w-3.5 h-3.5 text-blue-500 shrink-0 mt-0.5" />
                            <span>{h}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Full Description Accordion */}
                  <div className="pt-2">
                    <span className="text-xs font-bold text-slate-900 dark:text-white uppercase tracking-wider block mb-1.5">
                      Full Narrative Description
                    </span>
                    <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed whitespace-pre-line">
                      {fullDesc}
                    </p>
                  </div>

                  {/* Fake Buy Button */}
                  <div className="pt-4 flex gap-3">
                    <button
                      type="button"
                      className="flex-1 py-3 bg-slate-900 dark:bg-white text-white dark:text-slate-900 font-extrabold rounded-xl text-xs flex items-center justify-center gap-2 cursor-pointer shadow-md"
                    >
                      <ShoppingBag className="w-4 h-4" /> Add to Shopping Cart
                    </button>
                    <button
                      type="button"
                      className="px-4 py-3 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold rounded-xl text-xs hover:bg-slate-200 cursor-pointer"
                    >
                      Wishlist
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ) : (
          /* View Mode: Structured Copy & Metadata Editor */
          <div className="p-6 space-y-6">
            {/* Generated Title */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="text-xs font-bold uppercase tracking-wider text-slate-400">
                  Product Headline Title
                </label>
                <div className="flex items-center gap-2">
                  <span className={`text-[10px] font-mono font-bold ${title.length >= 30 && title.length <= 65 ? 'text-emerald-500' : 'text-slate-400'}`}>
                    {title.length} / 60 chars optimal
                  </span>
                  <button
                    onClick={() => copyToClipboard(title, 'title')}
                    className="text-xs text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1 cursor-pointer"
                  >
                    {copiedField === 'title' ? <Check className="w-3 h-3 text-emerald-500" /> : <Copy className="w-3 h-3" />}
                    Copy
                  </button>
                </div>
              </div>
              {isEditing ? (
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="w-full p-3 text-base font-bold rounded-xl border border-blue-500 bg-blue-50/20 dark:bg-blue-950/30 text-slate-900 dark:text-white outline-none"
                />
              ) : (
                <h2 className="text-lg font-black text-slate-900 dark:text-white leading-snug">
                  {title}
                </h2>
              )}
            </div>

            {/* Short Description */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="text-xs font-bold uppercase tracking-wider text-slate-400">
                  Short Description (Hook & Overview)
                </label>
                <button
                  onClick={() => copyToClipboard(shortDesc, 'shortDesc')}
                  className="text-xs text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1 cursor-pointer"
                >
                  {copiedField === 'shortDesc' ? <Check className="w-3 h-3 text-emerald-500" /> : <Copy className="w-3 h-3" />}
                  Copy
                </button>
              </div>
              {isEditing ? (
                <textarea
                  rows={2}
                  value={shortDesc}
                  onChange={(e) => setShortDesc(e.target.value)}
                  className="w-full p-3 text-sm rounded-xl border border-blue-500 bg-blue-50/20 dark:bg-blue-950/30 text-slate-900 dark:text-white outline-none"
                />
              ) : (
                <p className="text-sm text-slate-700 dark:text-slate-300 font-medium italic bg-slate-50 dark:bg-slate-800/60 p-3.5 rounded-xl border border-slate-100 dark:border-slate-800">
                  "{shortDesc}"
                </p>
              )}
            </div>

            {/* Full Description */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="text-xs font-bold uppercase tracking-wider text-slate-400">
                  Full Narrative Description
                </label>
                <button
                  onClick={() => copyToClipboard(fullDesc, 'fullDesc')}
                  className="text-xs text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1 cursor-pointer"
                >
                  {copiedField === 'fullDesc' ? <Check className="w-3 h-3 text-emerald-500" /> : <Copy className="w-3 h-3" />}
                  Copy
                </button>
              </div>
              {isEditing ? (
                <textarea
                  rows={5}
                  value={fullDesc}
                  onChange={(e) => setFullDesc(e.target.value)}
                  className="w-full p-3 text-sm rounded-xl border border-blue-500 bg-blue-50/20 dark:bg-blue-950/30 text-slate-900 dark:text-white outline-none"
                />
              ) : (
                <p className="text-sm text-slate-800 dark:text-slate-200 leading-relaxed whitespace-pre-line bg-white dark:bg-slate-900">
                  {fullDesc}
                </p>
              )}
            </div>

            {/* Highlights */}
            {content.highlights && content.highlights.length > 0 && (
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                  Key Feature Highlights
                </label>
                <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                  {content.highlights.map((h, i) => (
                    <li key={i} className="flex items-start gap-2.5 text-xs font-semibold text-slate-800 dark:text-slate-200 bg-slate-50 dark:bg-slate-800/50 p-2.5 rounded-xl border border-slate-100 dark:border-slate-800 shadow-2xs">
                      <Sparkles className="w-4 h-4 text-cyan-500 shrink-0 mt-0.5" />
                      <span>{h}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Meta Tags */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 p-4.5 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700">
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-xs font-bold text-slate-700 dark:text-slate-300">SEO Meta Title</span>
                  <span className="text-[10px] font-mono text-slate-400">({metaTitle.length} chars)</span>
                </div>
                {isEditing ? (
                  <input
                    type="text"
                    value={metaTitle}
                    onChange={(e) => setMetaTitle(e.target.value)}
                    className="w-full p-2.5 text-xs rounded-xl border border-blue-500 bg-white dark:bg-slate-900 text-slate-900 dark:text-white outline-none"
                  />
                ) : (
                  <p className="text-xs text-blue-700 dark:text-blue-400 font-bold">{metaTitle}</p>
                )}
              </div>

              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-xs font-bold text-slate-700 dark:text-slate-300">SEO Meta Description</span>
                  <span className="text-[10px] font-mono text-slate-400">({metaDesc.length} chars)</span>
                </div>
                {isEditing ? (
                  <textarea
                    rows={2}
                    value={metaDesc}
                    onChange={(e) => setMetaDesc(e.target.value)}
                    className="w-full p-2.5 text-xs rounded-xl border border-blue-500 bg-white dark:bg-slate-900 text-slate-900 dark:text-white outline-none"
                  />
                ) : (
                  <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">{metaDesc}</p>
                )}
              </div>
            </div>

            {/* Suggested Keywords */}
            {content.suggested_keywords && content.suggested_keywords.length > 0 && (
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-1.5">
                  Suggested Catalog Keywords
                </label>
                <div className="flex flex-wrap gap-1.5">
                  {content.suggested_keywords.map((kw, i) => (
                    <span key={i} className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-bold bg-cyan-50 dark:bg-cyan-950/60 text-cyan-700 dark:text-cyan-300 border border-cyan-200/80 dark:border-cyan-800/80">
                      <Tag className="w-3 h-3" /> {kw}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Footer Actions */}
        <div className="flex flex-wrap items-center justify-between gap-3 p-4 bg-slate-50 dark:bg-slate-850 border-t border-slate-200 dark:border-slate-800">
          <div className="flex items-center gap-2">
            {content.id && onApprove && (
              <button
                onClick={() => onApprove(content.id!)}
                className="flex items-center gap-1.5 px-4 py-2.5 text-xs font-extrabold text-white bg-emerald-600 hover:bg-emerald-700 rounded-xl shadow-md transition-all cursor-pointer"
              >
                <CheckCircle className="w-3.5 h-3.5" /> Approve & Push to Catalog
              </button>
            )}

            {content.id && onNeedsReview && (
              <button
                onClick={() => onNeedsReview(content.id!)}
                className="flex items-center gap-1.5 px-3 py-2.5 text-xs font-bold text-amber-800 dark:text-amber-300 bg-amber-100 dark:bg-amber-950/60 border border-amber-300 dark:border-amber-800 hover:bg-amber-200 rounded-xl transition-colors cursor-pointer"
              >
                <AlertCircle className="w-3.5 h-3.5" /> Flag For Review
              </button>
            )}
          </div>

          {onRegenerate && (
            <button
              onClick={onRegenerate}
              className="flex items-center gap-1.5 px-4 py-2 text-xs font-bold text-blue-700 dark:text-blue-300 bg-blue-50 dark:bg-blue-950/50 border border-blue-300 dark:border-blue-800 hover:bg-blue-100 rounded-xl transition-colors cursor-pointer"
            >
              <RefreshCw className="w-3.5 h-3.5" /> Regenerate Output
            </button>
          )}
        </div>
      </div>

      {/* Head-to-Head Comparison Modal */}
      {showCompareModal && hasDualCandidates && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/75 backdrop-blur-md animate-in fade-in duration-150">
          <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-2xl max-w-4xl w-full max-h-[90vh] flex flex-col overflow-hidden">
            <div className="flex items-center justify-between p-5 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-850">
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-xl bg-blue-600 text-white shadow-sm">
                  <Split className="w-4 h-4" />
                </div>
                <div>
                  <h3 className="text-sm font-black text-slate-900 dark:text-white">
                    Anthropic Claude 3.5 vs. Google Gemini 3.5 Lite Arena
                  </h3>
                  <p className="text-[11px] text-slate-500 dark:text-slate-400">
                    Direct side-by-side quality benchmark across retail SEO and brand compliance
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setShowCompareModal(false)}
                className="p-2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6 overflow-y-auto space-y-6">
              {/* Score Matrix */}
              <div className="grid grid-cols-2 gap-4">
                {candidates.map((cand, i) => (
                  <div
                    key={i}
                    className={`p-4 rounded-2xl border ${
                      cand.is_winner
                        ? 'border-amber-400 dark:border-amber-600 bg-amber-50/40 dark:bg-amber-950/20'
                        : 'border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-850'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-2">
                        {cand.provider === 'anthropic' ? (
                          <Cpu className="w-4 h-4 text-purple-600 dark:text-purple-400" />
                        ) : (
                          <Sparkles className="w-4 h-4 text-cyan-600 dark:text-cyan-400" />
                        )}
                        <span className="text-xs font-bold text-slate-900 dark:text-white">
                          {cand.provider_label}
                        </span>
                      </div>
                      {cand.is_winner && (
                        <span className="text-[10px] font-black px-2 py-0.5 rounded-full bg-amber-100 text-amber-800 dark:bg-amber-900/80 dark:text-amber-300 flex items-center gap-1">
                          <Trophy className="w-3 h-3" /> Winner
                        </span>
                      )}
                    </div>

                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div className="p-2.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
                        <span className="text-[10px] text-slate-400 block font-semibold">Overall Quality</span>
                        <span className="text-sm font-black text-slate-900 dark:text-white">
                          {cand.scores.quality_score}/100
                        </span>
                      </div>
                      <div className="p-2.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
                        <span className="text-[10px] text-slate-400 block font-semibold">SEO Rating</span>
                        <span className="text-sm font-black text-blue-600 dark:text-blue-400">
                          {cand.scores.seo_score}/100
                        </span>
                      </div>
                      <div className="p-2.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
                        <span className="text-[10px] text-slate-400 block font-semibold">Readability</span>
                        <span className="text-sm font-black text-emerald-600 dark:text-emerald-400">
                          {cand.scores.readability_score}/100
                        </span>
                      </div>
                      <div className="p-2.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
                        <span className="text-[10px] text-slate-400 block font-semibold">Brand Tone</span>
                        <span className="text-sm font-black text-purple-600 dark:text-purple-400">
                          {cand.scores.brand_tone_score}/100
                        </span>
                      </div>
                    </div>

                    <button
                      type="button"
                      onClick={() => {
                        handleAdoptCandidate(cand);
                        setShowCompareModal(false);
                      }}
                      className="mt-3.5 w-full py-2.5 bg-slate-900 hover:bg-slate-800 dark:bg-white dark:hover:bg-slate-100 text-white dark:text-slate-900 font-bold text-xs rounded-xl transition-all cursor-pointer flex items-center justify-center gap-1.5 shadow-sm"
                    >
                      <CheckCheck className="w-3.5 h-3.5" /> Adopt This Candidate
                    </button>
                  </div>
                ))}
              </div>

              {/* Side-by-Side Text Comparison */}
              <div className="space-y-4">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                  Detailed Copy & Metadata Comparison
                </h4>

                <div className="grid grid-cols-2 gap-4">
                  {candidates.map((cand, i) => (
                    <div key={i} className="space-y-3 p-4.5 rounded-2xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-700">
                      <div>
                        <span className="text-[10px] font-bold uppercase text-slate-400 block">Title</span>
                        <h5 className="text-xs font-bold text-slate-900 dark:text-white mt-0.5">
                          {cand.content.title}
                        </h5>
                      </div>

                      <div>
                        <span className="text-[10px] font-bold uppercase text-slate-400 block">Short Description</span>
                        <p className="text-xs text-slate-700 dark:text-slate-300 italic mt-0.5">
                          "{cand.content.short_description}"
                        </p>
                      </div>

                      <div>
                        <span className="text-[10px] font-bold uppercase text-slate-400 block">Full Description</span>
                        <p className="text-xs text-slate-700 dark:text-slate-300 leading-relaxed mt-0.5 whitespace-pre-line line-clamp-6">
                          {cand.content.full_description}
                        </p>
                      </div>

                      <div>
                        <span className="text-[10px] font-bold uppercase text-slate-400 block">SEO Meta Snippet</span>
                        <p className="text-[11px] font-bold text-blue-600 dark:text-blue-400 mt-0.5">
                          {cand.content.meta_title}
                        </p>
                        <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
                          {cand.content.meta_description}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="p-4 border-t border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-850 flex justify-end">
              <button
                type="button"
                onClick={() => setShowCompareModal(false)}
                className="px-4 py-2 bg-slate-200 dark:bg-slate-700 hover:bg-slate-300 dark:hover:bg-slate-600 text-slate-800 dark:text-white text-xs font-bold rounded-xl transition-colors cursor-pointer"
              >
                Close Arena
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
