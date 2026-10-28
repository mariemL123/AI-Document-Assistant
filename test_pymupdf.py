import pymupdf

pdf_path = input("Chemin complet du PDF : ").strip().strip('"')

try:
    with pymupdf.open(pdf_path) as document:
        print(f"\nNombre de pages : {len(document)}")

        for index, page in enumerate(document, start=1):
            text = page.get_text("text")

            print(f"\n--- Page {index} ---")
            print(f"Nombre de caractères : {len(text)}")
            print(repr(text[:500]))

except Exception as exc:
    print(f"Erreur : {type(exc).__name__}: {exc}")