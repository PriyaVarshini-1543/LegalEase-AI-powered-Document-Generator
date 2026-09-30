from typing import Literal
from pydantic import BaseModel, Field, field_validator


DocumentType = Literal[
    "Rental Agreement",
    "Employment Agreement",
    "Non-Disclosure Agreement",
    "Affidavit",
    "Demand Letter",
    "General Legal Letter",
]


class DocumentRequest(BaseModel):
    document_type: DocumentType
    client_name: str = Field(..., min_length=1, max_length=200)
    jurisdiction: str = Field(default="India", min_length=1, max_length=200)
    facts: str = Field(..., min_length=10, max_length=12000)
    tone: Literal["Formal", "Plain English", "Professional"] = "Formal"

    @field_validator("client_name", "jurisdiction", "facts")
    @classmethod
    def strip_values(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be blank.")
        return value


class DocumentResponse(BaseModel):
    title: str
    content: str
    source: Literal["openai", "local"]


class HealthResponse(BaseModel):
    status: str
    app: str
    version: str
