import py7zr
import zipfile
import io
import os

def process_zip_recursively(zip_file: bytes, path_output):
    """Traite un fichier zip ou 7z de manière récursive, en extrayant les fichiers et en les gérant en fonction de leur extension."""

    stream = io.BytesIO(zip_file)

    if zipfile.is_zipfile(stream):
        stream.seek(0)
        with zipfile.ZipFile(stream, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                if file_info.is_dir():
                    continue

                with zip_ref.open(file_info) as file:
                    content = file.read()
                    handle_file(file_info.filename, content, path_output)

    elif py7zr.is_7zfile(stream):
        stream.seek(0)
        with py7zr.SevenZipFile(stream, mode='r') as archive:
            all_files = archive.readall()
            for filename, bio in all_files.items():
                content = bio.read()
                handle_file(filename, content, path_output)


def handle_file(filename: str, content:bytes, path_output):
    """Gère les fichiers extraits en fonction de leur extension"""
    extension = filename.lower().split('.')[-1]
    
    if extension in {'zip', '7z'}:
        process_zip_recursively(content, path_output)  # Traite les fichiers zip ou 7z de manière récursive
    
    elif extension in {'pdf', 'docx', 'xlsx', 'pptx', 'txt', 'csv', 'json', 'xml','jpg', 'jpeg', 'png'} or os.path.splitext(filename)[1] == '':

        name_file = filename.replace('/', '_')  # Remplace les slashes pour éviter les problèmes de chemin

        #Appel la route d'indexation du moteur de RAG
        response = requests.post(f"{API_URL}/index", files={"file": (name_file, content)})
