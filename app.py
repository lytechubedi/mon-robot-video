import streamlit as st
import subprocess
import os

# Titre affiché sur ton site web
st.title("🎬 Mon Robot Vidéo - Mode Original")
st.write("Glisse ta vidéo ici pour casser sa structure et la rendre unique.")

# Création du bouton d'importation
uploaded_file = st.file_uploader("Importe ta vidéo MP4", type=["mp4"])

if uploaded_file is not None:
    # Fichiers de travail sur le serveur
    fichier_entree = "video_brute.mp4"
    fichier_sortie = "video_unique.mp4"
    
    # Écriture de la vidéo reçue sur le serveur cloud
    with open(fichier_entree, "wb") as f:
        f.write(uploaded_file.read())
        
    st.info("⏳ Le robot travaille... Modification des pixels, zoom de 5% et ajustement des filtres en cours...")
    
    # Commande de traitement combinée (sans bug)
    commande = [
        "ffmpeg", "-y", "-i", fichier_entree,
        "-vf", "scale=1.05*iw:-2,crop=iw/1.05:ih/1.05,format=yuv420p,eq=contrast=1.02:brightness=0.01,hue=s=1.08",
        "-c:v", "libx264", 
        preset", "medium", 
        "-c:a", "aac", 
        fichier_sortie
    ]
    
    # Lancement du traitement vidéo
    resultat = subprocess.run(commande, capture_output=True, text=True)
    
    # Si tout s'est bien passé
    if resultat.returncode == 0 and os.path.exists(fichier_sortie):
        st.success("✅ Traitement réussi ! Ta vidéo est prête.")
        
        # Création du bouton de téléchargement pour ton téléphone
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
        
    # Nettoyage automatique du serveur après le travail
    if os.path.exists(fichier_entree):
        os.remove(fichier_entree)

