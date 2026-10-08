import { apiClient } from './client';
import { Product, ProductListResponse, ProductCatalogItem } from '../types';

export const productsApi = {
  getProducts: async (params?: {
    search?: string;
    category?: string;
    brand?: string;
    status?: string;
    tone?: string;
    min_quality_score?: number;
    min_seo_score?: number;
    sort_by?: string;
    page?: number;
    page_size?: number;
  }): Promise<ProductListResponse> => {
    const response = await apiClient.get<ProductListResponse>('/products', { params });
    return response.data;
  },

  getProduct: async (id: number): Promise<ProductCatalogItem> => {
    const response = await apiClient.get<ProductCatalogItem>(`/products/${id}`);
    return response.data;
  },

  createProduct: async (product: Product): Promise<Product> => {
    const response = await apiClient.post<Product>('/products', product);
    return response.data;
  },

  updateProduct: async (id: number, product: Partial<Product>): Promise<Product> => {
    const response = await apiClient.put<Product>(`/products/${id}`, product);
    return response.data;
  },

  deleteProduct: async (id: number): Promise<void> => {
    await apiClient.delete(`/products/${id}`);
  }
};
