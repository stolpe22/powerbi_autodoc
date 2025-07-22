import os
import zipfile
import json
from .extractors import (
    extract_all_table_names,
    extract_all_measure_names,
    build_measures_reverse_map,
    build_measures_using_table_map,
    extract_measures_and_tables_dax,
    build_relationships_by_table
)
from .measure_md_renderer import MedidaMDRenderer
from .table_md_renderer import TabelaMDRenderer
from .rls_md_renderer import RLSMDRenderer
from ..utils import normalize_name

class ProjectProcessor:
    def __init__(self, autodoc_dir):
        self.autodoc_dir = autodoc_dir
        self.medida_renderer = MedidaMDRenderer()
        self.tabela_renderer = TabelaMDRenderer()
        self.rls_renderer = RLSMDRenderer()

    def process_zip(self, zip_path):
        nomeprojeto = os.path.splitext(os.path.basename(zip_path))[0]
        with zipfile.ZipFile(zip_path, "r") as zipf:
            for zinfo in zipf.infolist():
                if zinfo.filename.lower().endswith("datamodelschema"):
                    with zipf.open(zinfo) as file:
                        raw = file.read()
                        try:
                            text = raw.decode("utf-16-le")
                            data = json.loads(text)
                        except Exception as e:
                            print(f"Erro ao processar {zip_path}: {e}")
                            return
                        self._save_documentation(data, nomeprojeto)
                    break

    def _save_documentation(self, data, nomeprojeto):
        basepath = os.path.join(self.autodoc_dir, nomeprojeto)
        tabelas_path = os.path.join(basepath, "tabelas")
        medidas_path = os.path.join(basepath, "medidas")
        os.makedirs(tabelas_path, exist_ok=True)
        os.makedirs(medidas_path, exist_ok=True)

        tables = data.get("model", {}).get("tables", [])
        roles = data.get("model", {}).get("roles", [])
        relationships = data.get("model", {}).get("relationships", [])
        all_tables = extract_all_table_names(tables)
        all_measures = extract_all_measure_names(tables)
        measures_reverse_map = build_measures_reverse_map(
            tables, all_measures, all_tables, extract_measures_and_tables_dax
        )
        measures_using_table_map = build_measures_using_table_map(
            tables, all_measures, all_tables, extract_measures_and_tables_dax
        )
        relationships_by_table = build_relationships_by_table(relationships)

        for table in tables:
            md = self.tabela_renderer.render(table, nomeprojeto, measures_using_table_map, relationships_by_table)
            tname = normalize_name(table.get("name", "tabela_sem_nome"))
            with open(os.path.join(tabelas_path, f"{tname}.md"), "w", encoding="utf-8") as fout:
                fout.write(md)

        for table in tables:
            for measure in table.get("measures", []):
                md = self.medida_renderer.render(
                    measure,
                    nomeprojeto,
                    table.get("name", ""),
                    all_measures,
                    all_tables,
                    measures_reverse_map,
                )
                mname = normalize_name(measure.get("name", "medida_sem_nome"))
                with open(os.path.join(medidas_path, f"{mname}.md"), "w", encoding="utf-8") as fout:
                    fout.write(md)

        if roles:
            rls_md = self.rls_renderer.render(roles, nomeprojeto)
            with open(os.path.join(basepath, "RLS.md"), "w", encoding="utf-8") as fout:
                fout.write(rls_md)

    def process_all_zips(self, projetos_dir):
        for fname in os.listdir(projetos_dir):
            if fname.lower().endswith(".zip"):
                self.process_zip(os.path.join(projetos_dir, fname))