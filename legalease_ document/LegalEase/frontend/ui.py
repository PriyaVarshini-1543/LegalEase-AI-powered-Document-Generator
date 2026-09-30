import streamlit as st

from backend.models.schemas import DocumentRequest
from backend.services.document_service import create_document
from backend.utils.text_utils import word_count
from exporters.docx_exporter import export_docx
from exporters.pdf_exporter import export_pdf
from exporters.txt_exporter import export_txt

DOCUMENT_TYPES = [
    "Rental Agreement",
    "Employment Agreement",
    "Non-Disclosure Agreement",
    "Affidavit",
    "Demand Letter",
    "General Legal Letter",
]


def _load_css() -> None:
    st.markdown(
        """
        <style>
        .block-container { max-width: 1100px; padding-top: 2rem; }
        .hero {
            padding: 1.5rem;
            border-radius: 16px;
            background: linear-gradient(135deg, #2457C5, #173B89);
            color: white;
            margin-bottom: 1.5rem;
        }
        .disclaimer {
            padding: 0.8rem 1rem;
            border-left: 4px solid #E2A72E;
            background: #FFF8E6;
            border-radius: 6px;
            margin: 1rem 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def run_app() -> None:
    st.set_page_config(
        page_title="LegalEase",
        page_icon="⚖️",
        layout="wide",
    )
    _load_css()

    st.markdown(
        """
        <div class="hero">
            <h1>⚖️ LegalEase</h1>
            <p>AI-assisted legal document drafting and export.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="disclaimer"><b>Important:</b> LegalEase generates drafts '
        'for review. It is not a lawyer and does not provide legal advice. '
        'Verify the document with a qualified professional before signing, '
        'filing, or relying on it.</div>',
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.header("Document setup")
        document_type = st.selectbox("Document type", DOCUMENT_TYPES)
        client_name = st.text_input("Prepared for / client name")
        jurisdiction = st.text_input("Jurisdiction", value="India")
        tone = st.selectbox("Writing style", ["Formal", "Plain English", "Professional"])

        st.divider()
        st.caption("AI key is optional. Without one, a local template generator is used.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Your facts and requirements")
        facts = st.text_area(
            "Describe the situation and terms",
            height=360,
            placeholder=(
                "Example: Landlord Priya rents a residential apartment to Arjun "
                "for 11 months at ₹25,000 per month. Security deposit is ₹75,000. "
                "Include maintenance responsibilities and a notice period."
            ),
        )

        generate = st.button(
            "Generate document",
            type="primary",
            use_container_width=True,
        )

    with col2:
        st.subheader("Generated draft")

        if generate:
            if not client_name.strip():
                st.error("Please enter the client name.")
                return
            if len(facts.strip()) < 10:
                st.error("Please provide at least a few sentences of facts/terms.")
                return

            request = DocumentRequest(
                document_type=document_type,
                client_name=client_name,
                jurisdiction=jurisdiction or "India",
                facts=facts,
                tone=tone,
            )

            with st.spinner("Preparing your draft..."):
                result = create_document(request)

            st.session_state["result"] = result
            st.success(
                "Draft generated using "
                + ("OpenAI." if result.source == "openai" else "the local fallback generator.")
            )

        result = st.session_state.get("result")

        if result:
            st.caption(f"{word_count(result.content)} words")
            edited = st.text_area(
                "Review and edit before exporting",
                value=result.content,
                height=520,
                key="document_editor",
            )

            txt = export_txt(result.title, edited)
            docx = export_docx(result.title, edited)
            pdf = export_pdf(result.title, edited)

            d1, d2, d3 = st.columns(3)
            with d1:
                st.download_button(
                    "Download TXT",
                    data=txt,
                    file_name="legalease_document.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            with d2:
                st.download_button(
                    "Download DOCX",
                    data=docx,
                    file_name="legalease_document.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                )
            with d3:
                st.download_button(
                    "Download PDF",
                    data=pdf,
                    file_name="legalease_document.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
        else:
            st.info("Your generated document will appear here.")
