import React, { useState, useEffect } from 'react';
import { productsApi, generationApi } from '../api';
import { ProductCatalogItem } from '../types';
import { CatalogueFilterBar } from '../components/catalogue/CatalogueFilterBar';
import { ProductGrid } from '../components/catalogue/ProductGrid';
import { ProductDetailModal } from '../components/catalogue/ProductDetailModal';
import { ShoppingBag, ChevronLeft, ChevronRight } from 'lucide-react';

export const CataloguePage: React.FC = () => {
  const [items, setItems] = useState<ProductCatalogItem[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [isLoading, setIsLoading] = useState(true);

  // Filters State
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('All');
  const [brand, setBrand] = useState('All');
  const [status, setStatus] = useState('All');
  const [tone, setTone] = useState('All');
  const [minQualityScore, setMinQualityScore] = useState(0);
  const [sortBy, setSortBy] = useState('newest');

  // Selected Item for Detail Modal
  const [selectedItem, setSelectedItem] = useState<ProductCatalogItem | null>(null);

  const categories = [
    'Electronics', 'Fashion', 'Home and Kitchen', 'Beauty and Personal Care',
    'Sports and Fitness', 'Grocery', 'Furniture', 'Travel Accessories'
  ];
  const brands = ['AuraSound', 'PulseTrack', 'UrbanShield', 'BaristaCraft', 'RadiantGlow', 'ZenMat', 'Organic Peak', 'HavenNordic', 'NomadVoyage'];

  const fetchProducts = () => {
    setIsLoading(true);
    productsApi
      .getProducts({
        search: search || undefined,
        category: category !== 'All' ? category : undefined,
        brand: brand !== 'All' ? brand : undefined,
        status: status !== 'All' ? status : undefined,
        tone: tone !== 'All' ? tone : undefined,
        min_quality_score: minQualityScore > 0 ? minQualityScore : undefined,
        sort_by: sortBy,
        page,
        page_size: 9,
      })
      .then((res) => {
        setItems(res.items);
        setTotal(res.total);
        setTotalPages(res.total_pages);
      })
      .finally(() => setIsLoading(false));
  };

  useEffect(() => {
    fetchProducts();
  }, [search, category, brand, status, tone, minQualityScore, sortBy, page]);

  const handleApprove = async (contentId: number) => {
    await generationApi.approveContent(contentId);
    fetchProducts();
  };

  const handleNeedsReview = async (contentId: number) => {
    await generationApi.markNeedsReview(contentId);
    fetchProducts();
  };

  const handleDelete = async (productId: number) => {
    if (confirm('Are you sure you want to delete this product record?')) {
      await productsApi.deleteProduct(productId);
      fetchProducts();
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200 dark:border-slate-800">
        <div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <ShoppingBag className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            Product Catalogue & Review Workflow
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Search, filter, preview, edit, approve, and manage generated product descriptions ({total} items total)
          </p>
        </div>
      </div>

      {/* Filter Bar */}
      <CatalogueFilterBar
        search={search}
        setSearch={setSearch}
        category={category}
        setCategory={setCategory}
        brand={brand}
        setBrand={setBrand}
        status={status}
        setStatus={setStatus}
        tone={tone}
        setTone={setTone}
        minQualityScore={minQualityScore}
        setMinQualityScore={setMinQualityScore}
        sortBy={sortBy}
        setSortBy={setSortBy}
        categories={categories}
        brands={brands}
      />

      {/* Product Grid */}
      {isLoading ? (
        <div className="flex items-center justify-center h-48 text-slate-400">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <ProductGrid
          items={items}
          onSelect={setSelectedItem}
          onApprove={handleApprove}
          onNeedsReview={handleNeedsReview}
          onDelete={handleDelete}
        />
      )}

      {/* Pagination Controls */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between pt-4 border-t border-slate-200 dark:border-slate-800 text-xs font-semibold">
          <span className="text-slate-500">
            Showing Page {page} of {totalPages} ({total} products)
          </span>
          <div className="flex items-center gap-2">
            <button
              disabled={page <= 1}
              onClick={() => setPage((p) => Math.max(p - 1, 1))}
              className="px-3 py-1.5 rounded-lg border border-slate-300 dark:border-slate-700 disabled:opacity-40 flex items-center gap-1 hover:bg-slate-100 dark:hover:bg-slate-800"
            >
              <ChevronLeft className="w-4 h-4" /> Previous
            </button>
            <button
              disabled={page >= totalPages}
              onClick={() => setPage((p) => Math.min(p + 1, totalPages))}
              className="px-3 py-1.5 rounded-lg border border-slate-300 dark:border-slate-700 disabled:opacity-40 flex items-center gap-1 hover:bg-slate-100 dark:hover:bg-slate-800"
            >
              Next <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* Detail Modal */}
      {selectedItem && (
        <ProductDetailModal
          item={selectedItem}
          onClose={() => setSelectedItem(null)}
          onUpdateSuccess={() => {
            fetchProducts();
            setSelectedItem(null);
          }}
        />
      )}
    </div>
  );
};
