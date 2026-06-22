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

# --- INTERFACE GRAPHIQUE ---
st.title("🤖 Mon Robot Vidéo & IA Tout-en-Un")
st.write("Traite tes vidéos et génère tes scripts SEO au même endroit, sans lignes de code.")

# Configuration des onglets pour séparer proprement les tâches
onglet_video, onglet_ia = st.tabs(["🎬 Traitement Vidéo Unique", "🧠 Générateur de Textes SEO"])

# --- ONGLET 1 : TRAITEMENT VIDÉO ---
with onglet_video:
    st.header("Rendre une vidéo unique")
    uploaded_file = st.file_uploader("Importe ta vidéo MP4", type=["mp4"])

    if uploaded_file is not None:
        fichier_entree = "video_brute.mp4"
        fichier_sortie = "video_unique.mp4"
        
        with open(fichier_entree, "wb") as f:
            f.write(uploaded_file.read())
            
        st.info("⚡ Modification structurelle ultra-rapide en cours...")
        
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
            st.success("✅ Vidéo prête !")
            with open(fichier_sortie, "rb") as f:
                st.download_button(
                    label="📥 Télécharger la vidéo unique",
                    data=f,
                    file_name="video_unique.mp4",
                    mime="video/mp4"
                )
        else:
            st.error("Erreur pendant le traitement vidéo.")
            
        if os.path.exists(fichier_entree):
            os.remove(fichier_entree)

# --- ONGLET 2 : GÉNÉRATEUR IA ---
with onglet_ia:
    st.header("Optimisation Algorithme & SEO")
    
    # Cases à remplir directement sur ton site
    cle_api_saisie = st.text_input("Clé API Gemini", type="password", help="Colle ta clé secrète récupérée sur Google AI Studio")
    theme_video = st.text_input("Quel est le thème ou sujet de ta vidéo ?", placeholder="Ex: 3 secrets pour doubler sa productivité")
    
    if st.button("🚀 Générer le pack viral"):
        if not cle_api_saisie:
            st.warning("⚠️ S'il te plaît, colle ta clé API Gemini pour activer le robot.")
        elif not theme_video:
            st.warning("⚠️ Donne un thème à ton robot pour qu'il sache quoi écrire.")
        else:
            try:
                with st.spinner("🤖 L'IA analyse les tendances algorithmiques..."):
                    client = genai.Client(api_key=cle_api_saisie)
                    
                    consigne = (
                        f"Tu es un expert mondial en algorithme YouTube Shorts, TikTok et en SEO. "
                        f"Génère-moi pour une vidéo sur le thème '{theme_video}' :\n"
                        f"1. Un titre hélicoptère ultra-viral (captivant, moins de 60 caractères, avec emojis).\n"
                        f"2. Une description optimisée avec des mots-clés forts pour forcer l'algorithme à te référencer.\n"
                        f"3. Les 5 meilleurs hashtags du moment.\n"
                        f"Donne un résultat ultra propre, prêt à être copié-collé."
                    )

                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=consigne
                    )
                    
                    st.success("🎉 Voici ton pack de publication optimisé :")
                    st.text_area("Résultat à copier :", value=response.text, height=350)
                    
            except Exception as e:
                st.error(f"Erreur de connexion avec l'IA : {e}")
