from app.models.case import LegalCase

def test_case_lifecycle_and_ownership(client, auth_headers, test_user, db_session):
    # Create Case
    create_payload = {
        "title": "Sunil Gupta v. Union Bank of India",
        "case_number": "OA/504/2023",
        "court": "Debts Recovery Tribunal, Delhi",
        "jurisdiction": "Recovery",
        "case_type": "Banking",
        "client_name": "Sunil Gupta",
        "opposing_party": "Union Bank of India",
        "status": "Active",
        "description": "Securitisation application under SARFAESI Act.",
    }
    create_resp = client.post("/api/v1/cases", json=create_payload, headers=auth_headers)
    assert create_resp.status_code == 201
    case_data = create_resp.json()
    case_id = case_data["id"]
    assert case_data["case_number"] == "OA/504/2023"

    # List cases
    list_resp = client.get("/api/v1/cases", headers=auth_headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    # Get single case
    get_resp = client.get(f"/api/v1/cases/{case_id}", headers=auth_headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Sunil Gupta v. Union Bank of India"

    # Update case
    update_resp = client.patch(f"/api/v1/cases/{case_id}", json={"status": "Pending"}, headers=auth_headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "Pending"

    # Delete case
    del_resp = client.delete(f"/api/v1/cases/{case_id}", headers=auth_headers)
    assert del_resp.status_code == 204

    # Verify deleted
    not_found_resp = client.get(f"/api/v1/cases/{case_id}", headers=auth_headers)
    assert not_found_resp.status_code == 404

