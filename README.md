# AI Document Assistant

**An AI-powered PDF document analysis application built with Python, FastAPI, OCR, and the OpenAI API.**

[**Live Demo**](https://ai-document-assistant-79cp.onrender.com/app) · [API Documentation](https://ai-document-assistant-79cp.onrender.com/docs) · [Health Check](https://ai-document-assistant-79cp.onrender.com/health) · [GitHub Repository](https://github.com/mariemL123/AI-Document-Assistant)

## Overview

AI Document Assistant is a web application that extracts text from PDF documents, detects when OCR is needed, and uses artificial intelligence to generate structured document analyses.

The project demonstrates practical backend development, document processing, API integration, database management, and cloud deployment using Python.

## Key Features

- **PDF text extraction:** Extracts text from digital PDF documents using PyMuPDF.
- **OCR fallback:** Uses Tesseract OCR to process scanned pages when text extraction is insufficient.
- **AI-powered analysis:** Integrates the OpenAI API to summarize documents and identify relevant information.
- **REST API:** Provides backend functionality through FastAPI.
- **Interactive API documentation:** Enables endpoint exploration and testing with Swagger UI.
- **Analysis history:** Stores document analysis metadata in SQLite.
- **Web interface:** Provides a browser-based interface for uploading documents and viewing analysis results.
- **Data visualization:** Displays document statistics and charts using Chart.js.
- **Cloud deployment:** Runs as a containerized application on Render.

## Live Application

Try the deployed application:

**[Open AI Document Assistant](https://ai-document-assistant-79cp.onrender.com/app)**

Additional resources:

- [Swagger UI](https://ai-document-assistant-79cp.onrender.com/docs)
- [API Health Check](https://ai-document-assistant-79cp.onrender.com/health)

*Note: The free hosting service may take some time to wake up after a period of inactivity. SQLite data on the free deployment may not persist across restarts or redeployments.*

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| FastAPI | REST API and backend |
| PyMuPDF | PDF text extraction |
| Tesseract OCR | Scanned document recognition |
| pytesseract and Pillow | OCR integration and image processing |
| OpenAI API | AI-powered document analysis |
| SQLite | Analysis history |
| HTML, CSS, JavaScript | Frontend |
| Chart.js | Data visualization |
| Docker | Containerization |
| Render | Cloud deployment |
| Git and GitHub | Version control and source code hosting |

## Architecture

The application follows a straightforward document-processing workflow:

1. The user uploads a PDF through the web interface.
2. The backend extracts text from the document.
3. OCR is used when scanned pages require text recognition.
4. The extracted content is passed to the OpenAI API for analysis.
5. The application returns structured analysis results.
6. Document statistics and analysis history are displayed in the interface.

## Project Structure

```text
AI-Document-Assistant/
├── main.py
├── index.html
├── requirements.txt
├── Dockerfile
├── .env.example
├── .gitignore
└── README.md
```

Additional local test scripts and configuration files may exist in the development environment.

## Getting Started

### Prerequisites

- Python 3.12 or a compatible Python version
- Tesseract OCR
- An OpenAI API key
- Git

### 1. Clone the repository

```bash
git clone https://github.com/mariemL123/AI-Document-Assistant.git
cd AI-Document-Assistant
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a reference.

Configure the variables required by the application:

```dotenv
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=your_supported_model_name
```

Replace the example values with your own valid credentials and a model available to your OpenAI API account.

**Security:** Never commit your `.env` file, API keys, or other secrets to GitHub.

### 5. Install Tesseract OCR

Install Tesseract OCR for your operating system. On Windows, ensure that the application can locate the Tesseract executable. On Linux, install Tesseract through the system package manager.

### 6. Start the application

```bash
python -m uvicorn main:app --reload
```

Open these addresses in your browser:

- Application: http://127.0.0.1:8000/app
- API root: http://127.0.0.1:8000/
- Health check: http://127.0.0.1:8000/health
- Swagger documentation: http://127.0.0.1:8000/docs

## Deployment

The project includes a `Dockerfile` and is deployed on Render.

The container installs the Python dependencies and Tesseract OCR, then starts the FastAPI application using the port provided by the hosting platform.

For production use, persistent storage should be configured for the SQLite database, or the database should be migrated to a managed database service.

## Example Use Cases

- Extracting totals, dates, and other information from invoices.
- Summarizing travel confirmations and booking documents.
- Analyzing educational documents and course materials.
- Processing scanned PDFs using OCR.
- Exploring AI-assisted document processing and automation workflows.

## Security and Limitations

- API credentials are configured through environment variables.
- Local secrets, virtual environments, and database files are excluded from version control.
- Uploaded documents may contain confidential information and should be handled carefully.
- AI-generated results may contain errors and should be verified when accuracy is important.
- The free deployment uses SQLite without guaranteed persistent storage.

## Roadmap

- [x] Build the FastAPI backend.
- [x] Implement PDF text extraction and OCR fallback.
- [x] Integrate AI-powered document analysis.
- [x] Build a web interface with visual statistics.
- [x] Implement SQLite-based analysis history.
- [x] Containerize the application with Docker.
- [x] Deploy a live demo on Render.
- [ ] Add automated tests and continuous integration.
- [ ] Improve validation, error handling, and API security.
- [ ] Introduce persistent production-grade database storage.
- [ ] Expand document extraction and analysis capabilities.

## Author

**Mariem L.**

Python · Backend Development · Artificial Intelligence · Document Processing

[GitHub Profile](https://github.com/mariemL123)

---

*This project demonstrates practical applications of Python, REST API development, OCR, AI integration, Docker, and cloud deployment.*

## Screenshots

### Application Interface

![AI Document Assistant - Application Interface](screenshots/Capture%20d%27%C3%A9cran%202026-10-29%20120116.png)

### Document Analysis

![AI Document Assistant - Document Analysis Results](screenshots/Capture%20d%27%C3%A9cran%202026-10-29%20120222.png)
