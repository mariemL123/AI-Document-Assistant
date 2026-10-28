import os
import sqlite3
from datetime import datetime, timezone
from io import BytesIO

import pymupdf
import pytesseract
from PIL import Image, UnidentifiedImageError
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

load_dotenv()

app = FastAPI(
    title="AI Document Assistant",
    description="Extraction OCR et analyse intelligente de documents PDF.",
    version="0.4.0",
)

# Configuration locale de Tesseract sous Windows.
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if os.path.isfile(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    os.path.join(BASE_DIR, "history.db"),
)

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 Mo
MAX_PDF_PAGES = 100
MAX_TEXT_FOR_AI = 20000


def get_db_connection():
    connection = sqlite3.connect(DATABASE_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    with get_db_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                created_at TEXT NOT NULL,
                pages INTEGER NOT NULL,
                characters_extracted INTEGER NOT NULL,
                ocr_pages INTEGER NOT NULL,
                method TEXT NOT NULL,
                ai_analysis TEXT NOT NULL,
                text_preview TEXT NOT NULL
            )
        """)


def save_analysis(result: dict) -> int:
    created_at = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    with get_db_connection() as connection:
        cursor = connection.execute("""
            INSERT INTO analyses (
                filename, created_at, pages, characters_extracted,
                ocr_pages, method, ai_analysis, text_preview
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            result["filename"],
            created_at,
            result["pages"],
            result["characters_extracted"],
            result["ocr_pages"],
            result["method"],
            result["ai_analysis"],
            result["text_preview"],
        ))
        return int(cursor.lastrowid)


def row_to_summary(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "filename": row["filename"],
        "created_at": row["created_at"],
        "pages": row["pages"],
        "characters_extracted": row["characters_extracted"],
        "ocr_pages": row["ocr_pages"],
        "method": row["method"],
    }


init_database()


@app.get("/")
def home():
    return {
        "message": "AI Document Assistant API is running",
        "status": "ok",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


def extract_pdf_text(content: bytes):
    pages_text = []
    ocr_pages = 0

    try:
        with pymupdf.open(stream=content, filetype="pdf") as document:
            if document.is_encrypted:
                raise HTTPException(
                    status_code=400,
                    detail="Password-protected PDFs are not supported.",
                )

            if len(document) == 0:
                raise HTTPException(
                    status_code=400,
                    detail="The PDF contains no pages.",
                )

            if len(document) > MAX_PDF_PAGES:
                raise HTTPException(
                    status_code=400,
                    detail=f"The PDF exceeds the {MAX_PDF_PAGES}-page limit.",
                )

            for page in document:
                text = page.get_text("text").strip()

                if len(text) < 20:
                    pix = page.get_pixmap(
                        matrix=pymupdf.Matrix(2, 2),
                        alpha=False,
                    )
                    try:
                        image = Image.open(BytesIO(pix.tobytes("png")))
                        image.load()
                    except (UnidentifiedImageError, OSError) as exc:
                        raise HTTPException(
                            status_code=400,
                            detail="A PDF page could not be prepared for OCR.",
                        ) from exc

                    text = pytesseract.image_to_string(
                        image,
                        lang="fra+eng",
                    ).strip()
                    ocr_pages += 1

                pages_text.append(text)

    except HTTPException:
        raise
    except (pymupdf.FileDataError, RuntimeError, ValueError) as exc:
        raise HTTPException(
            status_code=400,
            detail="The PDF is invalid, corrupted, or cannot be read.",
        ) from exc

    return "\n\n".join(pages_text).strip(), len(pages_text), ocr_pages


def analyze_with_ai(document_text: str):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=503,
            detail="The OpenAI API key is not configured.",
        )

    try:
        client = OpenAI()
        response = client.responses.create(
            # Le modèle peut être configuré dans .env avec OPENAI_MODEL.
            model=os.getenv("OPENAI_MODEL", "gpt-6-luna"),
            instructions=(
                "Tu es un assistant spécialisé dans l'analyse de documents. "
                "Réponds en français. Utilise uniquement les informations "
                "présentes dans le document. Ne devine pas les informations "
                "manquantes. Si une information manque, indique-le."
            ),
            input=(
                "Analyse le document ci-dessous et fournis :\n"
                "1. Un résumé clair en quelques phrases.\n"
                "2. Le type probable de document.\n"
                "3. Les informations importantes sous forme de liste.\n"
                "4. Les dates, montants et références trouvés.\n"
                "5. Les éventuelles actions à effectuer.\n\n"
                "DOCUMENT :\n"
                f"{document_text[:MAX_TEXT_FOR_AI]}"
            ),
        )
        return response.output_text

    except HTTPException:
        raise
    except Exception as exc:
        print(f"Erreur API : {type(exc).__name__}")
        raise HTTPException(
            status_code=502,
            detail=(
                "L'analyse IA a échoué. Vérifiez le nom du modèle, "
                "la clé API, la facturation et la connexion."
            ),
        ) from exc


