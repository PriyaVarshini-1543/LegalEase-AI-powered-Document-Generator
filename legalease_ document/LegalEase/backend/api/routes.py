from fastapi import APIRouter, Depends

from backend.core.config import Settings
from backend.dependencies import get_app_settings
from backend.models.schemas import DocumentRequest, DocumentResponse, HealthResponse
from backend.services.document_service import create_document

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health(settings: Settings = Depends(get_app_settings)) -> HealthResponse:
    return HealthResponse(
        status="ok",
        app=settings.app_name,
        version=settings.app_version,
    )


@router.post("/documents/generate", response_model=DocumentResponse)
def generate_document(request: DocumentRequest) -> DocumentResponse:
    return create_document(request)
