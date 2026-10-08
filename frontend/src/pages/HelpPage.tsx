import React from 'react';
import { HelpCircle, BookOpen, Sparkles, FileText, Layers, Download, CheckCircle2 } from 'lucide-react';
import { DemoVideoPlayer } from '../components/common/DemoVideoPlayer';

export const HelpPage: React.FC = () => {
  const steps = [
    {
      step: 'Step 1',
      title: 'Single Product AI Copy Generation',
      desc: 'Navigate to "Generate Description". Click "Load Sample Product" to pre-fill attributes, then click "Generate". Observe the instant copy output, Quality Score, SEO title/meta, and automated missing data warnings.',
    },
    {
      step: 'Step 2',
      title: 'Inline Edit & Approval Workflow',
      desc: 'On the generated result card, click "Edit Content" to adjust text, click "Save", and then click "Approve Description". Verify that the status updates to "Approved" and snapshot versions are created.',
    },
    {
      step: 'Step 3',
      title: 'Batch Generation from CSV/JSON',
      desc: 'Navigate to "Batch Generator". Download the sample CSV or JSON file, upload it back via drag-and-drop, configure a shared tone, and start batch processing.',
    },
    {
      step: 'Step 4',
      title: 'Brand Voice Guardrails Test',
      desc: 'Go to "Brand Voice & Rules". Add a prohibited word like "cheap" or "worst". Try generating copy with that word and observe how the Brand Tone Score drops with an explicit warning.',
    },
    {
      step: 'Step 5',
      title: 'Catalogue Search, Filter & Review',
      desc: 'Navigate to "Product Catalogue". Use the multi-filter bar to search products by category, brand, tone, status, or score range. Open the detail modal to compare original specs side-by-side with generated copy.',
    },
    {
      step: 'Step 6',
      title: 'Dashboard & Analytics',
      desc: 'Inspect the interactive Recharts visualizations on the Dashboard and Analytics pages. Explanatory metrics beneath each chart clarify key business insights and catalog health.',
    },
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Title Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200 dark:border-slate-800">
        <div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <HelpCircle className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            Documentation & Interactive Studio Walkthrough
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Step-by-step user guide and interactive feature walkthrough for CatalogCraft AI
          </p>
        </div>
      </div>

      {/* Interactive Retailer Demo Video Player */}
      <DemoVideoPlayer />

      {/* Demo Script Section */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 text-white shadow-xl border border-blue-800 space-y-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/20 text-cyan-300 text-xs font-bold border border-cyan-400/30">
          <Sparkles className="w-4 h-4 text-cyan-400" /> Interactive Feature Guide
        </div>
        <h2 className="text-xl font-bold">Recommended Studio Evaluation Flow</h2>
        <p className="text-xs text-slate-300 leading-relaxed">
          Follow these 6 steps to explore the full capabilities of CatalogCraft AI—from single generation to batch processing and brand governance.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 pt-2">
          {steps.map((s) => (
            <div key={s.step} className="p-4 rounded-xl bg-slate-950/70 border border-slate-800 space-y-2">
              <span className="text-[10px] font-bold uppercase tracking-wider text-cyan-400">{s.step}</span>
              <h3 className="text-xs font-bold text-white">{s.title}</h3>
              <p className="text-[11px] text-slate-400 leading-relaxed">{s.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Architecture Overview Card */}
      <div className="p-6 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-sm space-y-3">
        <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
          <BookOpen className="w-4 h-4 text-blue-500" /> Architecture & Key Features Summary
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs text-slate-600 dark:text-slate-400">
          <div className="space-y-1.5">
            <h4 className="font-bold text-slate-900 dark:text-white flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" /> Anthropic & Google Gemini Dual-AI Arbiter
            </h4>
            <p>Generates copy candidates using both Anthropic Claude 3.5 Sonnet and Google Gemini 3.5 Lite APIs, benchmarks each candidate across SEO, readability, and brand voice rules, and automatically decides the perfect description.</p>
          </div>
          <div className="space-y-1.5">
            <h4 className="font-bold text-slate-900 dark:text-white flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" /> Transparent Quality Scorer
            </h4>
            <p>Calculates 0-100 quality scores across Completeness, SEO, Readability, and Brand Alignment with actionable copy recommendations.</p>
          </div>
        </div>
      </div>
    </div>
  );
};
