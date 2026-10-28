import pymupdf

pdf_path = input("Chemin complet du PDF : ").strip().strip('"')

try:
    with pymupdf.open(pdf_path) as document:
        print("PDF chiffré :", document.is_encrypted)
        print("Nombre de pages :", len(document))

        for index, page in enumerate(document, start=1):
            print(f"\n--- Page {index} ---")
            print("Dimensions :", page.rect)
            print("Blocs de texte :", len(page.get_text("blocks")))
            print("Nombre d'images :", len(page.get_images(full=True)))
            print("Polices détectées :", len(page.get_fonts(full=True)))

            print("Structure du texte :")
            print(repr(page.get_text("text", sort=True)[:300]))

except Exception as exc:
    print(f"Erreur : {type(exc).__name__}: {exc}")