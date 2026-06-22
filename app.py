import streamlit as st
import subprocess
import os
from google import genai

# Installation automatique de FFmpeg
@st.cache_resource
def installer_ffmpeg_magique():
    import urllib.request
    import tarfile
    import stat
    
    ffmpeg_exe = "./ffmpeg"
    if not os.path.exists(ffmpeg_exe):
        try:
            url = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
            archive = "ffmpeg.tar.xz"
            
            with st.spinner("🔧 Configuration initiale du robot..."):
                urllib.request.urlretrieve(url, archive)
                with tarfile.open(archive, "r:xz") as tar:
                    for member in tar.getmembers():
                        if member.name.endswith("/ffmpeg") and not member.name.endswith("/ffmpeg-10bit"):
                            f_extrait = tar.extractfile(member)
                            with open(ffmpeg_exe, "wb") as f_out:
                                f_out.write(f_extrait.read())
            
            st.chmod(ffmpeg_exe, st.stat(ffmpeg_exe).st_mode | stat.S_IEXEC)
            if os.path.exists(archive):
                os.remove(archive)
        except Exception as e:
            st.error(f"Erreur d'installation automatique : {e}")
    return ffmpeg_exe

chemin_ffmpeg = installer_ffmpeg_magique()

# --- CONFIGURATION DE L'ECRAN ---
st.set_page_config(page_title="Robot Vidéo IA", page_icon="🚀", layout="centered")

st.title("🚀 Mon Robot Vidéo IA Automatique")
st.write("Crée une vidéo unique et son pack SEO complet en un seul clic.")

st.write("---")

# --- FORMULAIRE UNIQUE ---
st.header("1️⃣ Remplir les informations")
cle_api_saisie = st.text_input("🔑 Ta clé API Gemini", type="password", help="Colle ta clé secrète récupérée sur Google AI Studio")
theme_video = st.text_input("📝 Quel est le sujet de la vidéo ?", placeholder="Ex: 3 secrets pour devenir riche")
uploaded_file = st.file_uploader("📥 Importe ta vidéo MP4", type=["mp4"])

st.write("---")

# --- LE BOUTON MAGIQUE ---
if st.button("🔥 LANCER LA MAGIE AUTOMATIQUE"):
    if not cle_api_saisie:
        st.warning("⚠️ S'il te plaît, ajoute ta clé API Gemini.")
    elif not theme_video:
        st.warning("⚠️ Donne un thème à ta vidéo pour l'IA.")
    elif uploaded_file is None:
        st.warning("⚠️ Tu as oublié d'importer une vidéo MP4.")
    else:
        # Création de deux colonnes pour afficher les résultats proprement côte à côte
        col_video, col_texte = st.columns(2)
        
        # --- PARTIE 1 : TRAITEMENT DE LA VIDÉO ---
        with col_video:
            st.subheader("🎬 Ta Vidéo Unique")
            fichier_entree = "video_brute.mp4"
            fichier_sortie = "video_unique.mp4"
            
            with open(fichier_entree, "wb") as f:
                f.write(uploaded_file.read())
                
            with st.spinner("⚡ Modification des pixels..."):
                commande = [
                    chemin_ffmpeg, "-y", "-i", fichier_entree,
                    "-vf", "scale=1.05*iw:-2,crop=iw/1.05:ih/1.05,format=yuv420p",
                    "-c:v", "libx264", 
                    "-preset", "ultrafast",
                    "-tune", "fastdecode",
                    "-c:a", "copy",
                    fichier_sortie
                ]
                resultat = subprocess.run(commande, capture_output=True, text=True)
            
            if resultat.returncode == 0 and os.path.exists(fichier_sortie):
                st.success("✅ Vidéo modifiée !")
                with open(fichier_sortie, "rb") as f:
                    st.download_button(
                        label="📥 Télécharger le MP4",
                        data=f,
                        file_name="video_unique_anti_copyright.mp4",
                        mime="video/mp4"
                    )
            else:
                st.error("Erreur vidéo.")
            
            if os.path.exists(fichier_entree):
                os.remove(fichier_entree)

        # --- PARTIE 2 : TEXTE AUTOMATIQUE ---
        with col_texte:
            st.subheader("🧠 Ton Pack SEO")
            try:
                with st.spinner("✍️ Rédaction des textes..."):
                    client = genai.Client(api_key=cle_api_saisie)
                    
                    consigne = (
                        f"Tu es un expert mondial en algorithme YouTube Shorts et TikTok.\n"
                        f"Génère pour une vidéo sur le thème '{theme_video}' :\n"
                        f"- Un titre ultra-viral (captivant, court, emojis).\n"
                        f"- Une description optimisée avec mots-clés.\n"
                        f"- Les 5 meilleurs hashtags.\n"
                        f"Reste très concis et impactant."
                    )

                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=consigne
                    )
                    
                st.success("✅ Script généré !")
                st.text_area("Texte à copier :", value=response.text, height=200)
                
            except Exception as e:
                st.error(f"Erreur IA : {e}")
