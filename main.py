import os
from src.models.project_processor import ProjectProcessor
from src.dataviz.dataviz_unzip_and_parse import dataviz_process_all_zips

if __name__ == "__main__":
    projetos_dir = "projetos"
    autodoc_dir = "autodoc"

    # Documentação do modelo (tabelas, medidas, RLS) utilizando a abordagem orientada a objetos
    processor = ProjectProcessor(autodoc_dir)
    processor.process_all_zips(projetos_dir)

    # Documentação dataviz (Layout: seções e visuais)
    dataviz_process_all_zips(projetos_dir, autodoc_dir)

    print("Processamento finalizado!")