"""NyayaSetu AI initial migration

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-10-28 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from pgvector.sqlalchemy import Vector

revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 0. pgvector extension
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')

    # 1. users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # 2. cases
    op.create_table(
        'cases',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('case_number', sa.String(length=100), nullable=False),
        sa.Column('court', sa.String(length=255), nullable=False),
        sa.Column('jurisdiction', sa.String(length=100), nullable=False),
        sa.Column('case_type', sa.String(length=100), nullable=False),
        sa.Column('client_name', sa.String(length=255), nullable=False),
        sa.Column('opposing_party', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('filing_date', sa.Date(), nullable=True),
        sa.Column('next_hearing_date', sa.Date(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_cases_owner_id', 'cases', ['owner_id'])
    op.create_index('ix_cases_case_number', 'cases', ['case_number'])
    op.create_index('ix_cases_court', 'cases', ['court'])
    op.create_index('ix_cases_status', 'cases', ['status'])
    op.create_index('ix_cases_next_hearing_date', 'cases', ['next_hearing_date'])
    op.create_index('idx_cases_owner_status', 'cases', ['owner_id', 'status'])

    # 3. documents
    op.create_table(
        'documents',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('case_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('original_filename', sa.String(length=255), nullable=False),
        sa.Column('mime_type', sa.String(length=100), nullable=False),
        sa.Column('storage_path', sa.String(length=500), nullable=False),
        sa.Column('file_size', sa.BigInteger(), nullable=False),
        sa.Column('sha256_checksum', sa.String(length=64), nullable=False),
        sa.Column('processing_status', sa.String(length=50), nullable=False),
        sa.Column('page_count', sa.Integer(), nullable=True),
        sa.Column('is_public_judgment', sa.Boolean(), nullable=False),
        sa.Column('source_url', sa.String(length=500), nullable=True),
        sa.Column('text_availability_status', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_documents_owner_id', 'documents', ['owner_id'])
    op.create_index('ix_documents_case_id', 'documents', ['case_id'])
    op.create_index('ix_documents_checksum', 'documents', ['sha256_checksum'])
    op.create_index('idx_docs_owner_case', 'documents', ['owner_id', 'case_id'])

    # 4. judgments
    op.create_table(
        'judgments',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('source_dataset', sa.String(length=100), nullable=False),
        sa.Column('external_id', sa.String(length=255), nullable=True),
        sa.Column('case_metadata_id', sa.String(length=255), nullable=True),
        sa.Column('parser_record_id', sa.String(length=255), nullable=True),
        sa.Column('dataset_source', sa.String(length=100), nullable=True),
        sa.Column('ingestion_split', sa.String(length=50), nullable=True),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('petitioner', sa.String(length=300), nullable=True),
        sa.Column('respondent', sa.String(length=300), nullable=True),
        sa.Column('party_caption', sa.Text(), nullable=True),
        sa.Column('docket_number', sa.String(length=150), nullable=True),
        sa.Column('cnr_number', sa.String(length=100), nullable=True),
        sa.Column('neutral_citation', sa.String(length=150), nullable=True),
        sa.Column('law_report_citation', sa.String(length=255), nullable=True),
        sa.Column('court_name', sa.String(length=255), nullable=False),
        sa.Column('court_code', sa.String(length=50), nullable=True),
        sa.Column('jurisdiction', sa.String(length=100), nullable=True),
        sa.Column('bench_name', sa.String(length=255), nullable=True),
        sa.Column('presiding_judge', sa.String(length=255), nullable=True),
        sa.Column('coram_members', sa.Text(), nullable=True),
        sa.Column('coram_members_text', sa.Text(), nullable=True),
        sa.Column('decision_date', sa.Date(), nullable=True),
        sa.Column('registration_date', sa.Date(), nullable=True),
        sa.Column('decision_year', sa.Integer(), nullable=True),
        sa.Column('citation_year', sa.Integer(), nullable=True),
        sa.Column('disposition_text', sa.Text(), nullable=True),
        sa.Column('normalized_outcome', sa.String(length=100), nullable=True),
        sa.Column('indexable_text', sa.Text(), nullable=True),
        sa.Column('headnote_text', sa.Text(), nullable=True),
        sa.Column('source_pdf_s3_url', sa.String(length=1000), nullable=True),
        sa.Column('source_json_s3_url', sa.String(length=1000), nullable=True),
        sa.Column('source_relative_path', sa.String(length=500), nullable=True),
        sa.Column('source_filename', sa.String(length=255), nullable=True),
        sa.Column('source_path_court_code', sa.String(length=50), nullable=True),
        sa.Column('source_path_bench', sa.String(length=100), nullable=True),
        sa.Column('source_path_year', sa.String(length=10), nullable=True),
        sa.Column('language_codes', sa.String(length=50), nullable=True),
        sa.Column('text_availability_status', sa.String(length=50), nullable=False),
        sa.Column('verification_status', sa.String(length=50), nullable=False),
        sa.Column('import_timestamp', sa.DateTime(timezone=True), nullable=True),
        sa.Column('normalized_record_json', sa.JSON(), nullable=True),
        sa.Column('parser_json', sa.JSON(), nullable=True),
        sa.Column('quality_json', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('source_dataset', 'external_id', name='uq_dataset_external_id')
    )
    op.create_index('ix_judgments_title', 'judgments', ['title'])
    op.create_index('ix_judgments_court_name', 'judgments', ['court_name'])
    op.create_index('ix_judgments_external_id', 'judgments', ['external_id'])
    op.create_index('ix_judgments_decision_date', 'judgments', ['decision_date'])
    op.create_index('ix_judgments_source_dataset', 'judgments', ['source_dataset'])
    op.create_index('ix_judgments_case_metadata_id', 'judgments', ['case_metadata_id'])
    op.create_index('ix_judgments_petitioner', 'judgments', ['petitioner'])
    op.create_index('ix_judgments_respondent', 'judgments', ['respondent'])
    op.create_index('ix_judgments_docket_number', 'judgments', ['docket_number'])
    op.create_index('ix_judgments_cnr_number', 'judgments', ['cnr_number'])
    op.create_index('ix_judgments_neutral_citation', 'judgments', ['neutral_citation'])
    op.create_index('ix_judgments_law_report_citation', 'judgments', ['law_report_citation'])
    op.create_index('ix_judgments_court_code', 'judgments', ['court_code'])
    op.create_index('ix_judgments_jurisdiction', 'judgments', ['jurisdiction'])
    op.create_index('ix_judgments_decision_year', 'judgments', ['decision_year'])
    op.create_index('ix_judgments_normalized_outcome', 'judgments', ['normalized_outcome'])
    op.create_index('ix_judgments_text_availability_status', 'judgments', ['text_availability_status'])
    op.create_index('idx_judgments_court_year', 'judgments', ['court_name', 'decision_year'])
    op.create_index('idx_judgments_text_avail', 'judgments', ['text_availability_status'])

    # 5. document_chunks
    op.create_table(
        'document_chunks',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('document_id', sa.Integer(), nullable=True),
        sa.Column('judgment_id', sa.Integer(), nullable=True),
        sa.Column('chunk_index', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('page_number', sa.Integer(), nullable=True),
        sa.Column('chunk_metadata', sa.JSON(), nullable=True),
        sa.Column('embedding', Vector(1536), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            '(document_id IS NOT NULL AND judgment_id IS NULL) OR (document_id IS NULL AND judgment_id IS NOT NULL)',
            name='chk_chunk_document_or_judgment'
        ),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['judgment_id'], ['judgments.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_document_chunks_document_id', 'document_chunks', ['document_id'])
    op.create_index('ix_document_chunks_judgment_id', 'document_chunks', ['judgment_id'])
    op.create_index('idx_chunks_doc_chunk', 'document_chunks', ['document_id', 'chunk_index'])
    op.create_index('idx_chunks_judg_chunk', 'document_chunks', ['judgment_id', 'chunk_index'])

    # 6. citations
    op.create_table(
        'citations',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('document_id', sa.Integer(), nullable=True),
        sa.Column('judgment_id', sa.Integer(), nullable=True),
        sa.Column('referenced_judgment_id', sa.Integer(), nullable=True),
        sa.Column('raw_citation', sa.String(length=500), nullable=False),
        sa.Column('normalized_citation', sa.String(length=500), nullable=True),
        sa.Column('context', sa.Text(), nullable=True),
        sa.Column('page_number', sa.Integer(), nullable=True),
        sa.Column('verification_status', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['judgment_id'], ['judgments.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['referenced_judgment_id'], ['judgments.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_citations_doc_id', 'citations', ['document_id'])
    op.create_index('ix_citations_judg_id', 'citations', ['judgment_id'])
    op.create_index('ix_citations_referenced_judgment_id', 'citations', ['referenced_judgment_id'])
    op.create_index('ix_citations_normalized_citation', 'citations', ['normalized_citation'])
    op.create_index('idx_citation_lookup', 'citations', ['normalized_citation'])

    # 7. dataset_import_jobs
    op.create_table(
        'dataset_import_jobs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('dataset_id', sa.String(length=255), nullable=False),
        sa.Column('configuration', sa.String(length=100), nullable=True),
        sa.Column('split', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('is_dry_run', sa.Boolean(), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('records_examined', sa.Integer(), nullable=False),
        sa.Column('records_imported', sa.Integer(), nullable=False),
        sa.Column('records_updated', sa.Integer(), nullable=False),
        sa.Column('records_skipped', sa.Integer(), nullable=False),
        sa.Column('records_rejected', sa.Integer(), nullable=False),
        sa.Column('last_processed_external_id', sa.String(length=255), nullable=True),
        sa.Column('error_summary', sa.Text(), nullable=True),
        sa.Column('job_metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('dataset_import_jobs')
    op.drop_table('citations')
    op.drop_table('document_chunks')
    op.drop_table('judgments')
    op.drop_table('documents')
    op.drop_table('cases')
    op.drop_table('users')

