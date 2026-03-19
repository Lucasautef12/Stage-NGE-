from pydantic import BaseModel, Field

class ClassificationRequest(BaseModel):
    """Schéma de requête pour la classification d'un document à partir de son contenu textuel
    Attributes:
        filename (str): Le nom du fichier à classifier
        content (str): Le contenu du fichier à classifier
    """

    filename : str = Field(..., description="Le nom du fichier à classifier")
    content : str = Field(..., description="Le contenu du fichier à classifier")

class ClassificationResponse(BaseModel):
    """Schéma de réponse pour la classification d'un document
    Attributes:
         filename (str): Le nom du fichier classifié
         label (str): Le label de classification du document
    """

    filename : str = Field(..., description="Le nom du fichier classifié")
    label : str = Field(..., description="Le label de classification du document")

class BatchClassificationResponse(BaseModel):
    """Schéma de réponse pour la classification en batch de plusieurs documents
    Attributes:
         results (List[ClassificationResponse]): La liste des résultats de classification pour chaque document classifié
    """
    
    results: list[ClassificationResponse] = Field(..., description="Liste des résultats de classification")
