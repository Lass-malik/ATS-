# Importe les bibliothèques nécessaires
import streamlit as st
from openai import OpenAI

# Recuperation de la clé OpenAI depuis secrets.toml
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Prompt pour l'analyse du CV
PROMPT_ANALYSE_CV = """
Tu es un expert ATS (Applicant Tracking System).

À partir du texte brut du CV ci-dessous, extrais les informations et retourne
UNIQUEMENT un JSON valide, sans aucun texte supplémentaire.

Règles générales :
- Respecte strictement la structure demandée
- Si une information est absente, retourne une chaîne vide ou une liste vide
- Ne mélange jamais les catégories

IMPORTANT :
- Extraire TOUTES les formations (Bac, Licence, Master, etc.)
- Une ligne = un diplôme
- Ordre : du plus récent au plus ancien

Structure attendue :

{{
  "nom": "",
  "formations": [
    {{
      "diplome": "",
      "etablissement": "",
      "date": ""
    }}
  ],
  "certifications": [
    {{
      "intitule": "",
      "organisme": "",
      "annee": ""
    }}
  ],
  "experiences": [
    {{
      "poste": "",
      "entreprise": "",
      "date_debut": "",
      "date_fin": ""
    }}
  ],
  "hard_skills": [],
  "soft_skills": [],
  "langues": [
    {{
      "langue": "",
      "niveau": ""
    }}
  ]
}}

TEXTE DU CV :
----------------
{cv_text}
"""

# Fonction pour analyser le CV avec OpenAI
def analyser_cv_openai(cv_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # le modèle openai utilisé
        messages=[
            {"role": "system", "content": "Tu es un ATS strict."},# Instructions pour le modèle
            {"role": "user", "content": PROMPT_ANALYSE_CV.format(cv_text=cv_text)}# Prompt avec le texte du CV
        ],
        temperature=0,# Contrôle la créativité de la réponse
        max_tokens=800 # Limite le nombre de tokens dans la réponse
    )

    return response.choices[0].message.content
