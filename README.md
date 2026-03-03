# 📄 PROJET ATS – Analyse Automatisée de CV avec IA

## 🎯 Objectif du projet

Ce projet vise à **automatiser l’analyse de CV** et le **matching avec des offres d’emploi** à l’aide de l’Intelligence Artificielle.  
Il transforme des CV non structurés (PDF, images scannées) en **données exploitables** afin d’aider les recruteurs à :

- Gagner du temps dans le tri des candidatures
- Évaluer objectivement l’adéquation candidat / poste
- Visualiser rapidement les forces et faiblesses d’un profil

Le projet combine **OCR**, **NLP** et **LLM (OpenAI)** dans une application **Streamlit interactive**.

---

## 🧠 Pipeline technique 

Le système est structuré en **6 étapes clés** :

### 1️⃣ Extraction (OCR)
- PDF texte : **PyMuPDF**
- PDF scanné / images : **Tesseract OCR**
- Sortie : texte brut du CV

### 2️⃣ Nettoyage du texte
- Suppression des espaces inutiles
- Normalisation légère du texte
- Préparation pour l’analyse NLP

### 3️⃣ Analyse intelligente du CV (OpenAI)
À partir du texte brut, un **modèle OpenAI peu coûteux** extrait un JSON structuré contenant :
- Identité du candidat
- Formations (toutes, sans résumé)
- Certifications
- Expériences professionnelles
- Hard skills
- Soft skills
- Langues

### 4️⃣ Matching CV ↔ Offre d’emploi (OpenAI)
Un second prompt calcule :
- Score de correspondance (%)
- Compétences manquantes
- Points forts
- Points faibles
- Avis global ATS

### 5️⃣ Structuration des données
- Résultats retournés en **JSON strict**
- Exploitable pour analyse, stockage ou export

### 6️⃣ Interface Streamlit
- Upload du CV
- Saisie de l’offre d’emploi
- Visualisation :
  - Barre de score ATS
  - Analyse synthétique du profil
  - Feedback recruteur

---

## 🗂️ Architecture du projet

```text
PROJET ATS/
├── extraction.py      # Extraction de texte (PDF/Docx)
├── analyse_cv.py      # Analyse sémantique et extraction d'entités via IA
├── matching.py         # Calcul du score de compatibilité Poste vs CV
├── streamlit_app.py   # Interface utilisateur (Dashboard)
├── requirements.txt   # Dépendances Python
├── README.md          # Documentation du projet
└── .streamlit/
    └── secrets.toml   # Clé API OpenAI (Sécurité)


