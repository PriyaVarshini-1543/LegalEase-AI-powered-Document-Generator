import logging

from backend.core.config import get_settings
from backend.models.schemas import DocumentRequest
from backend.utils.text_utils import clean_text

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are LegalEase, an AI-assisted legal document drafting assistant.
Draft a structured, professional document from the user's facts.

Important:
- Do not claim to be a lawyer.
- Do not invent statutes, case law, court rules, registration numbers, addresses,
  dates, parties, or legal citations that were not supplied.
- If an important fact is missing, use a clear bracketed placeholder such as [DATE]
  or [FULL ADDRESS].
- Keep the document practical and readable.
- Add a short "Review Notes" section listing facts that should be verified.
- The output is a draft for human/legal-professional review, not legal advice.
""".strip()


def _local_fallback(request: DocumentRequest) -> str:
    return clean_text(
        f"""\
{request.document_type.upper()}

Prepared for: {request.client_name}
Jurisdiction: {request.jurisdiction}
Tone: {request.tone}

1. PARTIES
The parties and their full legal details should be inserted or verified before use.

2. PURPOSE
This document is prepared based on the information supplied by the user.

3. FACTS / TERMS
{request.facts}

4. OBLIGATIONS AND UNDERSTANDINGS
The parties should clearly state their respective rights, duties, payment terms,
deadlines, confidentiality requirements, termination conditions, and other
material obligations applicable to the matter.

5. GOVERNING LAW AND JURISDICTION
[INSERT APPLICABLE LAW AND JURISDICTION AFTER PROFESSIONAL REVIEW]

6. SIGNATURES
Party/Signatory 1: ______________________________
Name: [FULL NAME]
Date: [DATE]

Party/Signatory 2: ______________________________
Name: [FULL NAME]
Date: [DATE]

REVIEW NOTES
- Verify every name, date, amount, address, and factual statement.
- Confirm the applicable law and jurisdiction.
- Add any mandatory clauses, notices, witnesses, stamps, registrations, or
  supporting documents required for the specific matter.
- Obtain professional legal review before signing, filing, or relying on this draft.
"""
    )


def _openai_generate(request: DocumentRequest, api_key: str, model: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    user_prompt = f"""
Create a {request.document_type}.

Prepared for: {request.client_name}
Jurisdiction: {request.jurisdiction}
Tone: {request.tone}

User-provided facts and requested terms:
{request.facts}
""".strip()

    response = client.responses.create(
        model=model,
        instructions=SYSTEM_PROMPT,
        input=user_prompt,
    )
    output = getattr(response, "output_text", None)
    if not output:
        raise RuntimeError("The AI service returned no text.")
    return clean_text(output)


def generate_document(request: DocumentRequest) -> tuple[str, str]:
    settings = get_settings()

    if not settings.openai_api_key:
        logger.info("OPENAI_API_KEY not configured; using local fallback.")
        return _local_fallback(request), "local"

    try:
        return _openai_generate(
            request,
            settings.openai_api_key,
            settings.openai_model,
        ), "openai"
    except Exception:
        logger.exception("OpenAI generation failed; falling back to local draft.")
        return _local_fallback(request), "local"
