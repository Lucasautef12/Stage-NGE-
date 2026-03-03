import os 
import zipfile
from PyPDF2 import PdfReader
from docx import Document
from striprtf.striprtf import rtf_to_text
import shutil
import time
import fitz


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

def count_files_by_format(path):
    format_counts = {}

    def count_files_by_format_rec(path):
        for entry in os.scandir(path):
            format = os.path.splitext(entry.name)[1]
            if entry.is_file() and not entry.name.endswith('.zip') and format != '':
                if format in format_counts:
                    format_counts[format] += 1
                else:
                    format_counts[format] = 1
            elif entry.is_dir():
                new_path = os.path.join(path, entry.name)
                count_files_by_format_rec(new_path)
    
    count_files_by_format_rec(path)

    return format_counts

def is_plan(path_pdf):
    doc = fitz.open(path_pdf)

    for i, page in enumerate(doc):
        draw = page.get_drawings()
        nb_drawings = len(draw)

        words = page.get_text("words")
        nb_words = len(words)

        if nb_drawings > nb_words:
            return True
    
    return False


def count_number_plans(path):
    count = 0

    for entry in os.scandir(path):
        if entry.is_file() and entry.name.endswith('.pdf') and is_plan(entry.path):
            count += 1
        elif entry.is_dir():
            count += count_number_plans(entry.path)

    return count

if __name__ == "__main__":
    name_folder1 = "LARMOR PLAGE (56) Résidence Riva Ilot Chaton"
    path_folder1 = path_data + name_folder1

    #nb_plans1 = count_number_plans(path_folder1)
    #print(f"Number of plans in {name_folder1} : {nb_plans1}")

    name_folder2 = "EPONE (78) Collège Benjamin FRANKLIN"
    path_folder2 = path_data + name_folder2

    nb_plans2 = count_number_plans(path_folder2)
    print(f"Number of plans in {name_folder2} : {nb_plans2}")

    name_folder_3  = "METZ (57) Crous Saulcy"
    path_folder_3 = path_data + name_folder_3

    #nb_plans_3 = count_number_plans(path_folder_3)
    #print(f"Number of plans in {name_folder_3} : {nb_plans_3}")




    