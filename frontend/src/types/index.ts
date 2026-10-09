export interface Product {
  id?: number;
  sku?: string;
  name: string;
  brand?: string;
  category: string;
  price?: number;
  currency?: string;
  features?: string[];
  specifications?: Record<string, any>;
  target_audience?: string;
  primary_keywords?: string[];
  secondary_keywords?: string[];
  usp?: string;
  image_url?: string;
  material?: string;
  dimensions?: string;
  color?: string;
  weight?: string;
  created_at?: string;
  updated_at?: string;
}

export interface CandidateOutput {
  provider: 'anthropic' | 'gemini';
  provider_label: string;
  model: string;
  source: string;
  content: {
    title: string;
    short_description: string;
    full_description: string;
    highlights: string[];
    meta_title: string;
    meta_description: string;
    suggested_keywords: string[];
    warnings: string[];
  };
  scores: {
    completeness_score: number;
    seo_score: number;
    readability_score: number;
    brand_tone_score: number;
    quality_score: number;
    recommendations?: string[];
  };
  is_winner: boolean;
  strengths?: string[];
}

export interface GeneratedContent {
  id?: number;
  product_id?: number;
  title: string;
  short_description: string;
  full_description: string;
  highlights: string[];
  meta_title: string;
  meta_description: string;
  suggested_keywords: string[];
  warnings: string[];
  tone: string;
  language: string;
  word_count_preference: string;
  seo_score: number;
  readability_score: number;
  completeness_score: number;
  brand_tone_score: number;
  quality_score: number;
  status: 'Draft' | 'Approved' | 'Needs Review';
  generation_source: string;
  candidates_data?: CandidateOutput[];
  decision_rationale?: string;
  api_key_notice?: {
    is_missing: boolean;
    missing_providers: string[];
    message?: string;
  };
  is_human_edited?: boolean;
  generated_at?: string;
  updated_at?: string;
}

export interface ProductCatalogItem {
  product: Product;
  generated_content: GeneratedContent | null;
}

export interface ProductListResponse {
  items: ProductCatalogItem[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface BrandSettings {
  brand_name: string;
  brand_voice: string;
  preferred_words: string[];
  prohibited_words: string[];
  mandatory_disclaimer?: string;
  content_rules?: string;
  default_tone: string;
  default_language: string;
  default_word_count: string;
  keyword_policy: string;
  allow_promotional_claims: boolean;
  max_keywords: number;
  include_feature_bullets: boolean;
  updated_at?: string;
}

export interface ContentVersion {
  id: number;
  version_number: number;
  content_snapshot: Record<string, any>;
  changed_by: string;
  change_type: string;
  created_at: string;
}

export interface BatchItem {
  id: number;
  batch_job_id: number;
  product_id?: number;
  row_number: number;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  error_message?: string;
  generated_content_id?: number;
  created_at: string;
  updated_at: string;
}

export interface BatchJob {
  id: number;
  file_name: string;
  file_type: string;

  total_products: number;
  processed_products: number;
  successful_products: number;
  failed_products: number;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  created_at: string;
  completed_at?: string;
  items?: BatchItem[];
}

export interface DashboardMetrics {
  total_products: number;
  descriptions_generated: number;
  approved_descriptions: number;
  products_needing_review: number;
  avg_seo_score: number;
  avg_quality_score: number;
  batch_jobs_completed: number;
}

export interface ActivityLog {
  id: number;
  product_name: string;
  action: string;
  status: string;
  score: number;
  timestamp: string;
  source: string;
}

export interface AnalyticsData {
  metrics: DashboardMetrics;
  generations_over_time: Array<{ date: string; count: number }>;
  products_by_category: Array<{ category: string; count: number }>;
  quality_score_distribution: Array<{ range: string; count: number }>;
  seo_score_distribution: Array<{ range: string; count: number }>;
  tone_usage: Array<{ tone: string; count: number }>;
  status_distribution: Array<{ status: string; count: number }>;
  recent_activities: ActivityLog[];
}

export interface HealthStatus {
  status: string;
  app_name: string;
  environment: string;
  ai_mode: string;
  claude_configured: boolean;
  anthropic_configured?: boolean;
  gemini_configured?: boolean;
  claude_model?: string;
  gemini_model?: string;
  version: string;
}
