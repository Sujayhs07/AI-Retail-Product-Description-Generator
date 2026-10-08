import { apiClient } from './client';
import { AnalyticsData, HealthStatus } from '../types';

export const analyticsApi = {
  getAnalytics: async (category?: string, brand?: string): Promise<AnalyticsData> => {
    const response = await apiClient.get<AnalyticsData>('/analytics/overview', {
      params: { category, brand }
    });
    return response.data;
  },

  getHealthStatus: async (): Promise<HealthStatus> => {
    const response = await apiClient.get<HealthStatus>('/health');
    return response.data;
  }
};
