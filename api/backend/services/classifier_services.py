from dotenv import load_dotenv
import fitz
from typing import List
import io
from PIL import Image
import ollama

class DocumentClassifier:
    def __init__(self, model_name : str = "qwen2.5vl:3b"):
        """Initialise le classificateur de documents en chargeant le modèle de classification zéro-shot de Hugging Face"""

        self.model_name = model_name
        self.labels = ["Plan technique", "Planning", "Devis quantitatif", "Rapport d'étude de sol", "Autre"] 
        # Les labels de classification possibles pour les documents, correspondant aux catégories de dossiers de projet dans lesquelles les documents classifiés seront rangés.
        # Un label, concrètement, correspondera à un dossier de projet dans lequel le document classifié sera rangé.

        self.prompt = f"""Tu es un assistant de classification de documents DCE. 
        Choisis impérativement une catégorie racine parmi : {', '.join(self.labels)}.
        Si le document est très spécifique, tu peux ajouter un sous-dossier (Ex: 'Plan technique/Charpente').
        Réponse attendue : CATEGORIE_RACINE ou CATEGORIE_RACINE/SOUS_DOSSIER uniquement.""" 


    def classify(self, pdf_bytes: bytes, filename: str) -> str:
        """Classifie un document en fonction de son contenu et de son nom de fichier
        Args:
            pdf_bytes (bytes): Les bytes du document PDF à classifier
            filename (str): Le nom du fichier
        Returns:
            str: Le label de classification du document"""
        
        img_bytes = self.preprocess(pdf_bytes) # On prétraite le document PDF pour en extraire une image de la première page à passer à Ollama pour la classification

        try:
            # On appelle Ollama pour obtenir la classification du document à partir de son image
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.prompt},
                    {"role": "user", "content": f"Fichier : {filename}", "images": [img_bytes]}
                ]
            )

            answer = response['message']['content'].strip() # On récupère la réponse de Ollama et on la nettoie pour n'avoir que le label de classification

            return answer
        except Exception as e:
            print(f"Erreur lors de l'appel à Ollama pour le document {filename}: {e}")
            return "Erreur d'analyse"


    def classify_folder(self, pdf_list: List[bytes], filenames: List[str]) -> List[str]:
        """
        Classifie une liste de documents PDF.
        Args:
            pdf_list (List[bytes]): Liste des contenus PDF en bytes.
            filenames (List[str]): Liste des noms de fichiers correspondants.
        Returns:
            List[str]: Liste des labels prédits.
        """
        
        return [self.classify(pdf, name) for pdf, name in zip(pdf_list, filenames)]
    
    def preprocess(self, pdf_bytes:bytes) -> bytes:
        """
        Prétraite le contenu d'un document PDF en extrayant le texte de ses pages et en limitant le nombre de pages à 2 pour éviter les problèmes de mémoire.
        On ajoute également le nom du fichier au début du texte pour aider le modèle de classification à mieux comprendre le contexte du document.
        """

        # On utilise la bibliothèque PyMuPDF (fitz) pour extraire le texte du PDF.
        # On ouvre le PDF à partir des bytes du fichier et on lit les pages une par une pour extraire le texte.
        
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        page = doc[0] # On lit la première page du PDF
        pix = page.get_pixmap(dpi=50) # On convertit la page en image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # On convertit l'image en bytes pour pouvoir la passer à Ollama
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()

        return img_bytes


#Instancie le classificateur de documents pour pouvoir l'utiliser dans les endpoints de classification de documents définis dans le routeur classifier.py
classifier_engine  = DocumentClassifier()