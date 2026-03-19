import ollama
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from pathlib import Path
import sys
from dotenv import load_dotenv
import os

#On ajoute le dossier "api" au path pour pouvoir importer les modules du dossier "services" et "rooters" sans problème d'importation
BASE_dir = Path(__file__).resolve().parent.parent.parent
print(f"BASE_dir: {BASE_dir}")
if str(BASE_dir) not in sys.path:
    sys.path.append(str(BASE_dir))

load_dotenv(BASE_dir / ".env")

qdrant_path = os.getenv("QDRANT_PATH") #Récupération de la variable d'environnement 
if not os.path.exists(BASE_dir / qdrant_path):
    os.makedirs(BASE_dir / qdrant_path)  # Créer le dossier de sortie s'il n'existe pas


class GeneralModel:
    def __init__(self, model_name: str = "qwen3.5:2b"):
        
        self.model_name = model_name

        self.vector_db = QdrantClient(path=BASE_dir / qdrant_path)

    def process(self, input_data: str) -> str:
        """Traite une entrée textuelle en utilisant le modèle de langage Ollama
        Args:
            input_data (str): L'entrée textuelle à traiter
        Returns:
            str: La réponse générée par le modèle de langage Ollama"""
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "Tu es un assistant généraliste qui répond à toutes les questions"
                    }
                ]
            )

            answer = response['message']['content'].strip() # On récupère la réponse de Ollama et on la nettoie pour n'avoir que le texte de la réponse

            return answer
        except Exception as e:
            print(f"Erreur lors de l'appel à Ollama pour l'entrée {input_data}: {e}")
            return "Erreur lors du traitement de la requête"
        
    def look_for_in_vector_db(self, query: str, k: int = 3) -> str:
        """Effectue une recherche dans la base de données vectorielle pour trouver des documents pertinents en fonction d'une requête
        Args:
            query (str): La requête de recherche
            k (int): Le nombre de documents à retourner
        Returns:
            str: Les résultats de la recherche formatés en texte"""

        docs = self.vector_db.similarity_search(query, k=k) # On effectue une recherche de similarité dans la base de données vectorielle pour trouver les k documents les plus pertinents

        results = "\n\n".join([f"Document: {doc.metadata['filename']}\nContenu: {doc.page_content}" for doc in docs]) # On formate les résultats de la recherche pour les inclure dans la réponse de Ollama

        return results
        
    def stream_chat(self, input_data: str):
        """Traite une entrée textuelle en utilisant le modèle de langage Ollama en mode chunked pour les longues entrées
        Args:
            input_data (str): L'entrée textuelle à traiter
        Returns:
            str: La réponse générée par le modèle de langage Ollama"""
        
        context = self.look_for_in_vector_db(input_data) # On effectue une recherche dans la base de données vectorielle pour trouver des documents pertinents en fonction de l'entrée textuelle
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": f"Tu es un assistant généraliste qui répond à toutes les questions.\
                     Voici les documents pertinents que tu peux utiliser pour répondre à la question de l'utilisateur: {context} "
                    ""},
                    {"role": "user", "content": input_data}
                ],
                stream=True, # On active le mode chunked pour recevoir la réponse en plusieurs parties
                options={
                "num_ctx": 2048,  # Réduit la mémoire réservée (plus rapide à charger)
                "low_vram": True, # Optimisation spécifique pour les cartes de 4Go
                "num_thread": 4   # Utilise le processeur pour aider la carte graphique
            }
                    )

            answer = ""
            for chunk in response:
                if 'message' in chunk and 'content' in chunk['message']:
                    content = chunk['message']['content']
                    
                    yield content

            print("\n")
            return answer # On nettoie la réponse finale pour n'avoir que le texte de la réponse
        except Exception as e:
            print(f"Erreur lors de l'appel à Ollama pour l'entrée {input_data}: {e}")
            return "Erreur lors du traitement de la requête"

general_engine = GeneralModel()
general_engine.stream_chat("Qu'est ce que eurocode ?")
