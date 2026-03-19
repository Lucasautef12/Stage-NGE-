from fastapi import APIRouter
from backend.schemes.classification import ClassificationRequest, ClassificationResponse
from backend.services.classifier_services import classifier_engine
from fastapi import UploadFile, File, HTTPException
from typing import List
import zipfile
import io

router = APIRouter()

@router.post("/upload", response_model=ClassificationResponse)
async def classify_from_file(file: UploadFile = File(...)):
    """Endpoint pour classifier un document à partir de son contenu et de son nom de fichier
    Args:
        file (UploadFile): Le fichier à classifier
    Returns:
        ClassificationResponse: La réponse de classification
    """

    #On lit le contenu du fichier téléchargé et on le prétraite pour extraire le texte du PDF
    #et ajouter le nom du fichier au début du texte
    content = await file.read()

    #On appelle la méthode de classification du classificateur de documents en lui passant le contenu prétraité
    #du fichier pour obtenir le label de classification du document
    label = classifier_engine.classify(content, file.filename)

    #Formate la réponse de classification en utilisant le schéma de réponse ClassificationResponse
    classification_response = ClassificationResponse(filename=file.filename, label=label)

    return classification_response

@router.post("/upload_zip", response_model=List[ClassificationResponse])
async def upload_zip(zip_file: UploadFile = File(...)):
    """
    Endpoint pour classifier plusieurs documents à partir d'un fichier zip contenant les documents à classifier.
    Args:
        zip_file (UploadFile): Le fichier zip contenant les documents à classifier
        Returns:
        List[ClassificationResponse]: La liste des réponses de classification pour chaque document classifié"""
    
    #On vérifie que le fichier téléchargé est bien un fichier zip
    if not zip_file.filename.endswith(".zip"):
            raise HTTPException(status_code=400, detail="Le fichier doit être un .zip")
    
    zip_content = await zip_file.read()

    try:
        with zipfile.ZipFile(io.BytesIO(zip_content)) as zip_ref:
            
            #Liste contenant les noms des fichiers présents dans le zip pour pouvoir les traiter un par un
            filenames = zip_ref.namelist()

            results = []

            #On parcourt les fichiers du zip et on traite uniquement les fichiers PDF, doc et docx pour les classifier
            for filename in filenames:
                 if filename.lower().endswith(".pdf") or filename.lower().endswith(".docx") or filename.lower().endswith(".doc"):
                      with zip_ref.open(filename) as file:
                           file_bytes = file.read()

                           #Preprocesse le contenu du fichier puis classifie le document en utilisant la méthode de classification du classificateur de documents
                           label = classifier_engine.classify(file_bytes, filename)

                           results.append(ClassificationResponse(filename=filename, label=label))

    #En cas d'erreur lors du traitement du fichier zip, on renvoie une erreur 500 avec le message d'erreur détaillé pour aider à diagnostiquer le problème.
    except Exception as e:
                           
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement du fichier zip: {str(e)}")
    
    return results