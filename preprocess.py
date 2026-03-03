import os 
import zipfile
from PyPDF2 import PdfReader
from docx import Document
from striprtf.striprtf import rtf_to_text
import shutil
import time
import fitz

path_data = './data/'

def preprocess(folder):
    for entry in os.scandir(folder):
        if entry.is_file() and entry.name.endswith('.zip'):
            zip_path = entry.path
            extract_path = zip_path[:-4]

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
                    
                preprocess(extract_path)

            os.remove(zip_path)
            
        elif entry.is_file() and (entry.name.endswith('.dwg') or entry.name.endswith('.ifc') or entry.name.endswith('.bcp')):
            os.remove(entry.path)

        elif entry.is_dir():
            preprocess(entry.path)


if __name__ == "__main__":
    name_folder1 = "LARMOR PLAGE (56) Résidence Riva Ilot Chaton"
    preprocess(path_data)