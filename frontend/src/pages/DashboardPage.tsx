import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { analyticsApi } from '../api';
import { AnalyticsData } from '../types';
import { StatCard } from '../components/common/StatCard';
import {
  Package,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  Search,
  Award,
  Layers,
  TrendingUp,
  Cpu,
  ArrowRight,
  Wand2,
  Sliders,
  Zap,
  BarChart2
} from 'lucide-react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  CartesianGrid
} from 'recharts';

import { DemoVideoPlayer } from '../components/common/DemoVideoPlayer';

export const DashboardPage: React.FC = () => {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    analyticsApi
      .getAnalytics()
      .then(setData)
      .finally(() => setIsLoading(false));
  }, []);

  if (isLoading || !data) {
    return (
      <div className="flex items-center justify-center h-80 text-slate-400">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
          <span className="text-xs font-bold text-slate-500 dark:text-slate-400">Loading Retail Intelligence Dashboard...</span>
        </div>
      </div>
    );
  }

  const { metrics, generations_over_time, products_by_category, status_distribution, recent_activities } = data;

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

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Hero Welcome Banner */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-blue-900 via-indigo-950 to-slate-950 text-white p-6 sm:p-8 shadow-2xl border border-blue-800/40">
        <div className="absolute top-0 right-0 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 right-1/4 w-80 h-80 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 max-w-3xl space-y-3">
          <div className="flex flex-wrap items-center gap-2">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-black bg-cyan-500/20 text-cyan-300 border border-cyan-400/30 shadow-xs">
              <Sparkles className="w-3.5 h-3.5 text-cyan-400 animate-pulse" /> Dual-AI Studio Live
            </span>
            <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-white/10 text-white border border-white/20">
              <Cpu className="w-3 h-3 text-purple-400" /> Claude 3.5 Sonnet + Gemini 3.5 Lite
            </span>
          </div>

          <h1 className="text-2xl sm:text-3xl font-black tracking-tight text-white leading-tight">
            CatalogCraft AI Copywriting Studio
          </h1>
          <p className="text-xs sm:text-sm text-slate-300 leading-relaxed max-w-2xl">
            Autonomous multi-model arbitration for e-commerce catalog descriptions. Generates and benchmarks copy candidates across completeness, SEO parameters, and brand voice rules.
          </p>

          {/* Quick Action Shortcuts */}
          <div className="flex flex-wrap items-center gap-3 pt-3">
            <Link
              to="/generate"
              className="px-4 py-2.5 rounded-xl font-bold text-xs text-white bg-blue-600 hover:bg-blue-500 shadow-lg shadow-blue-600/30 flex items-center gap-2 transition-all cursor-pointer hover:scale-102"
            >
              <Wand2 className="w-3.5 h-3.5" />
              <span>Generate Single Copy</span>
            </Link>

            <Link
              to="/batch"
              className="px-4 py-2.5 rounded-xl font-bold text-xs text-slate-200 bg-white/10 hover:bg-white/20 border border-white/15 flex items-center gap-2 transition-all cursor-pointer hover:scale-102"
            >
              <Layers className="w-3.5 h-3.5" />
              <span>Batch Processor (CSV)</span>
            </Link>

            <Link
              to="/catalogue"
              className="px-4 py-2.5 rounded-xl font-bold text-xs text-slate-200 bg-white/10 hover:bg-white/20 border border-white/15 flex items-center gap-2 transition-all cursor-pointer hover:scale-102"
            >
              <Package className="w-3.5 h-3.5" />
              <span>Browse Catalog</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Metric Cards Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Catalog Products"
          value={metrics.total_products}
          subtitle="Enterprise retail inventory"
          icon={<Package className="w-5 h-5 text-blue-500" />}
          color="blue"
        />
        <StatCard
          title="Descriptions Generated"
          value={metrics.descriptions_generated}
          subtitle={`${Math.round((metrics.descriptions_generated / (metrics.total_products || 1)) * 100)}% catalog coverage`}
          icon={<Sparkles className="w-5 h-5 text-cyan-500" />}
          color="cyan"
        />
        <StatCard
          title="Approved Descriptions"
          value={metrics.approved_descriptions}
          subtitle={`${metrics.products_needing_review} flagged for review`}
          icon={<CheckCircle2 className="w-5 h-5 text-emerald-500" />}
          color="emerald"
        />
        <StatCard
          title="Average Quality Score"
          value={`${metrics.avg_quality_score} / 100`}
          subtitle={`Average SEO: ${metrics.avg_seo_score} / 100`}
          icon={<Award className="w-5 h-5 text-amber-500" />}
          color="amber"
        />
      </div>

      {/* Retailer Interactive Demo Video Walkthrough */}
      <DemoVideoPlayer />

      {/* Main Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Chart 1: Generations Velocity */}
        <div className="lg:col-span-8 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-extrabold text-slate-900 dark:text-white flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-blue-500" />
                Copy Generation Velocity Over Time
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">Daily content generation output and model throughput</p>
            </div>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-50 dark:bg-blue-950 text-blue-600 dark:text-blue-400 border border-blue-200 dark:border-blue-800">
              Last 7 Days
            </span>
          </div>

          <div className="h-68 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={generations_over_time} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.45} />
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="date" tick={{ fontSize: 11 }} stroke="#94a3b8" />
                <YAxis tick={{ fontSize: 11 }} stroke="#94a3b8" />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderRadius: '12px', color: '#fff', fontSize: '12px', border: '1px solid #1e293b' }} />
                <Area type="monotone" dataKey="count" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#colorCount)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 2: Status Breakdown */}
        <div className="lg:col-span-4 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 shadow-sm space-y-4 flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-extrabold text-slate-900 dark:text-white flex items-center gap-2">
              <BarChart2 className="w-4 h-4 text-emerald-500" />
              Approval Pipeline Status
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400">Review vs. Approved inventory</p>
          </div>

          <div className="h-56 w-full flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={status_distribution}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={85}
                  paddingAngle={5}
                  dataKey="count"
                  nameKey="status"
                >
                  {status_distribution.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderRadius: '12px', color: '#fff', fontSize: '12px', border: '1px solid #1e293b' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="flex justify-around text-xs font-bold pt-3 border-t border-slate-100 dark:border-slate-800">
            {status_distribution.map((item, i) => (
              <div key={item.status} className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: COLORS[i % COLORS.length] }} />
                <span className="text-slate-600 dark:text-slate-400">{item.status}: <strong>{item.count}</strong></span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Secondary Row Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Chart 3: Category Distribution */}
        <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-extrabold text-slate-900 dark:text-white">Retail Category Distribution</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">Inventory SKU coverage across 8 enterprise retail verticals</p>
            </div>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-cyan-50 dark:bg-cyan-950 text-cyan-600 dark:text-cyan-400 border border-cyan-200 dark:border-cyan-800">
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
                      key={`cat-cell-dash-${index}`}
                      fill={CATEGORY_PALETTE[entry.category] || COLORS[index % COLORS.length]}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recent Activity Table */}
        <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-extrabold text-slate-900 dark:text-white">Recent Copywriting Activity</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">Live AI execution log and score outcomes</p>
            </div>
            <Link to="/catalogue" className="text-xs font-bold text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1">
              View All <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="text-slate-400 font-bold border-b border-slate-100 dark:border-slate-800">
                <tr>
                  <th className="pb-2.5">Product Name</th>
                  <th className="pb-2.5">Quality</th>
                  <th className="pb-2.5">Status</th>
                  <th className="pb-2.5 text-right">Timestamp</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800 font-medium">
                {recent_activities.slice(0, 5).map((act) => (
                  <tr key={act.id} className="hover:bg-slate-50/70 dark:hover:bg-slate-800/40 transition-colors">
                    <td className="py-3 font-semibold text-slate-900 dark:text-white truncate max-w-[160px]">
                      {act.product_name}
                    </td>
                    <td className="py-3 font-black text-emerald-600 dark:text-emerald-400">
                      {act.score.toFixed(0)} <span className="text-[10px] text-slate-400 font-normal">/100</span>
                    </td>
                    <td className="py-3">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                        act.status === 'Approved'
                          ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300'
                          : 'bg-blue-100 text-blue-700 dark:bg-blue-950 dark:text-blue-300'
                      }`}>
                        {act.status}
                      </span>
                    </td>
                    <td className="py-3 text-slate-400 text-[11px] text-right">
                      {act.timestamp}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
