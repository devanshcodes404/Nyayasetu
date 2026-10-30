from app.services.legal_dataset.importer import DatasetImporter
from app.models.judgment import Judgment


def test_idempotent_import_and_deduplication(db_session):
    importer = DatasetImporter(
        db=db_session,
        limit=5,
        streaming=False,
        dry_run=False,
        resume=False,
    )
    result1 = importer.run()
    assert result1["status"] == "Completed"
    first_imported = result1["imported"]
    assert first_imported > 0

    # Second run should skip duplicates and not inflate database count
    importer2 = DatasetImporter(
        db=db_session,
        limit=5,
        streaming=False,
        dry_run=False,
        resume=False,
    )
    result2 = importer2.run()
    assert result2["status"] == "Completed"
    assert result2["skipped"] == first_imported
    assert result2["imported"] == 0


def test_dry_run_behavior(db_session):
    initial_count = db_session.query(Judgment).count()
    importer_dry = DatasetImporter(
        db=db_session,
        limit=2,
        streaming=False,
        dry_run=True,
        resume=False,
    )
    res_dry = importer_dry.run()
    assert res_dry["is_dry_run"] is True
    post_count = db_session.query(Judgment).count()
    assert post_count == initial_count
