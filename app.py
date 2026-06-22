import streamlit as st
import subprocess
import os

# TRUC MAGIQUE 1 : Installation automatique de FFmpeg
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

# Chargement de FFmpeg
chemin_ffmpeg = installer_ffmpeg_magique()

# Interface du site web
st.title("🎬 Mon Robot Vidéo - Mode Original")
st.write("Glisse ta vidéo ici (formats longs acceptés) pour la rendre unique.")

# Zone d'importation de la vidéo
uploaded_file = st.file_uploader("Importe ta vidéo MP4", type=["mp4"])

if uploaded_file is not None:
    fichier_entree = "video_brute.mp4"
    fichier_sortie = "video_unique.mp4"
    
    with open(fichier_entree, "wb") as f:
        f.write(uploaded_file.read())
        
    st.info("⏳ Traitement ultra-rapide en cours pour vidéo longue...")
    
    # Commande FFmpeg configurée en mode "ultrafast" pour éviter les coupures sur les vidéos de 15 min
    commande = [
        chemin_ffmpeg, "-y", "-i", fichier_entree,
        "-vf", "scale=1.05*iw:-2,crop=iw/1.05:ih/1.05,format=yuv420p,eq=contrast=1.02:brightness=0.01,hue=s=1.08",
        "-c:v", "libx264", 
        "-preset", "ultrafast",  # Mode TGV pour gros fichiers
        "-c:a", "aac", 
        fichier_sortie
    ]
    
    resultat = subprocess.run(commande, capture_output=True, text=True)
    
    if resultat.returncode == 0 and os.path.exists(fichier_sortie):
        st.success("✅ Traitement réussi ! Ta vidéo est prête.")
        
        with open(fichier_sortie, "rb") as f:
            st.download_button(
                label="📥 Télécharger la vidéo unique",
                data=f,
                file_name="video_pour_capcut.mp4",
                mime="video/mp4"
            )
            
    else:
        st.error("Mince, une erreur est survenue pendant le traitement.")
        st.code(resultat.stderr)
        
    if os.path.exists(fichier_entree):
        os.remove(fichier_entree)
