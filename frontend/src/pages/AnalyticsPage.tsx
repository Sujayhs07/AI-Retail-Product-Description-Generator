import React, { useEffect, useState } from 'react';
import { analyticsApi } from '../api';
import { AnalyticsData } from '../types';
import { StatCard } from '../components/common/StatCard';
import {
  BarChart3,
  Award,
  Sparkles,
  Download,
  Info
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  PieChart,
  Pie,
  Cell
} from 'recharts';

export const AnalyticsPage: React.FC = () => {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [category, setCategory] = useState('All');
  const [brand, setBrand] = useState('All');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    analyticsApi
      .getAnalytics(category !== 'All' ? category : undefined, brand !== 'All' ? brand : undefined)
      .then(setData)
      .finally(() => setIsLoading(false));
  }, [category, brand]);

  if (isLoading || !data) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400">
        <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const { metrics, quality_score_distribution, seo_score_distribution, tone_usage, products_by_category } = data;
  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#06b6d4', '#8b5cf6', '#ec4899'];
  const CATEGORY_PALETTE: Record<string, string> = {
    'Electronics': '#3b82f6',
    'Fashion': '#ec4899',
    'Home and Kitchen': '#f59e0b',
    'Beauty and Personal Care': '#8b5cf6',
    'Sports and Fitness': '#10b981',
    'Furniture': '#6366f1',
    'Grocery': '#14b8a6',
    'Travel Accessories': '#06b6d4',
  };

  const exportAnalyticsJson = () => {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'catalogcraft_analytics.json';
    a.click();
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200 dark:border-slate-800">
        <div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            AI Content Analytics & Performance Reporting
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Deep-dive metrics into SEO strength, readability scores, and catalog copywriting velocity
          </p>
        </div>

        <div className="flex items-center gap-2">
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="px-3 py-1.5 text-xs font-semibold rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white"
          >
            <option value="All">All Categories (8 Verticals)</option>
            <option value="Electronics">Electronics</option>
            <option value="Fashion">Fashion</option>
            <option value="Home and Kitchen">Home and Kitchen</option>
            <option value="Beauty and Personal Care">Beauty and Personal Care</option>
            <option value="Sports and Fitness">Sports and Fitness</option>
            <option value="Furniture">Furniture</option>
            <option value="Grocery">Grocery</option>
            <option value="Travel Accessories">Travel Accessories</option>
          </select>

          <button
            onClick={exportAnalyticsJson}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-bold text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 hover:bg-slate-100 rounded-lg transition-colors"
          >
            <Download className="w-3.5 h-3.5" /> Export Report
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <StatCard
          title="Overall Catalog Quality"
          value={`${metrics.avg_quality_score} / 100`}
          subtitle="4-dimension composite score"
          icon={<Award className="w-5 h-5 text-emerald-500" />}
          color="emerald"
        />
        <StatCard
          title="SEO Optimization Score"
          value={`${metrics.avg_seo_score} / 100`}
          subtitle="Keyword placement & meta length"
          icon={<Sparkles className="w-5 h-5 text-blue-500" />}
          color="blue"
        />
        <StatCard
          title="Catalog Coverage"
          value={`${metrics.descriptions_generated} / ${metrics.total_products}`}
          subtitle={`${metrics.approved_descriptions} approved & published`}
          icon={<BarChart3 className="w-5 h-5 text-purple-500" />}
          color="purple"
        />
      </div>

      {/* Detailed Charts with Commentary */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Chart 1: Quality Score Distribution */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-sm space-y-3">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white">Copy Quality Score Distribution</h3>
          <div className="h-56 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={quality_score_distribution} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="range" tick={{ fontSize: 10 }} stroke="#94a3b8" />
                <YAxis tick={{ fontSize: 11 }} stroke="#94a3b8" />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderRadius: '8px', color: '#fff', fontSize: '12px' }} />
                <Bar dataKey="count" fill="#10b981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          {/* Explanation text */}
          <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800 text-xs text-slate-600 dark:text-slate-400 flex items-start gap-2">
            <Info className="w-4 h-4 text-blue-500 shrink-0 mt-0.5" />
            <div>
              <strong>Quality Insight:</strong> Evaluates overall copy accuracy. Scores over 80 indicate complete technical attributes, compliant brand voice, and natural keyword density.
            </div>
          </div>
        </div>

        {/* Chart 2: SEO Score Distribution */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-sm space-y-3">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white">SEO Score Distribution</h3>
          <div className="h-56 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={seo_score_distribution} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="range" tick={{ fontSize: 11 }} stroke="#94a3b8" />
                <YAxis tick={{ fontSize: 11 }} stroke="#94a3b8" />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderRadius: '8px', color: '#fff', fontSize: '12px' }} />
                <Bar dataKey="count" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800 text-xs text-slate-600 dark:text-slate-400 flex items-start gap-2">
            <Info className="w-4 h-4 text-blue-500 shrink-0 mt-0.5" />
            <div>
              <strong>SEO Metric Insight:</strong> Measures search engine readiness. High scores confirm optimal meta title/description character bounds (140-160 chars) and organic primary keyword presence.
            </div>
          </div>
        </div>

        {/* Chart 3: Tone Usage Distribution */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-sm space-y-3">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white">Brand Tone Distribution</h3>
          <div className="h-56 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={tone_usage} cx="50%" cy="50%" outerRadius={80} dataKey="count" nameKey="tone" label>
                  {tone_usage.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderRadius: '8px', color: '#fff', fontSize: '12px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800 text-xs text-slate-600 dark:text-slate-400 flex items-start gap-2">
            <Info className="w-4 h-4 text-blue-500 shrink-0 mt-0.5" />
            <div>
              <strong>Voice Tone Insight:</strong> Demonstrates brand voice versatility across different product lines (Professional, Luxury, Friendly, Minimal, Technical, Playful, Eco-conscious).
            </div>
          </div>
        </div>

        {/* Chart 4: Category Distribution */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-slate-900 dark:text-white">Retail Category Distribution</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">Inventory SKU coverage across 8 enterprise retail verticals</p>
            </div>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-purple-50 dark:bg-purple-950 text-purple-600 dark:text-purple-400 border border-purple-200 dark:border-purple-800">
              8 Verticals
            </span>
          </div>

          <div className="h-76 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={products_by_category} layout="vertical" margin={{ top: 5, right: 25, left: 10, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e2e8f0" />
                <XAxis type="number" tick={{ fontSize: 11 }} stroke="#94a3b8" />
                <YAxis dataKey="category" type="category" tick={{ fontSize: 10 }} stroke="#94a3b8" width={145} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderRadius: '12px', color: '#fff', fontSize: '12px', border: '1px solid #1e293b' }} />
                <Bar dataKey="count" radius={[0, 6, 6, 0]}>
                  {products_by_category.map((entry, index) => (
                    <Cell
                      key={`cat-cell-${index}`}
                      fill={CATEGORY_PALETTE[entry.category] || COLORS[index % COLORS.length]}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800 text-xs text-slate-600 dark:text-slate-400 flex items-start gap-2">
            <Info className="w-4 h-4 text-blue-500 shrink-0 mt-0.5" />
            <div>
              <strong>Catalog Coverage Insight:</strong> Demonstrates platform adaptability and omni-channel taxonomy support across 8 essential e-commerce retail verticals.
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};
