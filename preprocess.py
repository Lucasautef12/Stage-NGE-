import os 
import zipfile
from PyPDF2 import PdfReader
import py7zr
path_data = './data/'

def preprocess(folder):
    for entry in os.scandir(folder):
        if entry.is_file() and (entry.name.endswith('.zip') or entry.name.endswith('.Zip')):
            zip_path = entry.path
            extract_path = zip_path[:-4]

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
                    
                preprocess(extract_path)

            os.remove(zip_path)
        
        elif entry.is_file() and entry.name.endswith('.7z'):
            with py7zr.SevenZipFile(entry.path, mode='r') as archive:
                archive.extractall(path=entry.path[:-3])

            os.remove(entry.path)
            preprocess(entry.path[:-3])            

        elif entry.is_file() and (entry.name.endswith('.dwg') or entry.name.endswith('.ifc') or entry.name.endswith('.bcp') or entry.name.endswith('.2d') or entry.name.endswith('.3d') or entry.name.endswith('.pc3') or entry.name.endswith('.ctb') or entry.name.endswith('.bak') or entry.name.endswith('.css') or entry.name.endswith('.2db') or entry.name.endswith('.xsl') or os.path.splitext(entry.name)[1] == '' ):
            os.remove(entry.path)

        elif entry.is_dir():
            preprocess(entry.path)

        #Remove the empty directories
        if entry.is_dir() and len(os.listdir(entry.path)) == 0:
            os.rmdir(entry.path)

if __name__ == "__main__":
    name_folder1 = "LARMOR PLAGE (56) Résidence Riva Ilot Chaton"
    preprocess(path_data)