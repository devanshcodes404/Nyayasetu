"""
Seeds initial demo data (test user, demo cases, sample judgments).
Run via:
python scripts/seed_demo.py
"""
import sys
import os
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import SessionLocal
from app.models.user import User
from app.models.case import LegalCase
from app.core.security import hash_password
from app.services.legal_dataset.importer import DatasetImporter


def seed_demo():
    print("Seeding NyayaSetu AI demo environment...")
    db = SessionLocal()
    try:
        # Create demo advocate user
        demo_user = db.query(User).filter(User.email == "advocate@nyayasetu.ai").first()
        if not demo_user:
            demo_user = User(
                full_name="Advocate Vikramaditya Verma",
                email="advocate@nyayasetu.ai",
                password_hash=hash_password("NyayaSetu@2026"),
                is_active=True,
            )
            db.add(demo_user)
            db.commit()
            db.refresh(demo_user)
            print(f"Created demo advocate user: {demo_user.email} (Password: NyayaSetu@2026)")

        # Create demo legal cases
        case1 = db.query(LegalCase).filter(LegalCase.case_number == "CA/4102/2021").first()
        if not case1:
            case1 = LegalCase(
                owner_id=demo_user.id,
                title="State of Maharashtra v. Union of India",
                case_number="CA/4102/2021",
                court="Supreme Court of India",
                jurisdiction="Appellate",
                case_type="Constitutional",
                client_name="State of Maharashtra",
                opposing_party="Union of India & Ors.",
                status="Active",
                filing_date=date(2021, 8, 14),
                next_hearing_date=date(2026, 11, 15),
                description="Constitutional challenge regarding exercise of gubernatorial discretion under Article 163.",
            )
            db.add(case1)

        case2 = db.query(LegalCase).filter(LegalCase.case_number == "ARB/482/2022").first()
        if not case2:
            case2 = LegalCase(
                owner_id=demo_user.id,
                title="TechServe Solutions v. Bharat Telecom",
                case_number="ARB/482/2022",
                court="High Court of Delhi",
                jurisdiction="Commercial",
                case_type="Arbitration",
                client_name="TechServe Solutions Pvt. Ltd.",
                opposing_party="Bharat Telecom Infrastructure Corp.",
                status="Pending",
                filing_date=date(2022, 4, 10),
                next_hearing_date=date(2026, 12, 5),
                description="Petition under Section 11(6) for appointment of sole arbitrator following dispute over unilateral nomination.",
            )
            db.add(case2)

        db.commit()
        print("Demo cases verified.")

        # Ingest initial sample judgments
        print("Importing initial sample judgments from corpus fixtures...")
        importer = DatasetImporter(db=db, limit=10, dry_run=False, resume=False)
        res = importer.run()
        print(f"Sample judgment import result: {res['imported']} new records imported.")

        print("Demo seeding complete!")
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo()

