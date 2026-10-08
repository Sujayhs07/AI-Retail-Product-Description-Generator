import { apiClient } from './client';
import { BrandSettings } from '../types';

export const settingsApi = {
  getBrandSettings: async (): Promise<BrandSettings> => {
    const response = await apiClient.get<BrandSettings>('/settings/brand');
    return response.data;
  },

  updateBrandSettings: async (settings: Partial<BrandSettings>): Promise<BrandSettings> => {
    const response = await apiClient.put<BrandSettings>('/settings/brand', settings);
    return response.data;
  },

  resetBrandSettings: async (): Promise<BrandSettings> => {
    const response = await apiClient.post<BrandSettings>('/settings/brand/reset');
    return response.data;
  }
};
