import React from 'react';
import { Search, Filter, ArrowUpDown } from 'lucide-react';

interface FilterProps {
  search: string;
  setSearch: (v: string) => void;
  category: string;
  setCategory: (v: string) => void;
  brand: string;
  setBrand: (v: string) => void;
  status: string;
  setStatus: (v: string) => void;
  tone: string;
  setTone: (v: string) => void;
  minQualityScore: number;
  setMinQualityScore: (v: number) => void;
  sortBy: string;
  setSortBy: (v: string) => void;
  categories: string[];
  brands: string[];
}

export const CatalogueFilterBar: React.FC<FilterProps> = ({
  search,
  setSearch,
  category,
  setCategory,
  brand,
  setBrand,
  status,
  setStatus,
  tone,
  setTone,
  minQualityScore,
  setMinQualityScore,
  sortBy,
  setSortBy,
  categories,
  brands,
}) => {
  return (
    <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 shadow-sm space-y-3">
      {/* Search & Sort Row */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
          <input
            type="text"
            placeholder="Search by product name, SKU, brand..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-4 py-2 text-xs rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div className="flex items-center gap-2">
          <ArrowUpDown className="w-3.5 h-3.5 text-slate-400" />
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-3 py-2 text-xs font-semibold rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white outline-none"
          >
            <option value="newest">Sort: Newest First</option>
            <option value="oldest">Sort: Oldest First</option>
            <option value="name">Sort: Product Name</option>
            <option value="quality_score">Sort: Highest Quality Score</option>
            <option value="seo_score">Sort: Highest SEO Score</option>
          </select>
        </div>
      </div>

      {/* Filters Row */}
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 pt-2 border-t border-slate-100 dark:border-slate-800 text-xs">
        <div>
          <label className="block text-[10px] font-bold uppercase text-slate-400 mb-0.5">Category</label>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="w-full p-1.5 rounded border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200"
          >
            <option value="All">All Categories</option>
            {categories.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-[10px] font-bold uppercase text-slate-400 mb-0.5">Brand</label>
          <select
            value={brand}
            onChange={(e) => setBrand(e.target.value)}
            className="w-full p-1.5 rounded border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200"
          >
            <option value="All">All Brands</option>
            {brands.map((b) => (
              <option key={b} value={b}>{b}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-[10px] font-bold uppercase text-slate-400 mb-0.5">Status</label>
          <select
            value={status}
            onChange={(e) => setStatus(e.target.value)}
            className="w-full p-1.5 rounded border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200"
          >
            <option value="All">All Statuses</option>
            <option value="Approved">Approved</option>
            <option value="Draft">Draft</option>
            <option value="Needs Review">Needs Review</option>
          </select>
        </div>

        <div>
          <label className="block text-[10px] font-bold uppercase text-slate-400 mb-0.5">Tone</label>
          <select
            value={tone}
            onChange={(e) => setTone(e.target.value)}
            className="w-full p-1.5 rounded border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200"
          >
            <option value="All">All Tones</option>
            <option value="Professional">Professional</option>
            <option value="Premium / Luxury">Premium / Luxury</option>
            <option value="Friendly">Friendly</option>
            <option value="Minimal">Minimal</option>
            <option value="Technical">Technical</option>
            <option value="Playful">Playful</option>
            <option value="Eco-conscious">Eco-conscious</option>
          </select>
        </div>

        <div>
          <label className="block text-[10px] font-bold uppercase text-slate-400 mb-0.5">
            Min Quality: {minQualityScore}
          </label>
          <input
            type="range"
            min="0"
            max="90"
            step="10"
            value={minQualityScore}
            onChange={(e) => setMinQualityScore(Number(e.target.value))}
            className="w-full accent-blue-600 mt-1 cursor-pointer"
          />
        </div>
      </div>
    </div>
  );
};
