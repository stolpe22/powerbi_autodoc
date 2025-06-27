import os
import zipfile
import json

from .md_render import render_tabela_md, render_medida_md
from .extractors import (
    extract_all_table_names,
    extract_all_measure_names,
    build_measures_reverse_map,
    build_measures_using_table_map,
    extract_measures_and_tables_dax,
)
from .utils import normalize_name

def process_all_zips(projetos_dir, autodoc_dir):
    for fname in os.listdir(projetos_dir):
        if fname.lower().endswith(".zip"):
            nomeprojeto = os.path.splitext(fname)[0]
            zip_path = os.path.join(projetos_dir, fname)
            print(f"Processando: {zip_path}")
            with zipfile.ZipFile(zip_path, "r") as zipf:
                for zinfo in zipf.infolist():
                    if zinfo.filename.lower().endswith("datamodelschema"):
                        with zipf.open(zinfo) as file:
                            raw = file.read()
                            try:
                                text = raw.decode("utf-16-le")
                            except Exception:
                                print(f"Erro ao decodificar {zinfo.filename} em {fname}")
                                continue
                            try:
                                data = json.loads(text)
                            except Exception as e:
                                print(f"Erro ao parsear JSON: {e}")
                                continue
                            salvar_documentacao(data, nomeprojeto, autodoc_dir)
                        break

def salvar_documentacao(data, nomeprojeto, autodoc_dir):
    basepath = os.path.join(autodoc_dir, nomeprojeto)
    tabelas_path = os.path.join(basepath, "tabelas")
    medidas_path = os.path.join(basepath, "medidas")
    os.makedirs(tabelas_path, exist_ok=True)
    os.makedirs(medidas_path, exist_ok=True)

    tables = data.get("model", {}).get("tables", [])
    all_tables = extract_all_table_names(tables)
    all_measures = extract_all_measure_names(tables)
    # NOVO: construa o mapa de medidas referenciadoras
    measures_reverse_map = build_measures_reverse_map(
        tables, all_measures, all_tables, extract_measures_and_tables_dax
    )
    
    measures_using_table_map = build_measures_using_table_map(
        tables, all_measures, all_tables, extract_measures_and_tables_dax
    )

    # Geração de documentação para TABELAS
    for table in tables:
        md = render_tabela_md(table, nomeprojeto, measures_using_table_map)
        tname = normalize_name(table.get("name", "tabela_sem_nome"))
        md_path = os.path.join(tabelas_path, f"{tname}.md")
        with open(md_path, "w", encoding="utf-8") as fout:
            fout.write(md)

    # Geração de documentação para MEDIDAS
    for table in tables:
        for measure in table.get("measures", []):
            md = render_medida_md(
                measure,
                nomeprojeto,
                table.get("name", ""),
                all_measures,
                all_tables,
                measures_reverse_map,
            )
            mname = normalize_name(measure.get("name", "medida_sem_nome"))
            md_path = os.path.join(medidas_path, f"{mname}.md")
            with open(md_path, "w", encoding="utf-8") as fout:
                fout.write(md)