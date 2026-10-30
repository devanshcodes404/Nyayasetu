from app.services.legal_dataset.mapping import (
    map_raw_record_to_judgment,
    parse_iso_or_slash_date,
    normalize_disposition,
    determine_text_availability,
)
from app.services.legal_dataset.validation import validate_judgment_record


def test_schema_mapping_and_normalization():
    raw_sample = {
        "id": "HC-BOM-1029",
        "case_title": "Ramesh v. Suresh & Ors.",
        "court_name": "Bombay High Court",
        "decision_date": "2023-04-15",
        "disposition_text": "Petition Allowed. Impugned decree set aside.",
        "indexable_text": "A" * 1500,  # > 1000 chars -> FullText
    }
    mapped = map_raw_record_to_judgment(raw_sample)
    assert mapped["title"] == "Ramesh v. Suresh & Ors."
    assert mapped["decision_year"] == 2023
    assert mapped["normalized_outcome"] == "Allowed"
    assert mapped["text_availability_status"] == "FullText"

    # Validation
    is_valid, reason = validate_judgment_record(mapped)
    assert is_valid is True
    assert reason is None


def test_validation_rejection_rules():
    # Empty title
    is_valid, reason = validate_judgment_record({"title": "", "court_name": "Delhi High Court"})
    assert is_valid is False
    assert "title" in reason.lower()

    # Invalid year
    is_valid_yr, reason_yr = validate_judgment_record({
        "title": "State v. Person",
        "court_name": "Court",
        "decision_year": 3050,
        "external_id": "ABC",
    })
    assert is_valid_yr is False
    assert "year" in reason_yr.lower()

