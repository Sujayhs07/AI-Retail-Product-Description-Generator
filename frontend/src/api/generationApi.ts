import { apiClient } from './client';
import { Product, GeneratedContent, ContentVersion } from '../types';

export interface GenerateRequestPayload {
  product: Product;
  tone: string;
  language: string;
  word_count_preference: string;
  save_to_catalog: boolean;
  engine?: string;
}

export interface GenerateResponsePayload {
  generated_content: GeneratedContent & { scores: any; decision_summary?: any };
}

export const generationApi = {
  generateDescription: async (payload: GenerateRequestPayload): Promise<GenerateResponsePayload> => {
    const response = await apiClient.post<GenerateResponsePayload>('/generate-description', payload);
    return response.data;
  },

  regenerateDescription: async (payload: {
    product_id: number;
    content_id: number;
    tone?: string;
    language?: string;
    word_count_preference?: string;
    engine?: string;
  }): Promise<GeneratedContent> => {
    const response = await apiClient.post<GeneratedContent>('/regenerate-description', payload);
    return response.data;
  },

  updateContent: async (contentId: number, update: Partial<GeneratedContent>): Promise<GeneratedContent> => {
    const response = await apiClient.put<GeneratedContent>(`/generated-content/${contentId}`, update);
    return response.data;
  },

  approveContent: async (contentId: number): Promise<GeneratedContent> => {
    const response = await apiClient.post<GeneratedContent>(`/generated-content/${contentId}/approve`);
    return response.data;
  },

  markNeedsReview: async (contentId: number): Promise<GeneratedContent> => {
    const response = await apiClient.post<GeneratedContent>(`/generated-content/${contentId}/needs-review`);
    return response.data;
  },

  getContentHistory: async (contentId: number): Promise<{ history: ContentVersion[] }> => {
    const response = await apiClient.get<{ history: ContentVersion[] }>(`/generated-content/${contentId}/history`);
    return response.data;
  }
};
