#Importation des bibliothèques nécessaires
import streamlit as st
import json
from openai import OpenAI

# Recuperation de la clé OpenAI depuis secrets.toml
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Prompt pour le matching CV avec l'Offre d'emploi
PROMPT_MATCHING = """
Tu es un ATS professionnel.

À partir :
1) du PROFIL CANDIDAT (JSON structuré)
2) de l'OFFRE D'EMPLOI

Calcule un score de correspondance précis.

Retourne UNIQUEMENT un JSON valide :

{{
  "score_match": "85%",
  "hard_skills_manquantes": [],
  "soft_skills_manquantes": [],
  "points_forts": [],
  "points_faibles": [],
  "avis_global": ""
}}

PROFIL CANDIDAT :
----------------
{cv_json}

OFFRE D'EMPLOI :
----------------
{job_description}
"""

# Fonction pour matcher le CV avec l'Offre d'emploi
def matcher_cv_offre(cv_json, job_description):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # le modèle openai utilisé
        messages=[
            {"role": "system", "content": "Tu es un ATS strict."}, # Instructions pour le modèle
            {
                "role": "user", 
                "content": PROMPT_MATCHING.format( 
                    cv_json=json.dumps(cv_json, ensure_ascii=False),
                    job_description=job_description
                )
            }
        ],
        temperature=0, # Contrôle la créativité de la réponse
        max_tokens=600 # Limite le nombre de tokens dans la réponse
    )

    return response.choices[0].message.content
