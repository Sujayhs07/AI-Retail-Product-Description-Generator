import React from 'react';
import { ProductCatalogItem } from '../../types';
import { ScoreBadge } from '../common/ScoreBadge';
import { StatusBadge } from '../common/StatusBadge';
import { formatCurrency } from '../../lib/utils';
import {
  Eye,
  CheckCircle,
  AlertCircle,
  Trash2,
  Cpu,
  Copy,
  Check,
  Package
} from 'lucide-react';

interface ProductGridProps {
  items: ProductCatalogItem[];
  onSelect: (item: ProductCatalogItem) => void;
  onApprove: (id: number) => void;
  onNeedsReview: (id: number) => void;
  onDelete: (id: number) => void;
}

export const ProductGrid: React.FC<ProductGridProps> = ({
  items,
  onSelect,
  onApprove,
  onNeedsReview,
  onDelete,
}) => {
  const [copiedId, setCopiedId] = React.useState<number | null>(null);

  const handleCopy = (id: number, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  if (items.length === 0) {
    return (
      <div className="text-center py-12 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 p-8">
        <Package className="w-12 h-12 text-slate-300 dark:text-slate-600 mx-auto mb-3" />
        <h3 className="text-sm font-bold text-slate-700 dark:text-slate-300">No products match your filters</h3>
        <p className="text-xs text-slate-500 mt-1">Try resetting your search term or filter options.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      {items.map(({ product, generated_content: content }) => (
        <div
          key={product.id}
          className="glass-card rounded-2xl overflow-hidden flex flex-col justify-between border border-slate-200/90 dark:border-slate-800/90 transition-all duration-200"
        >
          {/* Card Top */}
          <div className="p-5 space-y-3">
            <div className="flex items-start justify-between gap-2">
              <div className="flex gap-3">
                {product.image_url ? (
                  <img
                    src={product.image_url}
                    alt={product.name}
                    className="w-14 h-14 rounded-xl object-cover border border-slate-200 dark:border-slate-800 shrink-0 shadow-2xs"
                  />
                ) : (
                  <div className="w-14 h-14 rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-800 flex items-center justify-center text-slate-400 shrink-0">
                    <Package className="w-6 h-6" />
                  </div>
                )}
                <div>
                  <h4 className="text-sm font-bold text-slate-900 dark:text-white line-clamp-1">
                    {product.name}
                  </h4>
                  <div className="flex items-center gap-1.5 text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                    <span>{product.brand || 'No Brand'}</span>
                    <span>•</span>
                    <span className="font-semibold text-blue-600 dark:text-blue-400">{product.category}</span>
                  </div>
                  <p className="text-xs font-bold text-slate-700 dark:text-slate-300 mt-1">
                    {formatCurrency(product.price, product.currency)}
                  </p>
                </div>
              </div>

              {content && <StatusBadge status={content.status} size="sm" />}
            </div>

            {/* Generated Copy Snippet */}
            {content ? (
              <div className="space-y-2 pt-2 border-t border-slate-100 dark:border-slate-800">
                <p className="text-xs text-slate-600 dark:text-slate-300 line-clamp-2 italic">
                  "{content.short_description}"
                </p>

                <div className="flex items-center justify-between pt-1">
                  <ScoreBadge score={content.quality_score} size="sm" />
                  <span className="inline-flex items-center gap-1 text-[10px] text-slate-400 font-medium">
                    <Cpu className="w-3 h-3 text-cyan-500" />
                    {content.generation_source.includes('gemini')
                      ? 'Gemini 3.5'
                      : content.generation_source.includes('claude')
                      ? 'Claude 3.5'
                      : content.generation_source.includes('dual')
                      ? 'Dual-AI'
                      : 'Mock Engine'}
                  </span>
                </div>
              </div>
            ) : (
              <div className="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-xl text-center text-xs text-slate-400 italic">
                Description not yet generated
              </div>
            )}
          </div>

          {/* Card Action Footer */}
          <div className="px-4 py-3 bg-slate-50/80 dark:bg-slate-800/60 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
            <button
              onClick={() => onSelect({ product, generated_content: content })}
              className="flex items-center gap-1 text-xs font-bold text-blue-600 dark:text-blue-400 hover:underline"
            >
              <Eye className="w-3.5 h-3.5" /> Preview & Edit
            </button>

            <div className="flex items-center gap-1">
              {content && (
                <>
                  <button
                    onClick={() => handleCopy(content.id!, `${content.title}\n\n${content.full_description}`)}
                    className="p-1.5 rounded hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300"
                    title="Copy Text"
                  >
                    {copiedId === content.id ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
                  </button>

                  <button
                    onClick={() => onApprove(content.id!)}
                    className="p-1.5 rounded hover:bg-emerald-100 text-emerald-600 dark:hover:bg-emerald-950/40"
                    title="Approve Description"
                  >
                    <CheckCircle className="w-3.5 h-3.5" />
                  </button>

                  <button
                    onClick={() => onNeedsReview(content.id!)}
                    className="p-1.5 rounded hover:bg-amber-100 text-amber-600 dark:hover:bg-amber-950/40"
                    title="Mark Needs Review"
                  >
                    <AlertCircle className="w-3.5 h-3.5" />
                  </button>
                </>
              )}

              <button
                onClick={() => product.id && onDelete(product.id)}
                className="p-1.5 rounded hover:bg-rose-100 text-rose-500 dark:hover:bg-rose-950/40"
                title="Delete Product"
              >
                <Trash2 className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};
