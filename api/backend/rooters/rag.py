from fastapi import APIRouter, UploadFile, File
from backend.services.rag_services import rag_engine

router = APIRouter()

@router.post("/index")
async def index_documents(file: UploadFile = File(...)):
    """Endpoint pour indexer des documents à partir de leur contenu et de leur nom de fichier
    Args:
        file (UploadFile): Le fichier à indexer
    Returns:
        dict: Un message indiquant que les documents ont été indexés avec succès
    """

    #On lit le contenu du fichier téléchargé et on le prétraite pour extraire le texte du PDF
    #et ajouter le nom du fichier au début du texte
    content = await file.read()

    #On appelle la méthode d'indexation du moteur de RAG en lui passant le contenu prétraité
    #du fichier pour indexer les documents dans la base de données vectorielle
    rag_engine.index(content, file.filename)

    return {"message": "Documents indexés avec succès."}