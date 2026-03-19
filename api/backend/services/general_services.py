import ollama

class GeneralModel:
    def __init__(self, model_name: str = "qwen3.5:2b"):
        
        self.model_name = model_name

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
                    {"role": "system", "content": "Tu es un assistant généraliste qui répond à toutes les questions."},
                    {"role": "user", "content": input_data}
                ]
            )

            answer = response['message']['content'].strip() # On récupère la réponse de Ollama et on la nettoie pour n'avoir que le texte de la réponse

            return answer
        except Exception as e:
            print(f"Erreur lors de l'appel à Ollama pour l'entrée {input_data}: {e}")
            return "Erreur lors du traitement de la requête"
        
    def stream_chat(self, input_data: str):
        """Traite une entrée textuelle en utilisant le modèle de langage Ollama en mode chunked pour les longues entrées
        Args:
            input_data (str): L'entrée textuelle à traiter
        Returns:
            str: La réponse générée par le modèle de langage Ollama"""
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "Tu es un assistant généraliste qui répond à toutes les questions."},
                    {"role": "user", "content": input_data}
                ],
                stream=True, # On active le mode chunked pour recevoir la réponse en plusieurs parties
                options={
                "num_ctx": 2048,  # Réduit la mémoire réservée (plus rapide à charger)
                "low_vram": True, # Optimisation spécifique pour les cartes de 4Go
                "num_thread": 4   # Utilise ton processeur pour aider la carte graphique
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
