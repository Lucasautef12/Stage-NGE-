import os 
import zipfile
from PyPDF2 import PdfReader
from docx import Document
from striprtf.striprtf import rtf_to_text
import shutil
import time
import fitz


path_data = './data/'


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

def remove_obsolet_files(path):
    for entry in os.scandir(path):
        if entry.is_file() and (entry.name.endswith('.zip') or entry.name.endswith('.dwg') or entry.name.endswith('.ifc') or entry.name.endswith('.bcp')):
            os.remove(entry.path)
        elif entry.is_dir():
            remove_obsolet_files(entry.path)

if __name__ == "__main__":
    name_folder1 = "LARMOR PLAGE (56) Résidence Riva Ilot Chaton"
    remove_obsolet_files(path_data)




    