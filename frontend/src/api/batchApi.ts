import { apiClient } from './client';
import { BatchJob } from '../types';

export const batchApi = {
  uploadBatchFile: async (file: File): Promise<BatchJob> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post<BatchJob>('/batch/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  getBatchJob: async (batchId: number): Promise<BatchJob> => {
    const response = await apiClient.get<BatchJob>(`/batch/${batchId}`);
    return response.data;
  },

  startBatchGeneration: async (
    batchId: number,
    options?: { tone?: string; language?: string; word_count_preference?: string }
  ): Promise<{ message: string; batch_id: number; status: string }> => {
    const response = await apiClient.post(`/batch/${batchId}/generate`, options || {});
    return response.data;
  },

  retryFailedItems: async (batchId: number): Promise<{ message: string; batch_id: number }> => {
    const response = await apiClient.post(`/batch/${batchId}/retry-failed`);
    return response.data;
  },

  getBatchResults: async (batchId: number): Promise<any> => {
    const response = await apiClient.get(`/batch/${batchId}/results`);
    return response.data;
  }
};
