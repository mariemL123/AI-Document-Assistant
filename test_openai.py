
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

try:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-6-luna",
        input="Réponds en une phrase en français : la connexion à l'API fonctionne."
    )
    print("Réponse de l'IA :")
    print(response.output_text)

except Exception as exc:
    print("Le test a échoué.")
    print(f"Type d'erreur : {type(exc).__name__}")
    print("Vérifie la clé API, les crédits et l'accès au modèle.")
