import os
from src.unzip_and_parse import process_all_zips
from src.dataviz_unzip_and_parse import dataviz_process_all_zips

if __name__ == "__main__":
    projetos_dir = "projetos"
    autodoc_dir = "autodoc"

    # Documentação do modelo (tabelas, medidas, RLS)
    process_all_zips(projetos_dir, autodoc_dir)

    # Documentação dataviz (Layout: seções e visuais)
    dataviz_process_all_zips(projetos_dir, autodoc_dir)

    print("Processamento finalizado!")