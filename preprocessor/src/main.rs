use std::fs;
use std::io;
use std:path:Path;
use zip:ZipArchive;

/// Fonction principale de prétraitement d'un dossier DCE
fn preprocess(dir: &Path) -> anyhow::Result<()> {
    for entry in fs::read_dir(dir)? {
        let entry = entry?;
        let path = entry.path()

        /// Liste des extensions de fichiers autorisées à être traitées
        const ALLOWED_EXTENSIONS: &[&str] = &[".xml", ".pdf", ".xls", ".rtf", ".txt", ".jpg", ".xlsx", ".docx", ".png", ".JPG"];

        if path.is_file() {

            let extension = path.extension().and_then(|s| s.to_str()).unwrap_or("").to_lowercase();
            /// Si c'est un fichier ZIP, on le décompresse
            
            if extension == "zip" {
                let folder_name = path.file_stem().unwrap().to_os_string();
                let unzip_target = path.parent().unwrap().join(folder_name);
                
                ///Dezipper le fichier ZIP
                unzip_file(&path, &unzip_target)?;
                
                /// Suppression du ZIP après extraction
                fs::remove_file(&path)?;

                /// Récursion pour fouiller le nouveau dossier compressé
                preprocess(&unzip_target)?;
            }
            /// Si c'est un fichier avec une extension autorisée, on le garde
            else {
                
                if !ALLOWED_EXTENSIONS.contains(&extension.as_str()) {
                    fs::remove_file(&path)?;
                }
            }

        else if path.is_dir() {
            /// Si c'est un dossier, on continue à fouiller dedans
            preprocess(&path)?;

            /// Après avoir traité le dossier, on vérifie s'il est vide et on le supprime si c'est le cas
            if fs::read_dir(&path)?.next().is_none() {
                fs::remove_dir(&path)?;
            }

    Ok(())
}
        }
    }
}

fn unzip_file(zip_path: &Path, target: &Path) -> anyhow::Result<()> {
    let file = fs::File::open(zip_path)?;
    let mut archive = ZipArchive::new(file)?;
    
    fs::create_dir_all(target)?;
    
    for i in 0..archive.len() {
        let mut file = archive.by_index(i)?;
        let outpath = target.join(file.mangled_name());

        if file.is_dir() {
            fs::create_dir_all(&outpath)?;
        } else {
            if let Some(p) = outpath.parent() { fs::create_dir_all(p)?; }
            let mut outfile = fs::File::create(&outpath)?;
            std::io::copy(&mut file, &mut outfile)?;
        }
    }
    Ok(())
}