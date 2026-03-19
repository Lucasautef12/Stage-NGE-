import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File
import os
from dotenv import load_dotenv
from typing import List


#On ajoute le dossier "api" au path pour pouvoir importer les modules du dossier "services" et "rooters" sans problème d'importation
BASE_dir = Path(__file__).resolve().parent.parent
print(f"BASE_dir: {BASE_dir}")
if str(BASE_dir) not in sys.path:
    sys.path.append(str(BASE_dir))

load_dotenv(BASE_dir / ".env")

output_folder = os.getenv("OUTPUT_DIR") #Récupération de la variable d'environnement 
if not os.path.exists(BASE_dir / output_folder):
    os.makedirs(BASE_dir / output_folder)  # Créer le dossier de sortie s'il n'existe pas

#Importation des modules nécessaires pour chaque agent
from backend.rooters import classifier, rag, general
from backend.services import classifier_services, rag_services
from backend.tools import handle_file, process_zip_recursively

#app FastAPI pour définir l'API, avec un endpoint pour chaque agent
app = FastAPI(title="API d'IA multi-agents pour NGE", description="Cette API permet de classifier des documents en fonction de leur contenu et de leur nom de fichier, en utilisant un modèle de classification zéro-shot de Hugging Face.", version="1.0.0")

# On inclut le routeur de classification pour gérer les endpoints liés à la classification de documents
app.include_router(classifier.router, prefix='/classifier', tags=['classifier'])
app.include_router(rag.router, prefix='/rag', tags=['RAG'])
app.include_router(general.router, prefix='/general', tags=['general'])

#Route principale de l'API pour vérifier que l'API est bien en ligne et accessible
@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API de NGE servant à interroger un système multi-agents permettant d'analyser automatiquement un DCE."}

@app.post("/uploadfolder")
async def upload_folder(files: List[UploadFile] = File(...)):
    """Endpoint pour uploader un dossier compressé (zip ou 7z) contenant des documents à classifier."""
    
    try:
        for file in files:
            file_bytes = await file.read()
            name_folder = file.filename.split('.')[0]  # On utilise le nom du fichier sans l'extension comme nom de dossier
            os.makedirs(BASE_dir / output_folder / name_folder, exist_ok=True)  # Créer le dossier de sortie pour ce fichier

            extension = file.filename.lower().split('.')[-1]
            if extension in {'zip', '7z'}:
                process_zip_recursively(file_bytes, BASE_dir / output_folder / name_folder)  # On traite le fichier zip ou 7z de manière récursive et on stocke les fichiers extraits dans le dossier backend/outputs/nom_du_dossier

            elif extension in {'pdf', 'docx', 'xlsx', 'pptx', 'txt', 'csv', 'json', 'xml','jpg', 'jpeg', 'png'} or os.path.splitext(file.filename)[1] == '':
                handle_file(file.filename, file_bytes, BASE_dir / output_folder / name_folder)  # Si le fichier est un document ou une image, on le stocke directement dans le dossier backend/outputs/nom_du_dossier

        return {"message": "Dossiers traités et uploadés avec succès."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement du dossier : {str(e)}")