@app.post("/documents/analyze")
async def analyze_pdf(file: UploadFile = File(...)):
    filename = file.filename or ""

    if not filename or not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file.",
        )

    # Lire au plus 20 Mo + 1 octet afin de détecter le dépassement
    # sans charger entièrement un fichier arbitrairement volumineux.
    try:
        content = await file.read(MAX_FILE_SIZE + 1)
    finally:
        await file.close()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="The PDF exceeds the 20 MB limit.",
        )

    # L'extension seule ne prouve pas que le fichier est un PDF.
    if not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="The file does not have a valid PDF signature.",
        )

    try:
        extracted_text, page_count, ocr_pages = extract_pdf_text(content)

        if not extracted_text or not extracted_text.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text was found in the PDF.",
            )

        ai_analysis = analyze_with_ai(extracted_text)

        result = {
            "filename": filename,
            "pages": page_count,
            "characters_extracted": len(extracted_text),
            "ocr_pages": ocr_pages,
            "method": "pdf_text_with_ocr_fallback",
            "ai_analysis": ai_analysis,
            "text_preview": extracted_text[:1000],
        }
        result["history_id"] = save_analysis(result)
        return result

    except HTTPException:
        raise
    except sqlite3.Error as exc:
        print(f"Erreur base de données : {type(exc).__name__}")
        raise HTTPException(
            status_code=500,
            detail="The analysis could not be saved to history.",
        ) from exc
    except Exception as exc:
        print(f"Erreur PDF : {type(exc).__name__}")
        raise HTTPException(
            status_code=400,
            detail="Could not process this PDF.",
        ) from exc


@app.get("/history")
def list_analysis_history(limit: int = 50):
    """Liste les analyses récentes."""
    limit = max(1, min(limit, 200))
    with get_db_connection() as connection:
        rows = connection.execute("""
            SELECT id, filename, created_at, pages, characters_extracted,
                   ocr_pages, method
            FROM analyses ORDER BY id DESC LIMIT ?
        """, (limit,)).fetchall()
    return {"items": [row_to_summary(row) for row in rows], "count": len(rows)}


@app.get("/history/{analysis_id}")
def get_analysis_from_history(analysis_id: int):
    """Récupère le résultat complet d'une ancienne analyse."""
    with get_db_connection() as connection:
        row = connection.execute(
            "SELECT * FROM analyses WHERE id = ?", (analysis_id,)
        ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Analyse introuvable dans l'historique.",
        )

    result = dict(row)
    result["history_id"] = result.pop("id")
    return result


@app.delete("/history/{analysis_id}")
def delete_analysis_from_history(analysis_id: int):
    """Supprime une entrée de l'historique."""
    with get_db_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM analyses WHERE id = ?", (analysis_id,)
        )
        deleted = cursor.rowcount

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Analyse introuvable dans l'historique.",
        )

    return {"status": "deleted", "history_id": analysis_id}


@app.get("/app", include_in_schema=False)
def web_interface():
    html_path = os.path.join(BASE_DIR, "index.html")
    if not os.path.isfile(html_path):
        raise HTTPException(
            status_code=404,
            detail="The frontend file index.html was not found.",
        )
    return FileResponse(html_path)
