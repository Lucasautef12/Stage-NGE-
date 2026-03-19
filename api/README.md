# 🏗️ NGE API - Document Classifier

Cette API FastAPI est conçue pour permettre à **Copilot** d'interagir avec les services de classification de documents de NGE. Elle utilise une architecture modulaire pour faciliter la maintenance et l'évolution du moteur d'IA.

## 📂 Architecture du Projet

Le projet est découpé en deux pôles distincts (Frontend et Backend) afin d'isoler l'interface utilisateur de la logique métier.

### 🎨 Frontend (`/frontend`)
Regroupe les composants liés à l'interface utilisateur.
* **`app.py`** : Point d'entrée de l'application **Streamlit**. Gère l'affichage, la capture des documents utilisateur et les appels API vers le backend.

### ⚙️ Backend (`/backend`)
Cœur technologique de l'application, structuré en couches pour séparer les responsabilités :

* **`main.py`** : Point d'entrée de l'API. Configure **FastAPI** et centralise les routeurs.
* **`routers/`** : Contient les définitions des routes. C'est ici que sont exposées les fonctionnalités vers l'extérieur.
* **`schemes/`** : Définit les modèles **Pydantic** pour la validation des données entrantes et sortantes (contrats JSON).
* **`services/`** : Héberge la logique métier pure (ex : le moteur de classification `DocumentClassifier`).
* **`models/`** : Répertoire local de stockage pour les modèles open source **Hugging Face** (évite les téléchargements redondants).
* **`output/`** : Dossier de destination pour le stockage des dossiers extraits et des documents traités.

---## 📂 Architecture du Projet

Le projet est découpé en deux pôles distincts (Frontend et Backend) afin d'isoler l'interface utilisateur de la logique métier.

### 🎨 Frontend (`/frontend`)
Regroupe les composants liés à l'interface utilisateur.
* **`app.py`** : Point d'entrée de l'application **Streamlit**. Gère l'affichage, la capture des documents utilisateur et les appels API vers le backend.

### ⚙️ Backend (`/backend`)
Cœur technologique de l'application, structuré en couches pour séparer les responsabilités :

* **`main.py`** : Point d'entrée de l'API. Configure **FastAPI**, gère les middlewares et centralise les routeurs.
* **`routers/`** : Contient les définitions des endpoints (routes). C'est ici que sont exposées les fonctionnalités vers l'extérieur.
* **`schemes/`** : Définit les modèles **Pydantic** pour la validation des données entrantes et sortantes (contrats JSON).
* **`services/`** : Héberge la logique métier pure (ex : le moteur de classification `DocumentClassifier`).
* **`models/`** : Répertoire local de stockage pour les modèles open source **Hugging Face** (évite les téléchargements redondants).
* **`outputs/`** : Dossier de destination pour le stockage des dossiers extraits et des documents traités.

---

## 🚀 Installation et Lancement

### 1. Création d'un environnement virtuel 

```bash
py -m venv env
```

### 2. Activation de l'environnement virtuel

```bash
.\env\Scripts\activate
```

### 3. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 4. Executer l'API

Depuis le dossier api :

```bash
uvicorn main:app --reload
```



