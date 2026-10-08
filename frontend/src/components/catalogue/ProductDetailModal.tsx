import React, { useState, useEffect } from 'react';
import { ProductCatalogItem, ContentVersion } from '../../types';
import { ScoreBadge } from '../common/ScoreBadge';
import { StatusBadge } from '../common/StatusBadge';
import { generationApi } from '../../api';
import {
  X,
  Copy,
  Check,
  CheckCircle,
  AlertCircle,
  History,
  Save,
  RefreshCw,
  Sparkles,
  Tag,
  ShieldCheck,
  FileText
} from 'lucide-react';

interface ModalProps {
  item: ProductCatalogItem | null;
  onClose: () => void;
  onUpdateSuccess: () => void;
}

export const ProductDetailModal: React.FC<ModalProps> = ({ item, onClose, onUpdateSuccess }) => {
  if (!item) return null;

  const { product, generated_content: content } = item;
  const [activeTab, setActiveTab] = useState<'content' | 'edit' | 'history'>('content');
  const [copied, setCopied] = useState(false);
  const [history, setHistory] = useState<ContentVersion[]>([]);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);

  // Edit Form State
  const [title, setTitle] = useState(content?.title || '');
  const [shortDesc, setShortDesc] = useState(content?.short_description || '');
  const [fullDesc, setFullDesc] = useState(content?.full_description || '');
  const [metaTitle, setMetaTitle] = useState(content?.meta_title || '');
  const [metaDesc, setMetaDesc] = useState(content?.meta_description || '');

  useEffect(() => {
    if (content?.id && activeTab === 'history') {
      setIsLoadingHistory(true);
      generationApi.getContentHistory(content.id)
        .then((res) => setHistory(res.history))
        .finally(() => setIsLoadingHistory(false));
    }
  }, [content?.id, activeTab]);

  const handleApprove = async () => {
    if (content?.id) {
      await generationApi.approveContent(content.id);
      onUpdateSuccess();
    }
  };

  const handleNeedsReview = async () => {
    if (content?.id) {
      await generationApi.markNeedsReview(content.id);
      onUpdateSuccess();
    }
  };

  const handleSaveEdit = async () => {
    if (content?.id) {
      await generationApi.updateContent(content.id, {
        title,
        short_description: shortDesc,
        full_description: fullDesc,
        meta_title: metaTitle,
        meta_description: metaDesc,
      });
      onUpdateSuccess();
      setActiveTab('content');
    }
  };

  const copyFullCopy = () => {
    if (!content) return;
    const text = `${content.title}\n\n${content.short_description}\n\n${content.full_description}`;
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/70 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="relative w-full max-w-5xl max-h-[90vh] bg-white dark:bg-slate-900 rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-800 flex flex-col overflow-hidden">
        
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/60">
          <div className="flex items-center gap-3">
            <h3 className="text-base font-bold text-slate-900 dark:text-white">
              {product.name}
            </h3>
            {content && <StatusBadge status={content.status} />}
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-white hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body - 2 Columns */}
        <div className="flex-1 overflow-y-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
          
          {/* Left Column: Original Product Attributes */}
          <div className="lg:col-span-4 space-y-4 pr-0 lg:pr-4 border-b lg:border-b-0 lg:border-r border-slate-200 dark:border-slate-800">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Original Product Specs
            </h4>

            {product.image_url && (
              <img
                src={product.image_url}
                alt={product.name}
                className="w-full h-40 object-cover rounded-xl border border-slate-200 dark:border-slate-700"
              />
            )}

            <div className="space-y-2 text-xs text-slate-700 dark:text-slate-300">
              <p><strong>SKU:</strong> {product.sku || 'N/A'}</p>
              <p><strong>Brand:</strong> {product.brand || 'N/A'}</p>
              <p><strong>Category:</strong> {product.category}</p>
              <p><strong>Price:</strong> {product.price ? `$${product.price}` : 'N/A'}</p>
              <p><strong>Material:</strong> {product.material || 'N/A'}</p>
              <p><strong>Dimensions:</strong> {product.dimensions || 'N/A'}</p>
              <p><strong>Color / Weight:</strong> {product.color || 'N/A'} / {product.weight || 'N/A'}</p>
              {product.target_audience && <p><strong>Target Audience:</strong> {product.target_audience}</p>}
              {product.usp && <p><strong>USP:</strong> {product.usp}</p>}
            </div>

            {/* Features */}
            {product.features && product.features.length > 0 && (
              <div>
                <label className="block text-[10px] font-bold uppercase text-slate-400 mb-1">Features</label>
                <div className="flex flex-wrap gap-1">
                  {product.features.map((f, i) => (
                    <span key={i} className="px-2 py-0.5 rounded text-[11px] bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                      • {f}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Right Column: AI Content & Tabs */}
          <div className="lg:col-span-8 space-y-4">
            {/* Tabs Header */}
            <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-2">
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setActiveTab('content')}
                  className={`px-3 py-1.5 text-xs font-bold rounded-lg transition-colors ${
                    activeTab === 'content'
                      ? 'bg-blue-600 text-white'
                      : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
                  }`}
                >
                  <FileText className="w-3.5 h-3.5 inline mr-1" /> Generated Content
                </button>
                <button
                  onClick={() => setActiveTab('edit')}
                  className={`px-3 py-1.5 text-xs font-bold rounded-lg transition-colors ${
                    activeTab === 'edit'
                      ? 'bg-blue-600 text-white'
                      : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
                  }`}
                >
                  Edit Copy
                </button>
                <button
                  onClick={() => setActiveTab('history')}
                  className={`px-3 py-1.5 text-xs font-bold rounded-lg transition-colors ${
                    activeTab === 'history'
                      ? 'bg-blue-600 text-white'
                      : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
                  }`}
                >
                  <History className="w-3.5 h-3.5 inline mr-1" /> Version History
                </button>
              </div>

              {content && <ScoreBadge score={content.quality_score} />}
            </div>

            {/* Tab 1: Content Preview */}
            {activeTab === 'content' && content && (
              <div className="space-y-4">
                <div>
                  <label className="text-[10px] font-bold uppercase text-slate-400">Title</label>
                  <h4 className="text-base font-bold text-slate-900 dark:text-white">{content.title}</h4>
                </div>

                <div>
                  <label className="text-[10px] font-bold uppercase text-slate-400">Short Description</label>
                  <p className="text-xs text-slate-700 dark:text-slate-300 italic bg-slate-50 dark:bg-slate-800/50 p-2.5 rounded-lg">
                    "{content.short_description}"
                  </p>
                </div>

                <div>
                  <label className="text-[10px] font-bold uppercase text-slate-400">Full Description</label>
                  <p className="text-xs text-slate-800 dark:text-slate-200 leading-relaxed">
                    {content.full_description}
                  </p>
                </div>

                {content.highlights && content.highlights.length > 0 && (
                  <div>
                    <label className="text-[10px] font-bold uppercase text-slate-400">Highlights</label>
                    <ul className="list-disc list-inside text-xs text-slate-700 dark:text-slate-300 space-y-0.5">
                      {content.highlights.map((h, i) => <li key={i}>{h}</li>)}
                    </ul>
                  </div>
                )}
              </div>
            )}

            {/* Tab 2: Edit Copy */}
            {activeTab === 'edit' && content && (
              <div className="space-y-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Title</label>
                  <input
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className="w-full p-2 text-xs rounded border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Short Description</label>
                  <textarea
                    rows={2}
                    value={shortDesc}
                    onChange={(e) => setShortDesc(e.target.value)}
                    className="w-full p-2 text-xs rounded border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Full Description</label>
                  <textarea
                    rows={4}
                    value={fullDesc}
                    onChange={(e) => setFullDesc(e.target.value)}
                    className="w-full p-2 text-xs rounded border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white outline-none"
                  />
                </div>
                <button
                  onClick={handleSaveEdit}
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-lg flex items-center gap-1.5"
                >
                  <Save className="w-3.5 h-3.5" /> Save Edits
                </button>
              </div>
            )}

            {/* Tab 3: History */}
            {activeTab === 'history' && (
              <div className="space-y-2">
                {isLoadingHistory ? (
                  <p className="text-xs text-slate-400">Loading version history...</p>
                ) : history.length === 0 ? (
                  <p className="text-xs text-slate-400">No previous version snapshots stored.</p>
                ) : (
                  <div className="space-y-2">
                    {history.map((v) => (
                      <div key={v.id} className="p-3 rounded-lg bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs">
                        <div className="flex justify-between font-bold mb-1">
                          <span>Version {v.version_number} - {v.change_type}</span>
                          <span className="text-[10px] text-slate-400">{new Date(v.created_at).toLocaleString()}</span>
                        </div>
                        <p className="text-slate-600 dark:text-slate-300 italic font-mono text-[11px]">
                          "{v.content_snapshot.title}"
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Modal Footer Controls */}
        <div className="flex flex-wrap items-center justify-between p-4 bg-slate-50 dark:bg-slate-800/80 border-t border-slate-200 dark:border-slate-800">
          <div className="flex items-center gap-2">
            <button
              onClick={handleApprove}
              className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-lg flex items-center gap-1.5 cursor-pointer"
            >
              <CheckCircle className="w-3.5 h-3.5" /> Approve
            </button>
            <button
              onClick={handleNeedsReview}
              className="px-3 py-2 bg-amber-100 text-amber-800 font-semibold text-xs rounded-lg flex items-center gap-1.5 cursor-pointer"
            >
              <AlertCircle className="w-3.5 h-3.5" /> Needs Review
            </button>
          </div>

          <button
            onClick={copyFullCopy}
            className="px-3 py-2 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-200 font-semibold text-xs rounded-lg flex items-center gap-1.5"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
            {copied ? 'Copied!' : 'Copy Copywriter Text'}
          </button>
        </div>
      </div>
    </div>
  );
};
