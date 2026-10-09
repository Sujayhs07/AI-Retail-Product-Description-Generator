import React, { useState, useEffect } from 'react';
import { GeneratedContent, CandidateOutput } from '../../types';
import { QualityScorePanel } from './QualityScorePanel';
import { ScoreBadge } from '../common/ScoreBadge';
import { downloadFile } from '../../lib/utils';
import {
  Copy,
  Check,
  Download,
  Edit2,
  Save,
  CheckCircle,
  AlertCircle,
  AlertTriangle,
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
  Zap,
  ThumbsUp,
  ShieldCheck,
  Search,
  BookOpen,
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
  const [activeTab, setActiveTab] = useState<'comparison' | 'editor' | 'storefront'>('comparison');
  const [dismissNotice, setDismissNotice] = useState(false);

  // Editable Form State (for currently active / adopted version)
  const [title, setTitle] = useState(content.title || '');
  const [shortDesc, setShortDesc] = useState(content.short_description || '');
  const [fullDesc, setFullDesc] = useState(content.full_description || '');
  const [metaTitle, setMetaTitle] = useState(content.meta_title || '');
  const [metaDesc, setMetaDesc] = useState(content.meta_description || '');

  // Candidates & Dual Decision State
  const candidates: CandidateOutput[] = Array.isArray(content.candidates_data) ? content.candidates_data : [];
  const hasDualCandidates = candidates.length >= 2;

  // Track which candidate is approved / active
  const [approvedCandidateProvider, setApprovedCandidateProvider] = useState<string | null>(
    content.status === 'Approved' ? content.generation_source || null : null
  );

  useEffect(() => {
    setTitle(content.title || '');
    setShortDesc(content.short_description || '');
    setFullDesc(content.full_description || '');
    setMetaTitle(content.meta_title || '');
    setMetaDesc(content.meta_description || '');
    if (content.status === 'Approved') {
      setApprovedCandidateProvider(content.generation_source || null);
    }
  }, [content]);

  const copyToClipboard = (text: string, fieldName: string) => {
    if (!text) return;
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

  // Directly approve a chosen candidate (Claude or Gemini)
  const handleApproveCandidate = (cand: CandidateOutput) => {
    setTitle(cand.content.title);
    setShortDesc(cand.content.short_description);
    setFullDesc(cand.content.full_description);
    setMetaTitle(cand.content.meta_title);
    setMetaDesc(cand.content.meta_description);
    setApprovedCandidateProvider(cand.provider);

    if (content.id && onUpdate) {
      onUpdate(content.id, {
        title: cand.content.title,
        short_description: cand.content.short_description,
        full_description: cand.content.full_description,
        highlights: cand.content.highlights || [],
        meta_title: cand.content.meta_title || '',
        meta_description: cand.content.meta_description || '',
        suggested_keywords: cand.content.suggested_keywords || [],
        warnings: cand.content.warnings || [],
        seo_score: cand.scores?.seo_score ?? 0,
        readability_score: cand.scores?.readability_score ?? 0,
        completeness_score: cand.scores?.completeness_score ?? 0,
        brand_tone_score: cand.scores?.brand_tone_score ?? 0,
        quality_score: cand.scores?.quality_score ?? 0,
        status: 'Approved',
        generation_source: cand.provider,
      });
    } else if (content.id && onApprove) {
      onApprove(content.id);
    }
  };

  // Adopt candidate into editor without immediately approving
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
        highlights: cand.content.highlights || [],
        meta_title: cand.content.meta_title || '',
        meta_description: cand.content.meta_description || '',
        suggested_keywords: cand.content.suggested_keywords || [],
        warnings: cand.content.warnings || [],
        seo_score: cand.scores?.seo_score ?? 0,
        readability_score: cand.scores?.readability_score ?? 0,
        completeness_score: cand.scores?.completeness_score ?? 0,
        brand_tone_score: cand.scores?.brand_tone_score ?? 0,
        quality_score: cand.scores?.quality_score ?? 0,
        generation_source: cand.provider,
      });
    }
    setActiveTab('editor');
  };

  const handleDownloadTxt = () => {
    const text = `${title}\n\n${shortDesc}\n\n${fullDesc}\n\nHighlights:\n${(content.highlights || []).map((h) => `- ${h}`).join('\n')}`;
    downloadFile(text, `${(title || 'product').toLowerCase().replace(/\s+/g, '_')}_copy.txt`, 'txt');
  };

  const handleDownloadMd = () => {
    const md = `# ${title}\n\n> ${shortDesc}\n\n## Overview\n${fullDesc}\n\n### Key Highlights\n${(content.highlights || []).map((h) => `- ${h}`).join('\n')}\n\n### SEO Metadata\n- **Title:** ${metaTitle}\n- **Description:** ${metaDesc}\n- **Keywords:** ${(content.suggested_keywords || []).join(', ')}`;
    downloadFile(md, `${(title || 'product').toLowerCase().replace(/\s+/g, '_')}_copy.md`, 'md');
  };

  const handleDownloadJson = () => {
    downloadFile(JSON.stringify(content, null, 2), `${(title || 'product').toLowerCase().replace(/\s+/g, '_')}_copy.json`, 'json');
  };

  return (
    <div className="space-y-6">
      {/* API Key Missing & Mock Generator Active Notice Banner */}
      {(content.api_key_notice?.is_missing ||
        content.generation_source === 'mock' ||
        content.generation_source === 'dual_decided_mock' ||
        candidates.some((c) => c.source === 'mock')) && !dismissNotice && (
        <div className="rounded-2xl border border-amber-300 dark:border-amber-700/80 bg-gradient-to-r from-amber-50 via-orange-50/40 to-amber-50 dark:from-amber-950/40 dark:via-orange-950/20 dark:to-amber-950/30 p-4 shadow-sm flex items-start justify-between gap-3 animate-in fade-in">
          <div className="flex items-start gap-3">
            <div className="p-2 rounded-xl bg-amber-500/20 text-amber-700 dark:text-amber-300 shrink-0 mt-0.5">
              <AlertTriangle className="w-4 h-4" />
            </div>
            <div className="space-y-1">
              <h4 className="text-xs font-black uppercase tracking-wider text-amber-900 dark:text-amber-200 flex items-center gap-1.5">
                API Key Empty Notice: Offline Mock Generator Used
              </h4>
              <p className="text-xs text-amber-800 dark:text-amber-300 leading-relaxed">
                {content.api_key_notice?.message || 'API key is not configured in backend/.env. Switched to offline Deterministic Mock Generator.'}{' '}
                All SEO tags, keywords, and 4-dimensional quality scores are computed deterministically. To enable live Claude 3.5 Sonnet or Gemini 2.5 Flash Lite calls, configure your API keys in <code className="px-1 py-0.5 rounded bg-amber-200/60 dark:bg-amber-900/60 font-mono text-[10px]">backend/.env</code>.
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={() => setDismissNotice(true)}
            className="p-1 rounded-lg text-amber-600 dark:text-amber-400 hover:bg-amber-100 dark:hover:bg-amber-900/50 cursor-pointer shrink-0"
            title="Dismiss notice"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* ============================================================== */}
      {/* 1. DUAL AI DECIDER HEADER & RATIONALE BANNER                  */}
      {/* ============================================================== */}
      {hasDualCandidates ? (
        <div className="rounded-2xl border border-blue-200/90 dark:border-blue-800/80 bg-gradient-to-br from-blue-50/90 via-indigo-50/40 to-white dark:from-blue-950/40 dark:via-slate-900 dark:to-slate-900 p-5 shadow-sm space-y-3.5">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-2.5">
              <span className="p-2 rounded-xl bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20 shadow-2xs">
                <Trophy className="w-4 h-4" />
              </span>
              <div>
                <h3 className="text-xs font-black uppercase tracking-wider text-slate-900 dark:text-white flex items-center gap-1.5">
                  Dual-AI Arbiter Arena: Claude vs. Gemini
                </h3>
                <p className="text-[11px] text-slate-500 dark:text-slate-400">
                  Both models generated complete descriptions. Review both below and approve the winner for your catalog.
                </p>
              </div>
            </div>

            {/* View Mode Switcher */}
            <div className="flex items-center gap-1 bg-white/90 dark:bg-slate-800 p-1 rounded-xl border border-slate-200 dark:border-slate-700 shadow-2xs">
              <button
                type="button"
                onClick={() => setActiveTab('comparison')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                  activeTab === 'comparison'
                    ? 'bg-blue-600 text-white shadow-xs'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                }`}
              >
                <Split className="w-3.5 h-3.5" />
                <span>Dual Comparison</span>
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('editor')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                  activeTab === 'editor'
                    ? 'bg-blue-600 text-white shadow-xs'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                }`}
              >
                <FileText className="w-3.5 h-3.5" />
                <span>Copy Editor</span>
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('storefront')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                  activeTab === 'storefront'
                    ? 'bg-blue-600 text-white shadow-xs'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                }`}
              >
                <Eye className="w-3.5 h-3.5" />
                <span>Storefront Preview</span>
              </button>
            </div>
          </div>

          {content.decision_rationale && (
            <div className="p-3.5 rounded-xl bg-white/90 dark:bg-slate-900/90 border border-blue-100 dark:border-blue-900/60 shadow-2xs text-xs text-slate-700 dark:text-slate-300 leading-relaxed">
              <div className="font-bold text-slate-900 dark:text-white mb-1 flex items-center gap-1.5">
                <Scale className="w-3.5 h-3.5 text-blue-500" />
                <span>Arbiter Decision Rationale:</span>
              </div>
              <p>{content.decision_rationale}</p>
            </div>
          )}
        </div>
      ) : (
        /* Single AI Mode Banner */
        <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 shadow-sm flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2.5">
            <span className="p-2 rounded-xl bg-blue-100 dark:bg-blue-950 text-blue-600 dark:text-blue-400">
              <Cpu className="w-4 h-4" />
            </span>
            <div>
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-900 dark:text-white">
                Generated via {content.generation_source === 'anthropic' ? 'Anthropic Claude 3.5 Sonnet' : content.generation_source === 'gemini' ? 'Google Gemini' : 'AI Engine'}
              </h3>
              <p className="text-[11px] text-slate-500 dark:text-slate-400">
                AI Description generated and scored across all retail dimensions.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-1 bg-slate-100 dark:bg-slate-800 p-1 rounded-xl">
            <button
              type="button"
              onClick={() => setActiveTab('editor')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                activeTab === 'editor' || activeTab === 'comparison'
                  ? 'bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-xs'
                  : 'text-slate-600 dark:text-slate-400'
              }`}
            >
              <FileText className="w-3.5 h-3.5" />
              <span>Copy Editor</span>
            </button>
            <button
              type="button"
              onClick={() => setActiveTab('storefront')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                activeTab === 'storefront'
                  ? 'bg-white dark:bg-slate-700 text-blue-600 dark:text-blue-400 shadow-xs'
                  : 'text-slate-600 dark:text-slate-400'
              }`}
            >
              <Eye className="w-3.5 h-3.5" />
              <span>Storefront</span>
            </button>
          </div>
        </div>
      )}

      {/* ============================================================== */}
      {/* 2. TAB A: DUAL CANDIDATE COMPARISON (SHOW BOTH & APPROVE)      */}
      {/* ============================================================== */}
      {hasDualCandidates && activeTab === 'comparison' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="text-xs font-extrabold uppercase tracking-wider text-slate-700 dark:text-slate-300 flex items-center gap-2">
              <Split className="w-4 h-4 text-blue-500" />
              Compare Descriptions & Choose Version to Approve
            </h4>
            <span className="text-[11px] text-slate-500 dark:text-slate-400">
              Click <strong>Approve & Add to Catalog</strong> on your preferred model
            </span>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {candidates.map((cand, idx) => {
              const isClaude = cand.provider === 'anthropic';
              const isApprovedThis = (content.status === 'Approved' && approvedCandidateProvider === cand.provider) ||
                                     (content.status === 'Approved' && title === cand.content.title);
              const isCurrentlyViewed = title === cand.content.title;

              return (
                <div
                  key={idx}
                  className={`rounded-2xl border-2 transition-all p-5 flex flex-col justify-between space-y-4 shadow-sm ${
                    isClaude
                      ? 'border-purple-300 dark:border-purple-800/80 bg-gradient-to-b from-purple-50/30 to-white dark:from-purple-950/20 dark:to-slate-900'
                      : 'border-cyan-300 dark:border-cyan-800/80 bg-gradient-to-b from-cyan-50/30 to-white dark:from-cyan-950/20 dark:to-slate-900'
                  } ${isApprovedThis ? 'ring-2 ring-emerald-500 shadow-md' : ''}`}
                >
                  <div className="space-y-4">
                    {/* Header: Model Badge & Winner tag */}
                    <div className="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-slate-800">
                      <div className="flex items-center gap-2.5">
                        <div
                          className={`p-2 rounded-xl text-white ${
                            isClaude ? 'bg-purple-600' : 'bg-cyan-600'
                          }`}
                        >
                          {isClaude ? <Cpu className="w-4 h-4" /> : <Sparkles className="w-4 h-4" />}
                        </div>
                        <div>
                          <div className="text-sm font-black text-slate-900 dark:text-white flex items-center gap-1.5">
                            {cand.provider_label}
                          </div>
                          <div className="text-[10px] text-slate-500 dark:text-slate-400 font-mono">
                            Model: {cand.model}
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center gap-1.5">
                        {cand.is_winner && (
                          <span className="text-[10px] font-black px-2 py-0.5 rounded-full bg-amber-100 text-amber-800 dark:bg-amber-900/80 dark:text-amber-300 flex items-center gap-1 shadow-2xs">
                            <Trophy className="w-3 h-3 text-amber-500" />
                            Arbiter Pick
                          </span>
                        )}
                        {isApprovedThis && (
                          <span className="text-[10px] font-black px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 dark:bg-emerald-900/80 dark:text-emerald-300 flex items-center gap-1 shadow-2xs">
                            <Check className="w-3 h-3 text-emerald-600" />
                            Approved
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Scores Matrix */}
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                      <div className="p-2 rounded-xl bg-white dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/80">
                        <span className="text-[9px] text-slate-400 block font-semibold">Quality</span>
                        <span className="text-xs font-black text-slate-900 dark:text-white">
                          {(cand.scores?.quality_score ?? 0).toFixed(0)}/100
                        </span>
                      </div>
                      <div className="p-2 rounded-xl bg-white dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/80">
                        <span className="text-[9px] text-slate-400 block font-semibold">SEO</span>
                        <span className="text-xs font-black text-blue-600 dark:text-blue-400">
                          {(cand.scores?.seo_score ?? 0).toFixed(0)}/100
                        </span>
                      </div>
                      <div className="p-2 rounded-xl bg-white dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/80">
                        <span className="text-[9px] text-slate-400 block font-semibold">Readability</span>
                        <span className="text-xs font-black text-purple-600 dark:text-purple-400">
                          {(cand.scores?.readability_score ?? 0).toFixed(0)}/100
                        </span>
                      </div>
                      <div className="p-2 rounded-xl bg-white dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/80">
                        <span className="text-[9px] text-slate-400 block font-semibold">Brand Tone</span>
                        <span className="text-xs font-black text-cyan-600 dark:text-cyan-400">
                          {(cand.scores?.brand_tone_score ?? 0).toFixed(0)}/100
                        </span>
                      </div>
                    </div>

                    {/* Strengths Pills */}
                    {cand.strengths && cand.strengths.length > 0 && (
                      <div className="flex flex-wrap gap-1">
                        {cand.strengths.map((str, sIdx) => (
                          <span
                            key={sIdx}
                            className="text-[10px] font-medium px-2 py-0.5 rounded-md bg-white/80 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300"
                          >
                            ✓ {str}
                          </span>
                        ))}
                      </div>
                    )}

                    {/* Headline Title */}
                    <div className="space-y-1">
                      <div className="flex items-center justify-between">
                        <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                          Headline Title
                        </label>
                        <button
                          type="button"
                          onClick={() => copyToClipboard(cand.content.title, `cand-title-${idx}`)}
                          className="text-[11px] text-blue-600 hover:underline flex items-center gap-1 cursor-pointer"
                        >
                          {copiedField === `cand-title-${idx}` ? <Check className="w-3 h-3 text-emerald-500" /> : <Copy className="w-3 h-3" />}
                          Copy
                        </button>
                      </div>
                      <h4 className="text-sm font-black text-slate-900 dark:text-white leading-snug">
                        {cand.content.title}
                      </h4>
                    </div>

                    {/* Short Description */}
                    <div className="space-y-1">
                      <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                        Short Hook Description
                      </label>
                      <p className="text-xs text-slate-700 dark:text-slate-300 italic p-3 rounded-xl bg-white/90 dark:bg-slate-800/80 border border-slate-200/80 dark:border-slate-700/80">
                        "{cand.content.short_description}"
                      </p>
                    </div>

                    {/* Full Description */}
                    <div className="space-y-1">
                      <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                        Full Narrative Description
                      </label>
                      <div className="text-xs text-slate-800 dark:text-slate-200 leading-relaxed max-h-48 overflow-y-auto p-3 rounded-xl bg-white dark:bg-slate-850 border border-slate-200 dark:border-slate-700 whitespace-pre-line">
                        {cand.content.full_description}
                      </div>
                    </div>

                    {/* Highlights */}
                    {cand.content.highlights && cand.content.highlights.length > 0 && (
                      <div className="space-y-1">
                        <label className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                          Highlights Bullets ({cand.content.highlights.length})
                        </label>
                        <ul className="space-y-1">
                          {cand.content.highlights.slice(0, 3).map((h, hIdx) => (
                            <li key={hIdx} className="text-xs text-slate-700 dark:text-slate-300 flex items-start gap-1.5">
                              <span className="text-blue-500 font-bold">•</span>
                              <span>{h}</span>
                            </li>
                          ))}
                          {cand.content.highlights.length > 3 && (
                            <li className="text-[10px] text-slate-400 italic">
                              +{cand.content.highlights.length - 3} more highlights
                            </li>
                          )}
                        </ul>
                      </div>
                    )}

                    {/* SEO Meta Tags */}
                    <div className="p-3 rounded-xl bg-white/70 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700/80 space-y-1 text-xs">
                      <div>
                        <span className="text-[10px] text-slate-400 font-bold uppercase">Meta Title: </span>
                        <span className="text-blue-600 dark:text-blue-400 font-medium">{cand.content.meta_title}</span>
                      </div>
                      <div>
                        <span className="text-[10px] text-slate-400 font-bold uppercase">Meta Desc: </span>
                        <span className="text-slate-600 dark:text-slate-300">{cand.content.meta_description}</span>
                      </div>
                    </div>
                  </div>

                  {/* Candidate Action Buttons */}
                  <div className="pt-3 border-t border-slate-200 dark:border-slate-800 flex flex-col sm:flex-row items-center gap-2">
                    <button
                      type="button"
                      onClick={() => handleApproveCandidate(cand)}
                      className={`w-full py-2.5 px-3 rounded-xl text-xs font-black flex items-center justify-center gap-1.5 cursor-pointer transition-all shadow-md ${
                        isApprovedThis
                          ? 'bg-emerald-600 hover:bg-emerald-700 text-white ring-2 ring-emerald-400/50'
                          : isClaude
                          ? 'bg-purple-600 hover:bg-purple-700 text-white hover:scale-101'
                          : 'bg-cyan-600 hover:bg-cyan-700 text-white hover:scale-101'
                      }`}
                    >
                      <CheckCircle className="w-4 h-4" />
                      <span>{isApprovedThis ? '✓ Approved in Catalog' : `Approve & Add ${isClaude ? 'Claude' : 'Gemini'} Copy`}</span>
                    </button>

                    <button
                      type="button"
                      onClick={() => handleAdoptCandidate(cand)}
                      className="w-full sm:w-auto py-2.5 px-3 rounded-xl text-xs font-bold text-slate-700 dark:text-slate-300 bg-white dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 border border-slate-200 dark:border-slate-700 cursor-pointer transition-colors"
                      title="Open in Copy Editor to tweak"
                    >
                      Edit Copy
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* ============================================================== */}
      {/* 3. QUALITY SCORE BREAKDOWN PANEL                               */}
      {/* ============================================================== */}
      <QualityScorePanel
        qualityScore={content.quality_score ?? 0}
        completenessScore={content.completeness_score ?? 0}
        seoScore={content.seo_score ?? 0}
        readabilityScore={content.readability_score ?? 0}
        brandToneScore={content.brand_tone_score ?? 0}
        warnings={content.warnings || []}
      />

      {/* ============================================================== */}
      {/* 4. TAB B: COPY EDITOR & DETAILS                                */}
      {/* ============================================================== */}
      {activeTab === 'editor' && (
        <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-md overflow-hidden">
          {/* Editor Header Toolbar */}
          <div className="flex flex-wrap items-center justify-between gap-3 p-4 bg-slate-50/80 dark:bg-slate-850 border-b border-slate-200 dark:border-slate-800">
            <div className="flex items-center gap-2">
              <FileText className="w-4 h-4 text-blue-500" />
              <h3 className="text-xs font-extrabold uppercase tracking-wider text-slate-900 dark:text-white">
                Active Catalog Copy Editor
              </h3>
              {content.is_human_edited && (
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300">
                  Human Edited
                </span>
              )}
            </div>

            <div className="flex flex-wrap items-center gap-2">
              <button
                onClick={copyAll}
                className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-bold text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl hover:bg-slate-100 cursor-pointer"
              >
                {copiedField === 'all' ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
                {copiedField === 'all' ? 'Copied All!' : 'Copy All'}
              </button>

              <button
                onClick={handleDownloadMd}
                className="flex items-center gap-1 px-2.5 py-1.5 text-xs font-semibold text-slate-600 dark:text-slate-300 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl hover:bg-slate-100 cursor-pointer"
                title="Download Markdown"
              >
                <Download className="w-3.5 h-3.5" /> .MD
              </button>

              <button
                onClick={handleDownloadJson}
                className="flex items-center gap-1 px-2.5 py-1.5 text-xs font-semibold text-slate-600 dark:text-slate-300 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl hover:bg-slate-100 cursor-pointer"
                title="Download JSON"
              >
                <Download className="w-3.5 h-3.5" /> .JSON
              </button>

              {isEditing ? (
                <button
                  onClick={handleSave}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-xl shadow-sm cursor-pointer"
                >
                  <Save className="w-3.5 h-3.5" /> Save Changes
                </button>
              ) : (
                <button
                  onClick={() => setIsEditing(true)}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-bold text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl hover:bg-slate-100 cursor-pointer"
                >
                  <Edit2 className="w-3.5 h-3.5" /> Edit
                </button>
              )}
            </div>
          </div>

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

          {/* Editor Footer Actions */}
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
      )}

      {/* ============================================================== */}
      {/* 5. TAB C: LIVE STOREFRONT MOCKUP                               */}
      {/* ============================================================== */}
      {activeTab === 'storefront' && (
        <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-md p-6 sm:p-8 space-y-6">
          <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
            <div className="text-[11px] text-slate-400 flex items-center gap-2">
              <span>Home</span>
              <span>/</span>
              <span>Catalog</span>
              <span>/</span>
              <span className="text-slate-700 dark:text-slate-300 font-medium truncate max-w-xs">{title}</span>
            </div>
            <button
              onClick={() => setActiveTab(hasDualCandidates ? 'comparison' : 'editor')}
              className="text-xs text-blue-600 dark:text-blue-400 hover:underline cursor-pointer"
            >
              ← Back to Review
            </button>
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

              {/* Full Description */}
              <div className="pt-2">
                <span className="text-xs font-bold text-slate-900 dark:text-white uppercase tracking-wider block mb-1.5">
                  Full Narrative Description
                </span>
                <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed whitespace-pre-line">
                  {fullDesc}
                </p>
              </div>

              {/* Action Buttons */}
              <div className="pt-4 flex gap-3">
                {content.id && onApprove && (
                  <button
                    type="button"
                    onClick={() => onApprove(content.id!)}
                    className="flex-1 py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-extrabold rounded-xl text-xs flex items-center justify-center gap-2 cursor-pointer shadow-md transition-colors"
                  >
                    <CheckCircle className="w-4 h-4" /> Approve for Live Storefront
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
