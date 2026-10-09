import React, { useState } from 'react';
import { Product } from '../../types';
import {
  Sparkles,
  RotateCcw,
  FileText,
  Plus,
  X,
  Tag,
  Cpu,
  Scale,
  Zap,
  CheckCircle2,
  Image as ImageIcon,
  Layers,
  ChevronDown,
  ChevronUp,
  Headphones,
  Shirt,
  Coffee,
  Sparkle
} from 'lucide-react';

interface ProductFormProps {
  onGenerate: (product: Product, options: { tone: string; language: string; word_count_preference: string; engine: string }) => void;
  isLoading: boolean;
}

export const ProductForm: React.FC<ProductFormProps> = ({ onGenerate, isLoading }) => {
  // Form State
  const [formData, setFormData] = useState<Product>({
    name: '',
    sku: '',
    brand: '',
    category: 'Electronics',
    price: undefined,
    currency: 'USD',
    features: [],
    specifications: {},
    target_audience: '',
    primary_keywords: [],
    secondary_keywords: [],
    usp: '',
    image_url: '',
    material: '',
    dimensions: '',
    color: '',
    weight: '',
  });

  // Options State
  const [tone, setTone] = useState<string>('Professional');
  const [language, setLanguage] = useState<string>('English');
  const [wordCount, setWordCount] = useState<string>('Medium');
  const [engine, setEngine] = useState<string>('dual');

  // Dynamic Inputs State
  const [featureInput, setFeatureInput] = useState('');
  const [primaryKwInput, setPrimaryKwInput] = useState('');
  const [secondaryKwInput, setSecondaryKwInput] = useState('');
  const [specKeyInput, setSpecKeyInput] = useState('');
  const [specValInput, setSpecValInput] = useState('');

  // Active Preset Indicator
  const [activePreset, setActivePreset] = useState<string | null>(null);

  // Quick Preset Profiles
  const loadPreset = (presetType: string) => {
    setActivePreset(presetType);
    if (presetType === 'electronics') {
      setFormData({
        sku: 'AUDIO-PRO-900',
        name: 'AuraSound Pro Wireless Headphones',
        brand: 'AuraSound',
        category: 'Electronics',
        price: 199.99,
        currency: 'USD',
        features: ['Active Noise Cancellation', '40-Hour Battery Life', 'Spatial Audio Pacing', 'Multipoint Bluetooth 5.3'],
        specifications: { 'Driver Size': '40mm Neodymium', 'Battery': '40 Hours Playback', 'Charging': 'USB-C Fast Charge (10m = 4h)' },
        target_audience: 'Audiophiles, remote workers, and daily commuters',
        primary_keywords: ['wireless noise cancelling headphones', 'over ear headphones'],
        secondary_keywords: ['bluetooth headset with mic', 'long battery headphones'],
        usp: 'Studio-grade acoustics with hybrid adaptive noise cancellation technology',
        image_url: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=600&q=80',
        material: 'Magnesium Alloy & Memory Foam',
        dimensions: '7.5 x 6.2 x 3.1 inches',
        color: 'Matte Obsidian Black',
        weight: '250g',
      });
      setTone('Technical');
      setWordCount('Medium');
    } else if (presetType === 'fashion') {
      setFormData({
        sku: 'URBAN-JACK-008',
        name: 'UrbanShield All-Weather Waterproof Jacket',
        brand: 'UrbanShield',
        category: 'Fashion',
        price: 129.99,
        currency: 'USD',
        features: ['3-Layer Breathable Membrane', 'Seam-Sealed YKK Zippers', 'Adjustable Storm Hood', 'Reflective Night Vision Trims'],
        specifications: { 'Waterproof Rating': '15,000mm Hydrostatic', 'Breathability': '10,000g/m²', 'Care': 'Machine Wash Cold' },
        target_audience: 'Urban commuters, trail runners, and alpine hikers',
        primary_keywords: ['waterproof rain jacket', 'breathable outdoor jacket'],
        secondary_keywords: ['windbreaker coat', 'all weather jacket'],
        usp: 'Stormproof weather protection fused with tailored minimalist street style',
        image_url: 'https://images.unsplash.com/photo-1544441893-675973e31985?auto=format&fit=crop&w=600&q=80',
        material: '100% Recycled Ripstop Polyester',
        dimensions: 'Sizes S to XXL Tailored',
        color: 'Deep Charcoal Grey',
        weight: '420g',
      });
      setTone('Premium / Luxury');
      setWordCount('Medium');
    } else if (presetType === 'kitchen') {
      setFormData({
        sku: 'CAFE-SMART-500',
        name: 'BaristaCraft Precision Smart Espresso Machine',
        brand: 'BaristaCraft',
        category: 'Home and Kitchen',
        price: 349.99,
        currency: 'USD',
        features: ['15-Bar Italian Pump', 'Dual Thermo-Block Heating', 'Integrated Conical Burr Grinder', 'Micro-Foam Milk Steam Wand'],
        specifications: { 'Pressure': '15 Bar High Output', 'Water Tank': '2.0 Liters Removable', 'Heating Time': '45 Seconds' },
        target_audience: 'Specialty coffee lovers and home culinary enthusiasts',
        primary_keywords: ['smart espresso machine', 'home barista coffee maker'],
        secondary_keywords: ['dual boiler coffee maker', 'espresso machine with grinder'],
        usp: 'Cafe-quality golden crema extraction in under one minute at home',
        image_url: 'https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?auto=format&fit=crop&w=600&q=80',
        material: 'Brushed 304 Stainless Steel',
        dimensions: '12.5 x 11.0 x 14.2 inches',
        color: 'Brushed Silver',
        weight: '8.4kg',
      });
      setTone('Premium / Luxury');
      setWordCount('Long');
    } else if (presetType === 'beauty') {
      setFormData({
        sku: 'GLOW-REV-30',
        name: 'LumiGlow 20% Vitamin C Radiance Peptide Serum',
        brand: 'LumiGlow',
        category: 'Beauty and Personal Care',
        price: 48.00,
        currency: 'USD',
        features: ['20% Stabilized L-Ascorbic Acid', 'Triple Multi-Molecular Hyaluronic Acid', 'Ferulic Acid Antioxidant Shield', 'Cruelty-Free & Dermatologist Tested'],
        specifications: { 'Volume': '30ml / 1.0 fl oz', 'Formulation': 'Lightweight Fast-Absorbing', 'Skin Type': 'All Skin Types' },
        target_audience: 'Individuals seeking clinical skin radiance and barrier hydration',
        primary_keywords: ['vitamin c face serum', 'brightening anti aging serum'],
        secondary_keywords: ['hyaluronic acid peptide serum', 'glow facial oil'],
        usp: 'Clinically proven 3x boost in skin luminosity in 14 days without irritation',
        image_url: 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&w=600&q=80',
        material: 'UV-Protected Amber Glass Dropper Bottle',
        dimensions: '30ml Bottle',
        color: 'Golden Amber Essence',
        weight: '90g',
      });
      setTone('Friendly');
      setWordCount('Medium');
    }
  };

  const handleReset = () => {
    setActivePreset(null);
    setFormData({
      name: '',
      sku: '',
      brand: '',
      category: 'Electronics',
      price: undefined,
      currency: 'USD',
      features: [],
      specifications: {},
      target_audience: '',
      primary_keywords: [],
      secondary_keywords: [],
      usp: '',
      image_url: '',
      material: '',
      dimensions: '',
      color: '',
      weight: '',
    });
    setTone('Professional');
    setWordCount('Medium');
    setEngine('dual');
  };

  // Dynamic Handlers
  const addFeature = () => {
    if (featureInput.trim()) {
      setFormData((prev) => ({ ...prev, features: [...(prev.features || []), featureInput.trim()] }));
      setFeatureInput('');
    }
  };
  const removeFeature = (idx: number) => {
    setFormData((prev) => ({ ...prev, features: (prev.features || []).filter((_, i) => i !== idx) }));
  };

  const addPrimaryKw = () => {
    if (primaryKwInput.trim()) {
      setFormData((prev) => ({ ...prev, primary_keywords: [...(prev.primary_keywords || []), primaryKwInput.trim()] }));
      setPrimaryKwInput('');
    }
  };
  const removePrimaryKw = (idx: number) => {
    setFormData((prev) => ({ ...prev, primary_keywords: (prev.primary_keywords || []).filter((_, i) => i !== idx) }));
  };

  const addSecondaryKw = () => {
    if (secondaryKwInput.trim()) {
      setFormData((prev) => ({ ...prev, secondary_keywords: [...(prev.secondary_keywords || []), secondaryKwInput.trim()] }));
      setSecondaryKwInput('');
    }
  };
  const removeSecondaryKw = (idx: number) => {
    setFormData((prev) => ({ ...prev, secondary_keywords: (prev.secondary_keywords || []).filter((_, i) => i !== idx) }));
  };

  const addSpec = () => {
    if (specKeyInput.trim() && specValInput.trim()) {
      setFormData((prev) => ({
        ...prev,
        specifications: { ...(prev.specifications || {}), [specKeyInput.trim()]: specValInput.trim() },
      }));
      setSpecKeyInput('');
      setSpecValInput('');
    }
  };
  const removeSpec = (key: string) => {
    setFormData((prev) => {
      const next = { ...(prev.specifications || {}) };
      delete next[key];
      return { ...prev, specifications: next };
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onGenerate(formData, { tone, language, word_count_preference: wordCount, engine });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* 🚀 Interactive 1-Click Preset Gallery */}
      <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-sm space-y-3.5">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="p-1.5 rounded-lg bg-blue-500/10 text-blue-600 dark:text-blue-400">
              <Sparkles className="w-4 h-4" />
            </span>
            <div>
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-900 dark:text-white">
                1-Click Demo Profiles
              </h3>
              <p className="text-[11px] text-slate-500 dark:text-slate-400">
                Instantly load rich catalog products to test live Dual-AI generation
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={handleReset}
            className="flex items-center gap-1.5 px-2.5 py-1 text-xs font-semibold text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 rounded-lg transition-colors cursor-pointer"
          >
            <RotateCcw className="w-3 h-3" />
            Clear
          </button>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
          {/* Preset 1: Headphones */}
          <button
            type="button"
            onClick={() => loadPreset('electronics')}
            className={`p-2.5 rounded-xl border text-left transition-all cursor-pointer flex flex-col justify-between ${
              activePreset === 'electronics'
                ? 'border-blue-500 bg-blue-50/80 dark:bg-blue-950/40 ring-2 ring-blue-500/25 shadow-sm'
                : 'border-slate-200 dark:border-slate-800 hover:border-blue-300 dark:hover:border-slate-700 bg-slate-50/50 dark:bg-slate-850/50'
            }`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="p-1.5 rounded-lg bg-blue-100 dark:bg-blue-900/60 text-blue-700 dark:text-blue-300">
                <Headphones className="w-3.5 h-3.5" />
              </span>
              <span className="text-[10px] font-bold text-slate-500">$199.99</span>
            </div>
            <div className="text-xs font-bold text-slate-900 dark:text-white truncate">
              ANC Headphones
            </div>
            <div className="text-[10px] text-slate-500 dark:text-slate-400">Electronics • High Tech</div>
          </button>

          {/* Preset 2: Jacket */}
          <button
            type="button"
            onClick={() => loadPreset('fashion')}
            className={`p-2.5 rounded-xl border text-left transition-all cursor-pointer flex flex-col justify-between ${
              activePreset === 'fashion'
                ? 'border-purple-500 bg-purple-50/80 dark:bg-purple-950/40 ring-2 ring-purple-500/25 shadow-sm'
                : 'border-slate-200 dark:border-slate-800 hover:border-purple-300 dark:hover:border-slate-700 bg-slate-50/50 dark:bg-slate-850/50'
            }`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="p-1.5 rounded-lg bg-purple-100 dark:bg-purple-900/60 text-purple-700 dark:text-purple-300">
                <Shirt className="w-3.5 h-3.5" />
              </span>
              <span className="text-[10px] font-bold text-slate-500">$129.99</span>
            </div>
            <div className="text-xs font-bold text-slate-900 dark:text-white truncate">
              Weatherproof Jacket
            </div>
            <div className="text-[10px] text-slate-500 dark:text-slate-400">Fashion • Technical</div>
          </button>

          {/* Preset 3: Espresso */}
          <button
            type="button"
            onClick={() => loadPreset('kitchen')}
            className={`p-2.5 rounded-xl border text-left transition-all cursor-pointer flex flex-col justify-between ${
              activePreset === 'kitchen'
                ? 'border-amber-500 bg-amber-50/80 dark:bg-amber-950/40 ring-2 ring-amber-500/25 shadow-sm'
                : 'border-slate-200 dark:border-slate-800 hover:border-amber-300 dark:hover:border-slate-700 bg-slate-50/50 dark:bg-slate-850/50'
            }`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="p-1.5 rounded-lg bg-amber-100 dark:bg-amber-900/60 text-amber-700 dark:text-amber-300">
                <Coffee className="w-3.5 h-3.5" />
              </span>
              <span className="text-[10px] font-bold text-slate-500">$349.99</span>
            </div>
            <div className="text-xs font-bold text-slate-900 dark:text-white truncate">
              Smart Espresso
            </div>
            <div className="text-[10px] text-slate-500 dark:text-slate-400">Kitchen • Premium</div>
          </button>

          {/* Preset 4: Skincare */}
          <button
            type="button"
            onClick={() => loadPreset('beauty')}
            className={`p-2.5 rounded-xl border text-left transition-all cursor-pointer flex flex-col justify-between ${
              activePreset === 'beauty'
                ? 'border-rose-500 bg-rose-50/80 dark:bg-rose-950/40 ring-2 ring-rose-500/25 shadow-sm'
                : 'border-slate-200 dark:border-slate-800 hover:border-rose-300 dark:hover:border-slate-700 bg-slate-50/50 dark:bg-slate-850/50'
            }`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="p-1.5 rounded-lg bg-rose-100 dark:bg-rose-900/60 text-rose-700 dark:text-rose-300">
                <Sparkle className="w-3.5 h-3.5" />
              </span>
              <span className="text-[10px] font-bold text-slate-500">$48.00</span>
            </div>
            <div className="text-xs font-bold text-slate-900 dark:text-white truncate">
              Vitamin C Serum
            </div>
            <div className="text-[10px] text-slate-500 dark:text-slate-400">Beauty • Radiance</div>
          </button>
        </div>
      </div>

      {/* Section 1: Basic Information */}
      <div className="p-5 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 space-y-4 shadow-sm">
        <div className="flex items-center justify-between">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-blue-500" />
            1. Basic Information
          </h4>
          {formData.name && (
            <span className="text-[11px] font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3" /> Ready
            </span>
          )}
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="sm:col-span-2">
            <div className="flex items-center justify-between mb-1">
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">
                Product Name <span className="text-rose-500">*</span>
              </label>
              <span className="text-[10px] font-mono text-slate-400">
                {formData.name.length} chars
              </span>
            </div>
            <input
              type="text"
              required
              placeholder="e.g. AuraSound Pro Wireless Headphones"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              SKU / Product ID
            </label>
            <input
              type="text"
              placeholder="e.g. AUDIO-PRO-900"
              value={formData.sku || ''}
              onChange={(e) => setFormData({ ...formData, sku: e.target.value })}
              className="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Brand
            </label>
            <input
              type="text"
              placeholder="e.g. AuraSound"
              value={formData.brand || ''}
              onChange={(e) => setFormData({ ...formData, brand: e.target.value })}
              className="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Category <span className="text-rose-500">*</span>
            </label>
            <select
              required
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              className="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
            >
              <option value="Electronics">Electronics</option>
              <option value="Fashion">Fashion</option>
              <option value="Home and Kitchen">Home and Kitchen</option>
              <option value="Beauty and Personal Care">Beauty and Personal Care</option>
              <option value="Sports and Fitness">Sports and Fitness</option>
              <option value="Grocery">Grocery</option>
              <option value="Furniture">Furniture</option>
              <option value="Travel Accessories">Travel Accessories</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Price & Currency
            </label>
            <div className="flex gap-2">
              <input
                type="number"
                step="0.01"
                placeholder="199.99"
                value={formData.price !== undefined ? formData.price : ''}
                onChange={(e) => setFormData({ ...formData, price: e.target.value ? parseFloat(e.target.value) : undefined })}
                className="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
              />
              <select
                value={formData.currency}
                onChange={(e) => setFormData({ ...formData, currency: e.target.value })}
                className="w-26 px-2.5 py-2.5 text-sm rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none"
              >
                <option value="USD">USD ($)</option>
                <option value="EUR">EUR (€)</option>
                <option value="GBP">GBP (£)</option>
                <option value="INR">INR (₹)</option>
              </select>
            </div>
          </div>

          <div className="sm:col-span-2">
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Product Image URL (Live Preview)
            </label>
            <div className="flex gap-2">
              <input
                type="url"
                placeholder="https://images.unsplash.com/photo-..."
                value={formData.image_url || ''}
                onChange={(e) => setFormData({ ...formData, image_url: e.target.value })}
                className="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
              />
              {formData.image_url && (
                <img
                  src={formData.image_url}
                  alt="Thumb"
                  className="w-10 h-10 rounded-lg object-cover border border-slate-200 dark:border-slate-700 shrink-0"
                  onError={(e) => { (e.target as HTMLElement).style.display = 'none'; }}
                />
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Section 2: Product Details & Attributes */}
      <div className="p-5 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 space-y-4 shadow-sm">
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-cyan-500" />
          2. Product Details & Attributes
        </h4>

        {/* Dynamic Features Input */}
        <div>
          <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
            Key Features (Bullet points)
          </label>
          <div className="flex gap-2 mb-2">
            <input
              type="text"
              placeholder="e.g. Active Noise Cancellation, Fast Charging"
              value={featureInput}
              onChange={(e) => setFeatureInput(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addFeature(); } }}
              className="flex-1 px-3.5 py-2 text-sm rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white outline-none"
            />
            <button
              type="button"
              onClick={addFeature}
              className="px-3.5 py-2 bg-slate-900 dark:bg-slate-700 text-white rounded-xl text-xs font-bold hover:bg-slate-800 flex items-center gap-1 cursor-pointer transition-colors"
            >
              <Plus className="w-3.5 h-3.5" /> Add
            </button>
          </div>
          <div className="flex flex-wrap gap-1.5">
            {formData.features?.map((f, i) => (
              <span key={i} className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold bg-blue-50 dark:bg-blue-950/60 text-blue-700 dark:text-blue-300 border border-blue-200/80 dark:border-blue-800/80 animate-in zoom-in-95 duration-100">
                {f}
                <button type="button" onClick={() => removeFeature(i)} className="hover:text-rose-500 cursor-pointer">
                  <X className="w-3 h-3" />
                </button>
              </span>
            ))}
          </div>
        </div>

        {/* Dynamic Specifications */}
        <div>
          <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
            Technical Specifications (Key - Value Pairs)
          </label>
          <div className="flex gap-2 mb-2">
            <input
              type="text"
              placeholder="Key (e.g. Battery Life)"
              value={specKeyInput}
              onChange={(e) => setSpecKeyInput(e.target.value)}
              className="w-1/3 px-3.5 py-2 text-sm rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white outline-none"
            />
            <input
              type="text"
              placeholder="Value (e.g. 40 Hours Playback)"
              value={specValInput}
              onChange={(e) => setSpecValInput(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addSpec(); } }}
              className="flex-1 px-3.5 py-2 text-sm rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white outline-none"
            />
            <button
              type="button"
              onClick={addSpec}
              className="px-3.5 py-2 bg-slate-900 dark:bg-slate-700 text-white rounded-xl text-xs font-bold hover:bg-slate-800 flex items-center gap-1 cursor-pointer transition-colors"
            >
              <Plus className="w-3.5 h-3.5" /> Add
            </button>
          </div>
          <div className="flex flex-wrap gap-2">
            {Object.entries(formData.specifications || {}).map(([k, v]) => (
              <span key={k} className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-medium bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 border border-slate-200 dark:border-slate-700">
                <strong className="text-slate-900 dark:text-white">{k}:</strong> {v}
                <button type="button" onClick={() => removeSpec(k)} className="hover:text-rose-500 cursor-pointer">
                  <X className="w-3 h-3" />
                </button>
              </span>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-1">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Target Audience
            </label>
            <input
              type="text"
              placeholder="e.g. Audiophiles, remote workers, frequent travelers"
              value={formData.target_audience || ''}
              onChange={(e) => setFormData({ ...formData, target_audience: e.target.value })}
              className="w-full px-3.5 py-2 text-sm rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Unique Selling Proposition (USP)
            </label>
            <input
              type="text"
              placeholder="e.g. Studio acoustics with hybrid adaptive cancellation"
              value={formData.usp || ''}
              onChange={(e) => setFormData({ ...formData, usp: e.target.value })}
              className="w-full px-3.5 py-2 text-sm rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Material
            </label>
            <input
              type="text"
              placeholder="e.g. Magnesium Alloy & Memory Foam"
              value={formData.material || ''}
              onChange={(e) => setFormData({ ...formData, material: e.target.value })}
              className="w-full px-3.5 py-2 text-sm rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Dimensions / Weight / Color
            </label>
            <div className="grid grid-cols-3 gap-2">
              <input
                type="text"
                placeholder="7.5 x 6.2 in"
                value={formData.dimensions || ''}
                onChange={(e) => setFormData({ ...formData, dimensions: e.target.value })}
                className="w-full px-2.5 py-2 text-xs rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white outline-none"
              />
              <input
                type="text"
                placeholder="Matte Black"
                value={formData.color || ''}
                onChange={(e) => setFormData({ ...formData, color: e.target.value })}
                className="w-full px-2.5 py-2 text-xs rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white outline-none"
              />
              <input
                type="text"
                placeholder="250g"
                value={formData.weight || ''}
                onChange={(e) => setFormData({ ...formData, weight: e.target.value })}
                className="w-full px-2.5 py-2 text-xs rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white outline-none"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Section 3: SEO Configuration */}
      <div className="p-5 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 space-y-4 shadow-sm">
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 flex items-center gap-1.5">
          <Tag className="w-3.5 h-3.5 text-cyan-500" />
          3. SEO Target Keywords
        </h4>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Primary SEO Keywords (High Priority)
            </label>
            <div className="flex gap-2 mb-2">
              <input
                type="text"
                placeholder="e.g. noise cancelling headphones"
                value={primaryKwInput}
                onChange={(e) => setPrimaryKwInput(e.target.value)}
                onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addPrimaryKw(); } }}
                className="flex-1 px-3.5 py-2 text-sm rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white outline-none"
              />
              <button
                type="button"
                onClick={addPrimaryKw}
                className="px-3.5 py-2 bg-cyan-600 text-white rounded-xl text-xs font-bold hover:bg-cyan-700 flex items-center gap-1 cursor-pointer transition-colors"
              >
                <Plus className="w-3.5 h-3.5" /> Add
              </button>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {formData.primary_keywords?.map((kw, i) => (
                <span key={i} className="inline-flex items-center gap-1 px-3 py-1 rounded-lg text-xs font-bold bg-cyan-50 dark:bg-cyan-950/60 text-cyan-700 dark:text-cyan-300 border border-cyan-200/80 dark:border-cyan-800/80">
                  {kw}
                  <button type="button" onClick={() => removePrimaryKw(i)} className="hover:text-rose-500 cursor-pointer">
                    <X className="w-3 h-3" />
                  </button>
                </span>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Secondary Keywords (Long-Tail)
            </label>
            <div className="flex gap-2 mb-2">
              <input
                type="text"
                placeholder="e.g. long battery life headset"
                value={secondaryKwInput}
                onChange={(e) => setSecondaryKwInput(e.target.value)}
                onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addSecondaryKw(); } }}
                className="flex-1 px-3.5 py-2 text-sm rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white outline-none"
              />
              <button
                type="button"
                onClick={addSecondaryKw}
                className="px-3.5 py-2 bg-slate-800 dark:bg-slate-700 text-white rounded-xl text-xs font-bold hover:bg-slate-700 flex items-center gap-1 cursor-pointer transition-colors"
              >
                <Plus className="w-3.5 h-3.5" /> Add
              </button>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {formData.secondary_keywords?.map((kw, i) => (
                <span key={i} className="inline-flex items-center gap-1 px-3 py-1 rounded-lg text-xs font-medium bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
                  {kw}
                  <button type="button" onClick={() => removeSecondaryKw(i)} className="hover:text-rose-500 cursor-pointer">
                    <X className="w-3 h-3" />
                  </button>
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Section 4: AI Copywriting Preferences & Decision Engine */}
      <div className="p-5 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 space-y-4 shadow-sm">
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-purple-500" />
          4. Content Preferences & Model Selection
        </h4>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Brand Tone
            </label>
            <select
              value={tone}
              onChange={(e) => setTone(e.target.value)}
              className="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none"
            >
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
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Word Count Preference
            </label>
            <select
              value={wordCount}
              onChange={(e) => setWordCount(e.target.value)}
              className="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none"
            >
              <option value="Short">Short (40–60 words)</option>
              <option value="Medium">Medium (80–120 words)</option>
              <option value="Long">Long (150–200 words)</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Language
            </label>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none"
            >
              <option value="English">English</option>
              <option value="Spanish">Spanish</option>
              <option value="French">French</option>
              <option value="German">German</option>
              <option value="Japanese">Japanese</option>
            </select>
          </div>
        </div>

        {/* Engine Selection Arena Cards */}
        <div className="pt-3 border-t border-slate-100 dark:border-slate-800 space-y-2.5">
          <div className="flex items-center justify-between">
            <label className="block text-xs font-bold text-slate-900 dark:text-white">
              AI Decision Mode & Model Arena
            </label>
            <span className="text-[11px] text-cyan-600 dark:text-cyan-400 font-bold flex items-center gap-1">
              <Zap className="w-3 h-3" /> Claude 3.5 + Gemini 3.5
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {/* Dual AI Arbiter */}
            <button
              type="button"
              onClick={() => setEngine('dual')}
              className={`p-4 rounded-2xl border text-left transition-all cursor-pointer flex flex-col justify-between ${
                engine === 'dual'
                  ? 'border-blue-600 bg-blue-50/90 dark:bg-blue-950/40 ring-2 ring-blue-500/30 shadow-md'
                  : 'border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 bg-slate-50/50 dark:bg-slate-850/40'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-extrabold text-slate-900 dark:text-white flex items-center gap-1.5">
                    <Scale className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                    Dual-AI Arbiter
                  </span>
                  <span className="text-[10px] font-black px-2 py-0.5 rounded-full bg-blue-600 text-white shadow-2xs">
                    Recommended
                  </span>
                </div>
                <p className="text-[11px] text-slate-600 dark:text-slate-400 leading-snug">
                  Benchmarks <strong>Claude 3.5</strong> & <strong>Gemini 3.5</strong>, scores both across 4 dimensions, and awards the winner.
                </p>
              </div>
            </button>

            {/* Anthropic Claude */}
            <button
              type="button"
              onClick={() => setEngine('anthropic')}
              className={`p-4 rounded-2xl border text-left transition-all cursor-pointer flex flex-col justify-between ${
                engine === 'anthropic'
                  ? 'border-purple-600 bg-purple-50/90 dark:bg-purple-950/40 ring-2 ring-purple-500/30 shadow-md'
                  : 'border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 bg-slate-50/50 dark:bg-slate-850/40'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-bold text-slate-900 dark:text-white flex items-center gap-1.5">
                    <Cpu className="w-4 h-4 text-purple-600 dark:text-purple-400" />
                    Anthropic Claude
                  </span>
                  <span className="text-[10px] text-purple-700 dark:text-purple-300 font-mono font-bold">3.5 Sonnet</span>
                </div>
                <p className="text-[11px] text-slate-600 dark:text-slate-400 leading-snug">
                  Superior narrative pacing, sensory detail, and nuanced compliance with brand tone rules.
                </p>
              </div>
            </button>

            {/* Google Gemini */}
            <button
              type="button"
              onClick={() => setEngine('gemini')}
              className={`p-4 rounded-2xl border text-left transition-all cursor-pointer flex flex-col justify-between ${
                engine === 'gemini'
                  ? 'border-cyan-600 bg-cyan-50/90 dark:bg-cyan-950/40 ring-2 ring-cyan-500/30 shadow-md'
                  : 'border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 bg-slate-50/50 dark:bg-slate-850/40'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-bold text-slate-900 dark:text-white flex items-center gap-1.5">
                    <Sparkles className="w-4 h-4 text-cyan-600 dark:text-cyan-400" />
                    Google Gemini
                  </span>
                  <span className="text-[10px] text-cyan-700 dark:text-cyan-300 font-mono font-bold">3.5 Lite</span>
                </div>
                <p className="text-[11px] text-slate-600 dark:text-slate-400 leading-snug">
                  Ultra-fast structured reasoning, dense attribute parsing, and punchy conversion hooks.
                </p>
              </div>
            </button>
          </div>
        </div>
      </div>

      {/* Primary Action Button */}
      <button
        type="submit"
        disabled={isLoading || !formData.name.trim()}
        className="w-full py-4 px-6 rounded-2xl font-extrabold text-sm text-white bg-gradient-to-r from-blue-600 via-indigo-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 shadow-xl shadow-blue-500/25 disabled:opacity-50 transition-all duration-200 flex items-center justify-center gap-2 cursor-pointer hover:scale-[1.01] active:scale-[0.99]"
      >
        {isLoading ? (
          <>
            <span className="h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            <span>Analyzing Product Attributes & Running Dual-AI Arbiter...</span>
          </>
        ) : (
          <>
            <Sparkles className="w-4 h-4" />
            <span>
              {engine === 'dual'
                ? 'Benchmark Both Models & Decide Perfect Description'
                : `Generate Description with ${engine === 'anthropic' ? 'Anthropic Claude' : 'Google Gemini 3.5 Lite'}`}
            </span>
          </>
        )}
      </button>

      {/* Offline Mock Guarantee Note */}
      <div className="flex items-center justify-center gap-1.5 text-[11px] text-slate-500 dark:text-slate-400 text-center">
        <span>⚡ Zero-Downtime Architecture: If live API keys are empty, CatalogCraft automatically falls back to the deterministic offline Mock Engine.</span>
      </div>
    </form>
  );
};
