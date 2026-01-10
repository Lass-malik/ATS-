# Importation des bibliothèques nécessaires
import os
import re
import fitz  # PyMuPDF
import pytesseract
from PIL import Image

# Configuration du chemin de Tesseract 
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Fonction pour extraire le texte d'un PDF ou d'une image
def extract_text_from_pdf(file_path):
    """
    Extrait le texte d'un PDF ou d'une image.
    Gère proprement les fichiers corrompus ou incompatibles.
    """
    # Vérification de l'existence du fichier
    if not os.path.exists(file_path):
        raise ValueError("❌ Fichier introuvable. Veuillez charger un CV valide.")
    # Ouverture du document avec gestion des erreurs
    try:
        doc = fitz.open(file_path)
    except fitz.FileDataError:
        raise ValueError(
            "❌ Fichier incompatible ou corrompu.\n"
            "Veuillez charger un vrai PDF ou une image valide (JPG, PNG)."
        )
    except Exception:
        raise ValueError(
            "❌ Impossible d’ouvrir le fichier.\n"
            "Le format n’est pas reconnu."
        )
    # Recherche de texte dans le PDF ou l’image
    text = ""

    try:
        for page in doc:
            text += page.get_text()
    except Exception:
        raise ValueError(
            "❌ Le fichier est endommagé ou illisible.\n"
            "Essayez avec un autre CV."
        )

    # OCR si PDF scanné
    if len(text.strip()) < 50: # Seuil arbitraire pour détecter un PDF scanné en fonction du texte extrait
        try:
            for page in doc:
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                text += pytesseract.image_to_string(img, lang="fra")
        except Exception:
            raise ValueError(
                "❌ OCR impossible.\n"
                "L’image est floue ou non exploitable."
            )

    if len(text.strip()) < 20: # Seuil arbitraire pour détecter l'absence de texte exploitable
        raise ValueError(
            "❌ Aucun texte exploitable détecté.\n"
            "Le CV semble vide ou illisible."
        )

    return text

# Fonction pour nettoyer le texte extrait
def nettoyer_texte(text):
    """Nettoyage léger pour LLM"""
    text = re.sub(r"\s+", " ", text) # Remplace les espaces multiples par un seul espace
    text = text.replace("\x0c", "") # Supprime les caractères de saut de page
    return text.strip() # Supprime les espaces en début et fin de texte
