import { apiClient } from './client';

export const exportApi = {
  getProductsCsvUrl: () => `${apiClient.defaults.baseURL}/export/products.csv`,
  getProductsJsonUrl: () => `${apiClient.defaults.baseURL}/export/products.json`,
  getBatchCsvUrl: (batchId: number) => `${apiClient.defaults.baseURL}/export/batch/${batchId}.csv`,
  getBatchJsonUrl: (batchId: number) => `${apiClient.defaults.baseURL}/export/batch/${batchId}.json`,
};
