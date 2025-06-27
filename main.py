import os
from src.unzip_and_parse import process_all_zips

if __name__ == "__main__":
    projetos_dir = "projetos"
    autodoc_dir = "autodoc"
    process_all_zips(projetos_dir, autodoc_dir)
    print("Processamento finalizado!")