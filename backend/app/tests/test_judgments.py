from app.models.judgment import Judgment

def test_judgment_search_and_filters(client, db_session):
    # Seed a judgment
    j = Judgment(
        source_dataset="Sumitedu/indian-case-laws",
        external_id="TEST-SC-01",
        title="Union of India v. Association for Democratic Reforms",
        court_name="Supreme Court of India",
        neutral_citation="2002 INSC 225",
        decision_year=2002,
        disposition_text="Appeal Dismissed. Citizens have right to know antecedents of candidates.",
        normalized_outcome="Dismissed",
        text_availability_status="FullText",
        verification_status="SourceDatasetCorpus",
    )
    db_session.add(j)
    db_session.commit()

    # Search keyword
    res = client.get("/api/v1/judgments/search?q=Democratic")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 1
    assert data["items"][0]["neutral_citation"] == "2002 INSC 225"

    # Search with year filter
    res_year = client.get("/api/v1/judgments/search?year=2002")
    assert res_year.status_code == 200
    assert res_year.json()["total"] >= 1

    # Search not found
    res_none = client.get("/api/v1/judgments/search?q=NonExistentKeywordXYZ")
    assert res_none.status_code == 200
    assert res_none.json()["total"] == 0

