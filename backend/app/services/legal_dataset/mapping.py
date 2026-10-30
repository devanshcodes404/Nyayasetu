"""
Mapping raw Hugging Face 'Sumitedu/indian-case-laws' schema to the database Judgment model.
Maps candidate fields safely, handling flat and nested keys without assumption of complete text.
"""
from datetime import datetime, date
from typing import Dict, Any, Optional
import re


def parse_iso_or_slash_date(val: Any) -> Optional[date]:
    """Safely extracts date from ISO (YYYY-MM-DD), slash (DD/MM/YYYY), or string formats."""
    if not val:
        return None
    if isinstance(val, (date, datetime)):
        return val if isinstance(val, date) else val.date()
    
    s = str(val).strip()
    if not s:
        return None

    # Try YYYY-MM-DD
    match = re.search(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})", s)
    if match:
        try:
            return date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        except ValueError:
            pass

    # Try DD/MM/YYYY
    match_rev = re.search(r"(\d{1,2})[-/](\d{1,2})[-/](\d{4})", s)
    if match_rev:
        try:
            return date(int(match_rev.group(3)), int(match_rev.group(2)), int(match_rev.group(1)))
        except ValueError:
            pass

    return None


def extract_year(date_val: Optional[date], raw_year: Any) -> Optional[int]:
    """Extracts integer year."""
    if date_val:
        return date_val.year
    if raw_year:
        try:
            y = int(str(raw_year).strip())
            if 1800 <= y <= 2100:
                return y
        except ValueError:
            pass
    return None


def normalize_disposition(disposition_text: Optional[str]) -> Optional[str]:
    """Normalizes Indian court dispositions into canonical categories."""
    if not disposition_text:
        return None
    disp = disposition_text.lower()
    if any(k in disp for k in ["allowed", "granted", "relief granted"]):
        return "Allowed"
    if any(k in disp for k in ["dismissed", "rejected", "devoid of merit"]):
        return "Dismissed"
    if any(k in disp for k in ["disposed", "disposed of", "settled"]):
        return "Disposed"
    if any(k in disp for k in ["remanded", "sent back"]):
        return "Remanded"
    return "Other"


def determine_text_availability(record: Dict[str, Any]) -> str:
    """Accurately classifies text availability without falsely claiming complete text."""
    indexable_text = record.get("indexable_text") or record.get("judgment_text") or record.get("text") or ""
    headnote_text = record.get("headnote_text") or record.get("headnote") or ""

    if len(indexable_text.strip()) > 1000:
        return "FullText"
    elif len(indexable_text.strip()) > 150:
        return "ShortIndexable"
    elif len(headnote_text.strip()) > 50:
        return "HeadnoteOnly"
    elif record.get("source_pdf_s3_url"):
        return "PdfAvailableOnly"
    else:
        return "MetadataOnly"


def map_raw_record_to_judgment(record: Dict[str, Any], source_dataset: str = "Sumitedu/indian-case-laws") -> Dict[str, Any]:
    """
    Maps a raw dictionary from the dataset into the Judgment database schema.
    """
    # Extract identifiers
    external_id = str(record.get("id") or record.get("case_metadata_id") or record.get("parser_record_id") or "").strip()
    case_metadata_id = str(record.get("case_metadata_id") or "") or None
    parser_record_id = str(record.get("parser_record_id") or "") or None

    # Title & Parties
    title = str(
        record.get("case_title")
        or record.get("title")
        or record.get("party_caption")
        or f"Judgment {external_id or 'Unknown'}"
    ).strip()

    petitioner = record.get("party_petitioner") or record.get("petitioner")
    respondent = record.get("party_respondent") or record.get("respondent")
    party_caption = record.get("party_caption")

    # Dates
    decision_date = parse_iso_or_slash_date(record.get("decision_date"))
    registration_date = parse_iso_or_slash_date(record.get("registration_date"))
    decision_year = extract_year(decision_date, record.get("decision_year") or record.get("citation_year"))
    citation_year = extract_year(None, record.get("citation_year"))

    # Court & Jurisdiction
    court_name = str(record.get("court_name") or record.get("court") or "Supreme Court / High Court of India").strip()
    court_code = record.get("court_code") or record.get("source_path_court_code")
    jurisdiction = record.get("jurisdiction") or record.get("source_path_bench") or "India"

    # Outcome & Text
    disposition_text = record.get("disposition_text") or record.get("disposition")
    normalized_outcome = normalize_disposition(disposition_text)
    indexable_text = record.get("indexable_text") or record.get("judgment_text") or record.get("text")
    headnote_text = record.get("headnote_text") or record.get("headnote")
    text_availability = determine_text_availability(record)

    return {
        "source_dataset": source_dataset,
        "external_id": external_id if external_id else None,
        "case_metadata_id": case_metadata_id,
        "parser_record_id": parser_record_id,
        "dataset_source": record.get("dataset_source"),
        "ingestion_split": record.get("ingestion_split"),
        "title": title[:500],
        "petitioner": petitioner[:300] if petitioner else None,
        "respondent": respondent[:300] if respondent else None,
        "party_caption": party_caption,
        "docket_number": record.get("docket_number") or record.get("case_number"),
        "cnr_number": record.get("cnr_number"),
        "neutral_citation": record.get("neutral_citation"),
        "law_report_citation": record.get("law_report_citation"),
        "court_name": court_name[:255],
        "court_code": str(court_code)[:50] if court_code else None,
        "jurisdiction": str(jurisdiction)[:100] if jurisdiction else None,
        "bench_name": record.get("bench_name") or record.get("source_path_bench"),
        "presiding_judge": record.get("presiding_judge"),
        "coram_members": str(record.get("coram_members")) if record.get("coram_members") else None,
        "coram_members_text": record.get("coram_members_text"),
        "decision_date": decision_date,
        "registration_date": registration_date,
        "decision_year": decision_year,
        "citation_year": citation_year,
        "disposition_text": disposition_text,
        "normalized_outcome": normalized_outcome,
        "indexable_text": indexable_text,
        "headnote_text": headnote_text,
        "source_pdf_s3_url": record.get("source_pdf_s3_url"),
        "source_json_s3_url": record.get("source_json_s3_url"),
        "source_relative_path": record.get("source_relative_path"),
        "source_filename": record.get("source_filename"),
        "language_codes": str(record.get("language_codes")) if record.get("language_codes") else "en",
        "text_availability_status": text_availability,
        "verification_status": "SourceDatasetCorpus",
        "quality_json": record.get("quality_json") if isinstance(record.get("quality_json"), dict) else None,
    }

