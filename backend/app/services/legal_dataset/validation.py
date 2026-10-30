"""
Validation and rejection rules for imported case-law records.
Prevents blank entries, corrupt data, or malformed identifiers from breaking batch imports.
"""
from typing import Dict, Any, Tuple, Optional


def validate_judgment_record(mapped: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Validates mapped judgment fields.
    Returns (is_valid, rejection_reason).
    """
    if not mapped.get("title") or not mapped["title"].strip():
        return False, "Missing required case title"

    if not mapped.get("court_name") or not mapped["court_name"].strip():
        return False, "Missing required court name"

    # Must have at least an external_id or a docket number or a title longer than 5 chars
    has_identifier = bool(mapped.get("external_id") or mapped.get("docket_number") or mapped.get("cnr_number"))
    if not has_identifier and len(mapped["title"]) < 5:
        return False, "No valid case identifier or meaningful title"

    # Year validation if present
    year = mapped.get("decision_year")
    if year is not None and (year < 1800 or year > 2100):
        return False, f"Invalid decision year: {year}"

    return True, None

