from pypdf import PdfReader

pdf_path = input("Chemin complet du PDF : ").strip().strip('"')

try:
    reader = PdfReader(pdf_path)

    print(f"\nNombre de pages : {len(reader.pages)}")

    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        print(f"\n--- Page {index} ---")
        print(f"Nombre de caractères : {len(text or '')}")
        print(repr((text or "")[:500]))

except Exception as exc:
    print(f"Erreur : {type(exc).__name__}: {exc}")