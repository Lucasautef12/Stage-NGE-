#Read a USB key 
import os 
import zipfile
from PyPDF2 import PdfReader
from docx import Document
from striprtf.striprtf import rtf_to_text
import shutil
import time

path_data = './data/'

def dezipp(folder):
    for entry in os.scandir(folder):
        if entry.is_file() and entry.name.endswith('.zip'):
            zip_path = entry.path
            extract_path = zip_path[:-4]

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
                
                dezipp(extract_path)
        elif entry.is_dir():
            dezipp(entry.path)

def count_files_in_folder(path):
    #Count the number of files in a folder and its subfolders (we consider the folder is decompressed)
    count = 0
    for entry in os.scandir(path):
        if entry.is_file() and not entry.name.endswith('.zip'):
            count += 1
        elif entry.is_dir():
            count += count_files_in_folder(entry.path)
    return count

def list_all_formats(path):
    formats = set()
    
    if os.path.isfile(path) and not path.endswith('.zip'):
        formats.add(os.path.splitext(path)[1])
    else:
        with os.scandir(path):
            for entry in os.scandir(path):
                if entry.is_file() and not entry.name.endswith('.zip'):
                    formats.add(os.path.splitext(entry.name)[1])
                elif entry.is_dir():
                    new_path = os.path.join(path, entry.name)
                    formats.update(list_all_formats(new_path))
    return formats




if __name__ == "__main__":
    name_folder = "METZ (57) Crous Saulcy"
    path_folder = path_data + name_folder

    time0 = time.time()
    dezipp(path_folder)
    time1 = time.time()
    print(f"Decompression completed in {time1 - time0:.2f} seconds")
    