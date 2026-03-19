import qdrant_client
from qdrant_client.models import PointStruct, VectorParams, Distance
import uuid
import ollama
from docling.document_converter import DocumentConverter
from langchain_text_splitters import RecursiveCharacterTextSplitter
import io
from docling.datamodel.base_models import DocumentStream
import os 
from pathlib import Path
import sys
from dotenv import load_dotenv

os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"

#On ajoute le dossier "api" au path pour pouvoir importer les modules du dossier "services" et "rooters" sans problème d'importation
BASE_dir = Path(__file__).resolve().parent.parent.parent
print(f"BASE_dir: {BASE_dir}")
if str(BASE_dir) not in sys.path:
    sys.path.append(str(BASE_dir))

load_dotenv(BASE_dir / ".env")

qdrant_path = os.getenv("QDRANT_PATH") #Récupération de la variable d'environnement 
if not os.path.exists(BASE_dir / qdrant_path):
    os.makedirs(BASE_dir / qdrant_path)  # Créer le dossier de sortie s'il n'existe pas

class RAG:
    def __init__(self):
        
        #Create the qdrant client to connect to the vector database
        self.qdrant_client = qdrant_client.QdrantClient(
            path=BASE_dir / qdrant_path, # URL de connexion à la base de données vectorielle Qdrant, en local 
            prefer_grpc=False, # Utilise gRPC pour une communication plus rapide avec la base de données vectorielle
        )

        self.converter = DocumentConverter()  # Initialise le convertisseur de documents pour extraire le texte des fichiers PDF, DOCX, etc.

        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)  # Initialise le splitter de texte pour diviser le texte extrait des documents en chunks de taille appropriée pour l'indexation dans la base de données vectorielle
       
        self.embedding_model_name = "nomic-embed-text"
        self.vector_size = 768 

        self._setup_collection()
    
    def _setup_collection(self):
        """Vérifie ou crée la collection au démarrage"""
        collection_name = "documents"
        collections = self.qdrant_client.get_collections().collections
        if not any(c.name == collection_name for c in collections):
            self.qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE) # 384 = taille all-MiniLM
            )

    def get_embedding(self, text: str):
        """Utilise Ollama pour générer l'embedding d'un texte"""
        response = ollama.embeddings(model=self.embedding_model_name, prompt=text)
        return response['embedding']
    
    def parse_content(self, content: bytes, filename: str) -> str:
        # Créer un flux de données à partir des bytes du document pour le traitement
        buf = io.BytesIO(content)
        
        #On encapsule dans un DocumentStream (Docling adore ça)
        source = DocumentStream(name=filename, stream=buf)
        
        # 3. On utilise convert qu accepte stream
        result = self.converter.convert(source)
        
        return result.document.export_to_markdown() 
       
    def index(self, content: bytes, filename: str):
        """Indexe les documents dans la base de données vectorielle en utilisant le moteur de RAG
        Args:
            content (bytes): Le contenu du document à indexer
            filename (str): Le nom du fichier du document à indexer
        Returns:
            dict: Un message indiquant que les documents ont été indexés avec succès
        """

        text = self.parse_content(content, filename)  # Parse le contenu du document pour extraire le texte à indexer dans la base de données vectorielle

        chunks = self.text_splitter.split_text(text)  # Divise le texte extrait du document en chunks de taille appropriée pour l'indexation dans la base de données vectorielle

        points = []
        for i, text in enumerate(chunks):
            vector = self.get_embedding(text)
            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"filename": filename, "text": text, "chunk": i}
            ))

        # Upload vers la collection
        self.qdrant_client.upsert(
            collection_name="documents",
            points=points
        )

        return {"status": "success", "message": "Documents indexés avec succès."}
    
rag_engine = RAG()