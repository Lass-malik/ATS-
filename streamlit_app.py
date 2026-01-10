#Importation des bibliothèques nécessaires
import streamlit as st
import json
import plotly.graph_objects as go
import os
import tempfile

# Importation des modules personnalisés
from extraction import extract_text_from_pdf, nettoyer_texte
from analyse_cv import analyser_cv_openai
from matching import matcher_cv_offre

#Configuration de la page Streamlit
st.set_page_config(
    page_title="ATS Intelligent",
    page_icon="🤖",
    layout="wide"
)

# CSS personnalisé pour le thème sombre generé avec ChatGPT
st.markdown("""
<style>
/* ===== GLOBAL ===== */
.stApp {
    background-color: #0f172a;
    color: #e5e7eb;
}

html, body, [class*="css"] {
    color: #e5e7eb !important;
}

/* ===== TITRES ===== */
h1, h2, h3 {
    color: #f8fafc !important;
    font-weight: 700;
}

/* ===== CARDS ===== */
.card {
    background: #020617;
    padding: 1.5rem;
    border-radius: 16px;
    box-shadow: 0 0 0 1px #1e293b;
    margin-bottom: 1.5rem;
}

/* ===== FILE UPLOADER ===== */
[data-testid="stFileUploader"] {
    background: #020617;
    border: 2px dashed #38bdf8;
    border-radius: 14px;
    padding: 1.2rem;
}

/* ===== TEXT AREA ===== */
textarea {
    background-color: #020617 !important;
    color: #e5e7eb !important;
    border-radius: 12px !important;
}

/* ===== BUTTON ===== */
.stButton > button {
    background: linear-gradient(90deg, #2563eb, #06b6d4);
    color: white;
    border-radius: 14px;
    padding: 0.7rem 2rem;
    font-weight: 700;
    border: none;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.05);
}

/* ===== ALERTS ===== */
.stAlert {
    border-radius: 12px;
}

/* ===== PROGRESS BAR ===== */
.stProgress > div > div {
    background: linear-gradient(90deg, #22c55e, #16a34a);
}
</style>
""", unsafe_allow_html=True)

#EN-TÊTE DE L'APPLICATION
st.title("🤖 ATS Intelligent – Analyse & Matching de CV")
st.markdown("Analyse automatique de CV avec **OCR + IA + Visualisation ATS**")

#TELECHARGEMENT DU CV
st.markdown('<div class="card">', unsafe_allow_html=True)
uploaded_cv = st.file_uploader(
    "📄 Télécharger votre CV (PDF ou image)",
    type=["pdf", "png", "jpg", "jpeg"]
)
st.markdown('</div>', unsafe_allow_html=True)

#AJOUT DE LA DESCRIPTION DE L'OFFRE D'EMPLOI
st.markdown('<div class="card">', unsafe_allow_html=True)
job_description = st.text_area(
    "🧾 Description du poste",
    placeholder="Collez ici l'offre d'emploi...",
    height=180
)
st.markdown('</div>', unsafe_allow_html=True)

run_button = st.button("🚀 Lancer l’analyse")

# TRAITEMENT DU CV ET DE L'OFFRE D'EMPLOI
if run_button:
    if not uploaded_cv or not job_description: # Vérification des entrées
        st.warning("⚠️ Veuillez fournir un CV et une offre d’emploi.")
        st.stop()

    suffix = os.path.splitext(uploaded_cv.name)[1] # Récupérer l'extension du fichier
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp: # Créer un fichier temporaire avec la bonne extension
        tmp.write(uploaded_cv.getbuffer()) # Écrire le contenu du fichier téléchargé dans le fichier temporaire
        temp_path = tmp.name # Obtenir le chemin du fichier temporaire

    try:
        with st.spinner("📄 Extraction du texte du CV..."): # Extraction du texte du CV
            texte_brut = extract_text_from_pdf(temp_path)
            texte_nettoye = nettoyer_texte(texte_brut)

        with st.spinner("🤖 Analyse IA du CV..."): # Analyse du cv avec IA
            cv_json = json.loads(analyser_cv_openai(texte_nettoye))

        with st.spinner("📊 Calcul du score ATS..."): # Calcul du score de correspondance
            matching = json.loads(matcher_cv_offre(cv_json, job_description))

    except Exception as e:
        st.error(str(e))
        st.stop()

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    # SCORE CIRCULAIRE
    score = int(matching["score_match"].replace("%", ""))

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎯 Score de compatibilité ATS")

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": "%", "font": {"size": 40, "color": "white"}},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#22c55e"},
            "bgcolor": "#020617",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 50], "color": "#7f1d1d"},
                {"range": [50, 75], "color": "#ca8a04"},
                {"range": [75, 100], "color": "#15803d"},
            ],
        }
    ))

    gauge.update_layout(
        paper_bgcolor="#020617",
        font={"color": "white"},
        height=300
    )

    st.plotly_chart(gauge, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


    # RADAR SKILLS
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🛠️ Compétences techniques")

    hard_skills = cv_json.get("hard_skills", [])
    missing = matching.get("hard_skills_manquantes", [])

    labels = list(set(hard_skills + missing))
    values = [1 if s in hard_skills else 0 for s in labels]

    radar = go.Figure(go.Scatterpolar(
        r=values,
        theta=labels,
        fill="toself",
        fillcolor="rgba(56,189,248,0.4)",
        line=dict(color="#38bdf8")
    ))

    radar.update_layout(
        polar=dict(radialaxis=dict(visible=False)),
        paper_bgcolor="#020617",
        font=dict(color="white"),
        showlegend=False
    )

    st.plotly_chart(radar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

  
    # POINTS FORTS / FAIBLES
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Points forts")
        for p in matching.get("points_forts", []):
            st.success(p)

    with col2:
        st.subheader("⚠️ Axes d’amélioration")
        for p in matching.get("points_faibles", []):
            st.warning(p)

    st.markdown('</div>', unsafe_allow_html=True)

    # avis global ATS
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🧠 Avis global ATS")
    st.info(matching.get("avis_global", ""))
    st.markdown('</div>', unsafe_allow_html=True)
