from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
from backend.services.general_services import general_engine

router = APIRouter()

@router.post("/process")
async def process_input(input_data: str):
    """Endpoint pour traiter une entrée textuelle en utilisant le modèle de langage Ollama
    Args:
        input_data (str): L'entrée textuelle à traiter
    Returns:
        str: La réponse générée par le modèle de langage Ollama"""
    
    #On appelle la méthode de traitement du moteur généraliste en lui passant l'entrée textuelle pour obtenir la réponse générée par le modèle de langage Ollama
    response = general_engine.process_chunked(input_data)

    return {"response": response}

@router.post("/chat")
async def chat(input_data: str):
    """Endpoint pour discuter avec le modèle de langage Ollama en mode streaming
    Args:
        input_data (str): L'entrée textuelle à traiter
    Returns:
        str: La réponse générée par le modèle de langage Ollama"""
    
    #On appelle la méthode de chat en streaming du moteur généraliste en lui passant l'entrée textuelle
    return StreamingResponse(
        general_engine.stream_chat(input_data), 
        media_type="text/event-stream"
    )