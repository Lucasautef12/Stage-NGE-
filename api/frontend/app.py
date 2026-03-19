import streamlit as st
import requests
from dotenv import load_dotenv
from pathlib import Path
import sys
import os 

BASE_dir = Path(__file__).resolve().parent.parent
print(f"BASE_dir: {BASE_dir}")
if str(BASE_dir) not in sys.path:
    sys.path.append(str(BASE_dir))

load_dotenv(BASE_dir / ".env")
API_URL = os.getenv("URL_API")  # Récupération de l'URL de l'API depuis les variables d'environnement

def run():
    st.title("Chatbot NGE - Analyseur de Dossiers DCE")
    st.write("Bienvenue sur l'interface de NGE visant à analyser les dossiers DCE ! " \
    "Cette application utilise des modèles d'IA pour extraire des informations à partir d'un dossier DCE " \
    "et répondre à vos questions concernant le contenu du dossier DCE. Vous pouvez poser des questions sur les documents présents dans le dossier DCE, et l'IA vous fournira des réponses basées sur les informations extraites des documents.")

    st.write("Pour commencer, veuillez télécharger un dossier DCE :")

    # Téléchargement d'un dossier DCE
    uploaded_files = st.file_uploader("Choisissez un dossier DCE", accept_multiple_files="directory")

    #Convertir le dossier DCE en un fichier zip pour pouvoir l'envoyer à l'API

    ### A faire : convertir le dossier DCE en un fichier zip pour pouvoir l'envoyer à l'API, et ensuite supprimer le fichier zip après l'envoi pour ne pas encombrer le disque dur

    if uploaded_files:
        files = [
            ("files", (uploaded_file.name, uploaded_file, uploaded_file.type))
            for uploaded_file in uploaded_files
        ]
        response  = requests.post(f"{API_URL}/uploadfolder", files=files)

        if response.status_code == 200:
            st.success("Dossier DCE envoyé avec succès !")
        else:
            st.error(f"Erreur lors de l'envoi du dossier DCE : {response.text}")
    

if __name__ == "__main__":
    run()