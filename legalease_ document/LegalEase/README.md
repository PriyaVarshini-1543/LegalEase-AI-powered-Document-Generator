# LegalEase

LegalEase is a simple AI-assisted legal-document drafting application.

## Features
- Draft common legal documents from a plain-English request.
- Optional OpenAI Responses API integration.
- Works without an API key using a deterministic local template fallback.
- Export generated documents as TXT, DOCX, or PDF.
- FastAPI backend with health and document-generation endpoints.
- Streamlit frontend.
- Pytest test suite.

> LegalEase is an information and drafting aid, not a lawyer or a substitute for professional legal advice. Generated text must be reviewed for jurisdiction, facts, dates, names, and legal requirements before use.

## 1. Requirements

- Python 3.11 or newer
- Windows, macOS, or Linux
- Internet connection only if you want OpenAI generation

## 2. Windows setup

Open PowerShell in the `LegalEase` folder:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\setup_windows.ps1
```

Then activate the environment if the script did not keep it active:

```powershell
.\.venv\Scripts\Activate.ps1
```

Copy `.env.example` to `.env` and optionally add your OpenAI API key.

## 3. Run the Streamlit application

```powershell
streamlit run app.py
```

Open the URL shown by Streamlit, normally:
`http://localhost:8501`

The frontend can generate documents directly through the service layer, so you do not have to start FastAPI for the normal UI.

## 4. Run the API separately

```powershell
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

API:
`http://127.0.0.1:8000`

Swagger:
`http://127.0.0.1:8000/docs`

## 5. Run tests

```powershell
pytest -q
```

## 6. Docker

```bash
docker compose up --build
```

Streamlit:
`http://localhost:8501`

FastAPI:
`http://localhost:8000/docs`

## Environment variables

See `.env.example`.

If `OPENAI_API_KEY` is empty, LegalEase automatically uses the local fallback generator. This lets you test the entire UI and export workflow without API billing or credentials.

## Suggested demo

1. Choose `Rental Agreement`.
2. Enter the parties, property, rent, deposit, and term.
3. Click **Generate document**.
4. Review the generated draft.
5. Download TXT, DOCX, and PDF versions.
