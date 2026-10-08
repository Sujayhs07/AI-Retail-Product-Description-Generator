import React from 'react';
import { ShieldCheck, AlertTriangle, Lock, Eye, FileCheck, CheckCircle2 } from 'lucide-react';

export const ResponsibleAIPage: React.FC = () => {
  const principles = [
    {
      title: 'Human-in-the-Loop Copy Review',
      desc: 'AI-generated product descriptions serve as high-quality drafts. Every description must be reviewed and approved by a human copywriter or merchandiser prior to web publishing.',
      icon: <Eye className="w-5 h-5 text-blue-500" />,
    },
    {
      title: 'Factual Accuracy & Grounding',
      desc: 'The AI model is strictly constrained to the structured product attributes supplied. The system will never hallucinate specs, materials, warranties, certifications, or performance metrics.',
      icon: <FileCheck className="w-5 h-5 text-emerald-500" />,
    },
    {
      title: 'Zero PII & Confidential Data Handling',
      desc: 'This platform processes product specifications only. Customer personal identifiable information (PII), payment credentials, and internal confidential data are strictly excluded.',
      icon: <Lock className="w-5 h-5 text-purple-500" />,
    },
    {
      title: 'Automated Risk & Quality Flags',
      desc: 'Built-in Quality Scorer automatically detects missing attributes, prohibited phrases, and SEO inaccuracies, flagging them in real-time before copy release.',
      icon: <AlertTriangle className="w-5 h-5 text-amber-500" />,
    },
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Title Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200 dark:border-slate-800">
        <div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            Responsible AI & Safety Governance Policy
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Enterprise AI Principles & Omnichannel Retail Copywriting Guardrails
          </p>
        </div>
      </div>

      {/* Banner */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-blue-900 to-indigo-950 text-white shadow-xl border border-blue-800/50 space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/20 text-cyan-300 text-xs font-bold border border-cyan-500/30">
          <ShieldCheck className="w-4 h-4 text-cyan-400" /> Responsible AI Commitment
        </div>
        <h2 className="text-xl font-bold">CatalogCraft AI Safety Principles</h2>
        <p className="text-xs text-slate-300 leading-relaxed max-w-3xl">
          Retail content automation demands strict adherence to truthfulness, regulatory compliance, and brand safety. CatalogCraft AI enforces deterministic grounding and human oversight at every step of the content lifecycle.
        </p>
      </div>

      {/* Principles Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {principles.map((p) => (
          <div
            key={p.title}
            className="p-6 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-sm space-y-3"
          >
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-100 dark:border-slate-700">
                {p.icon}
              </div>
              <h3 className="text-sm font-bold text-slate-900 dark:text-white">{p.title}</h3>
            </div>
            <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              {p.desc}
            </p>
          </div>
        ))}
      </div>

      {/* Enterprise Governance Card */}
      <div className="p-6 rounded-xl border border-blue-200 dark:border-blue-900 bg-blue-50/50 dark:bg-blue-950/30 space-y-3">
        <h3 className="text-sm font-bold text-blue-950 dark:text-blue-200 flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-blue-600 dark:text-blue-400" />
          Enterprise Governance & Retailer Responsibility Statement
        </h3>
        <ul className="space-y-2 text-xs text-blue-900 dark:text-blue-300 list-disc list-inside">
          <li>Pre-configured with enterprise retail product catalogs and dynamic schema validation.</li>
          <li>Product pricing, warranties, safety claims, and legal statements should always be verified by compliance teams before publishing to live e-commerce storefronts.</li>
          <li>The retailer retains full editorial control, version governance, and sign-off authority for all final digital assets.</li>
        </ul>
      </div>
    </div>
  );
};
