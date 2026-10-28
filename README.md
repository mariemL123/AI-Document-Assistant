# AI Document Assistant

**An AI-powered PDF document analysis application built with Python and FastAPI.**

AI Document Assistant extracts text from PDF documents, applies OCR when needed, and uses AI to generate structured document analyses.

## Features

- **PDF text extraction** with PyMuPDF.
- **OCR fallback** for scanned PDF pages using Tesseract, pytesseract and Pillow.
- **AI-powered analysis** using the OpenAI API.
- **REST API** built with FastAPI.
- **Interactive API documentation** with Swagger UI.
- **Analysis history** stored locally in SQLite.
- **Web interface** with visual statistics and charts.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST API |
| PyMuPDF | PDF text extraction |
| Tesseract OCR | Text recognition |
| OpenAI API | Intelligent document analysis |
| SQLite | Local analysis history |
| HTML, CSS, JavaScript | Frontend |
| Chart.js | Data visualization |

## Project Structure

```text
AI-Document-Assistant/
├── main.py
├── index.html
├── inspect_pdf.py
├── test_openai.py
├── test_pdf.py
├── test_pymupdf.py
├── .env.example
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/mariemL123/AI-Document-Assistant.git
cd AI-Document-Assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the Python packages required by the application. If a `requirements.txt` file is available, run:

```bash
pip install -r requirements.txt
```

Otherwise, install the packages used by the project and create a `requirements.txt` file.

### 4. Configure environment variables

Create a local `.env` file and configure the OpenAI API key using the variable name expected by `main.py`.

**Never commit your `.env` file or API keys to GitHub.**

Install Tesseract OCR separately if OCR functionality is required, and configure its executable path for your environment.

### 5. Run the API

```bash
python -m uvicorn main:app --reload
```

Open the following URLs in your browser:

- API: http://127.0.0.1:8000
- Health check: http://127.0.0.1:8000/health
- Swagger documentation: http://127.0.0.1:8000/docs

## Use Cases

- Extracting information from invoices.
- Summarizing travel confirmations and booking documents.
- Analyzing educational documents and course materials.
- Processing scanned PDFs with OCR.
- Exploring AI-assisted document processing workflows.

## Security

- API credentials must be stored in environment variables.
- Local databases and virtual environments should not be committed.
- Uploaded documents may contain sensitive information; handle them securely.

## Roadmap

- [ ] Deploy the FastAPI backend.
- [ ] Publish a live frontend connected to the API.
- [ ] Add screenshots and a live demo.
- [ ] Improve document validation and error handling.
- [ ] Add automated tests and CI.
- [ ] Improve deployment and production security.

## Author

**Mariem L.**

Python · Backend Development · Artificial Intelligence

GitHub: [mariemL123](https://github.com/mariemL123)

---

*This project explores practical applications of Python, OCR, REST APIs and AI-powered document analysis.*
