from backend.models.schemas import DocumentRequest, DocumentResponse
from backend.services.ai_generator import generate_document
from backend.utils.text_utils import make_title


def create_document(request: DocumentRequest) -> DocumentResponse:
    content, source = generate_document(request)
    return DocumentResponse(
        title=make_title(request.document_type),
        content=content,
        source=source,
    )
