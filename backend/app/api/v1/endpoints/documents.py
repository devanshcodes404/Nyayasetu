"""
Document management endpoints: upload, list, retrieve, delete.
Integrates file parsing, checksum calculation, and safe Vercel Blob / local storage.
"""
import hashlib
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.session import get_db
from app.models.document import LegalDocument
from app.models.case import LegalCase
from app.models.user import User
from app.schemas.document import DocumentResponse
from app.api.v1.dependencies import get_current_user
from app.services.documents.storage import storage_service
from app.services.documents.parser import DocumentParser
from app.core.config import settings

router = APIRouter()


@router.get("", response_model=List[DocumentResponse])
def list_documents(
    case_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(LegalDocument).filter(LegalDocument.owner_id == current_user.id)
    if case_id:
        query = query.filter(LegalDocument.case_id == case_id)
    docs = query.order_by(desc(LegalDocument.created_at)).all()
    return [DocumentResponse.model_validate(d) for d in docs]


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    case_id: Optional[int] = Form(None),
    title: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Verify case ownership if case_id provided
    if case_id:
        case = db.query(LegalCase).filter(LegalCase.id == case_id, LegalCase.owner_id == current_user.id).first()
        if not case:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated case not found.")

    # Read and validate file size
    content = await file.read()
    file_size = len(content)
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if file_size > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum upload size of {settings.MAX_UPLOAD_SIZE_MB}MB.",
        )

    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    # Compute SHA-256 checksum
    checksum = hashlib.sha256(content).hexdigest()

    # Parse content
    mime_type = file.content_type or "application/octet-stream"
    original_filename = file.filename or "uploaded_document"
    doc_title = title.strip() if title and title.strip() else original_filename

    parse_result = DocumentParser.parse_bytes(content, mime_type, original_filename)
    
    # Store durable file
    storage_info = storage_service.save_file(content, original_filename, mime_type)

    doc = LegalDocument(
        owner_id=current_user.id,
        case_id=case_id,
        title=doc_title,
        original_filename=original_filename,
        mime_type=mime_type,
        storage_path=storage_info["storage_path"],
        file_size=file_size,
        sha256_checksum=checksum,
        processing_status="Indexed" if parse_result["status"] in ["FullText", "ScannedImage"] else "Failed",
        page_count=parse_result.get("page_count", 1),
        is_public_judgment=False,
        text_availability_status=parse_result.get("status", "Pending"),
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return DocumentResponse.model_validate(doc)


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    doc = db.query(LegalDocument).filter(
        LegalDocument.id == document_id,
        LegalDocument.owner_id == current_user.id,
    ).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")
    return DocumentResponse.model_validate(doc)


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    doc = db.query(LegalDocument).filter(
        LegalDocument.id == document_id,
        LegalDocument.owner_id == current_user.id,
    ).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

    # Remove stored physical/blob file
    storage_service.delete_file(doc.storage_path)

    db.delete(doc)
    db.commit()
    return None

