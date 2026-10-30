export interface User {
  id: number;
  full_name: string;
  email: string;
  is_active: boolean;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface LegalCase {
  id: number;
  owner_id: number;
  title: string;
  case_number: string;
  court: string;
  jurisdiction: string;
  case_type: string;
  client_name: string;
  opposing_party: string;
  status: 'Active' | 'Pending' | 'Disposed' | 'Appeal';
  filing_date?: string | null;
  next_hearing_date?: string | null;
  description?: string | null;
  created_at: string;
  updated_at: string;
  documents_count?: number;
}

export interface LegalDocument {
  id: number;
  owner_id: number;
  case_id?: number | null;
  title: string;
  original_filename: string;
  mime_type: string;
  file_size: number;
  sha256_checksum: string;
  processing_status: 'Uploaded' | 'Parsing' | 'Indexed' | 'Failed';
  page_count?: number | null;
  is_public_judgment: boolean;
  source_url?: string | null;
  text_availability_status: 'FullText' | 'ShortIndexable' | 'HeadnoteOnly' | 'ScannedImage' | 'Pending' | 'Failed' | 'MetadataOnly';
  created_at: string;
  updated_at: string;
}

export interface JudgmentListItem {
  id: number;
  title: string;
  petitioner?: string | null;
  respondent?: string | null;
  party_caption?: string | null;
  court_name: string;
  docket_number?: string | null;
  cnr_number?: string | null;
  neutral_citation?: string | null;
  law_report_citation?: string | null;
  decision_date?: string | null;
  decision_year?: number | null;
  disposition_text?: string | null;
  normalized_outcome?: string | null;
  text_availability_status: 'FullText' | 'ShortIndexable' | 'HeadnoteOnly' | 'MetadataOnly' | 'PdfAvailableOnly';
  verification_status: string;
  has_source_pdf: boolean;
  headnote_snippet?: string | null;
}

export interface JudgmentDetail extends JudgmentListItem {
  source_dataset: string;
  external_id?: string | null;
  case_metadata_id?: string | null;
  parser_record_id?: string | null;
  court_code?: string | null;
  jurisdiction?: string | null;
  bench_name?: string | null;
  presiding_judge?: string | null;
  coram_members?: string | null;
  coram_members_text?: string | null;
  registration_date?: string | null;
  citation_year?: number | null;
  indexable_text?: string | null;
  headnote_text?: string | null;
  source_pdf_s3_url?: string | null;
  source_json_s3_url?: string | null;
  source_relative_path?: string | null;
  language_codes?: string | null;
  import_timestamp?: string | null;
  quality_json?: Record<string, any> | null;
}

export interface PaginatedResult<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface DashboardMetrics {
  my_active_cases: number;
  my_total_documents: number;
  my_upcoming_hearings_count: number;
  public_judgments_imported: number;
  public_judgments_searchable: number;
  public_courts_count: number;
  recent_cases: Array<{
    id: number;
    title: string;
    case_number: string;
    court: string;
    status: string;
    next_hearing_date?: string | null;
  }>;
  upcoming_hearings: Array<{
    case_id: number;
    title: string;
    case_number: string;
    court: string;
    date: string;
  }>;
}

export interface DatasetStatus {
  dataset_id: string;
  total_judgments_imported: number;
  judgments_with_full_text: number;
  judgments_with_headnotes: number;
  metadata_only_judgments: number;
  courts_represented: number;
  latest_import_job?: {
    id: number;
    status: string;
    is_dry_run: boolean;
    records_imported: number;
    records_examined: number;
    started_at?: string | null;
    completed_at?: string | null;
  } | null;
  storage_type: string;
  is_ready_for_search: boolean;
}

export interface CitationItem {
  id: number;
  raw_citation: string;
  normalized_citation?: string | null;
  context?: string | null;
  page_number?: number | null;
  verification_status: string;
  referenced_judgment_id?: number | null;
  created_at: string;
}

