import os
import zipfile
import json

from .dataviz_extractors import (
    extract_sections_from_layout,
    extract_section_display_name,
    extract_visuals_from_section,
    extract_visual_properties,
)
from .dataviz_md_render import render_section_md, render_visualcontainer_md
from ..utils import normalize_name

def dataviz_process_all_zips(projetos_dir, autodoc_dir):
    for fname in os.listdir(projetos_dir):
        if not fname.lower().endswith(".zip"):
            continue
        nomeprojeto = os.path.splitext(fname)[0]
        zip_path = os.path.join(projetos_dir, fname)
        print(f"Processando dataviz: {zip_path}")
        try:
            layout = _dataviz_load_layout_from_zip(zip_path)
        except Exception as e:
            print(f"Erro ao ler Layout de {zip_path}: {e}")
            continue
        _dataviz_salvar_documentacao(layout, nomeprojeto, autodoc_dir)

def _dataviz_load_layout_from_zip(zip_path):
    with zipfile.ZipFile(zip_path, "r") as zipf:
        # Procura por "Report/Layout" (case-insensitive)
        layout_file = next(
            (
                zinfo
                for zinfo in zipf.infolist()
                if zinfo.filename.lower().replace("\\", "/") == "report/layout"
            ),
            None,
        )
        if not layout_file:
            raise FileNotFoundError("Arquivo Report/Layout não encontrado no zip.")
        with zipf.open(layout_file) as file:
            text = file.read().decode("utf-16-le")
            layout = json.loads(text)
            return layout

def _dataviz_salvar_documentacao(layout, nomeprojeto, autodoc_dir):

    sections_path = os.path.join(autodoc_dir, nomeprojeto, "dataviz", "sections")
    os.makedirs(sections_path, exist_ok=True)

    sections = extract_sections_from_layout(layout)
    if not sections:
        with open(os.path.join(sections_path, "_nenhuma_section_encontrada.md"), "w", encoding="utf-8") as fout:
            fout.write("Nenhuma section encontrada no layout.\n")
        print(f"Nenhuma section encontrada para {nomeprojeto}")
        return

    visual_file_names = {}
    for section in sections:
        visual_containers = extract_visuals_from_section(section)
        for vis in visual_containers:
            vis_info = extract_visual_properties(vis)
            vis_type = vis_info.get("visual_type", "unnamed").lower()
            vis_title_literal = vis_info.get("visual_nomeliteral")
            vis_id = vis_info.get("id", "sem_id")
            if vis_title_literal:
                fname = f"{vis_type}_{normalize_name(vis_title_literal)}_{vis_id}.md"
            else:
                fname = f"{vis_type}_unnamed_{vis_id}.md"
            visual_file_names[vis_id] = fname

    # 2. Agora passe visual_file_names para render_section_md:
    for section in sections:
        display_name = extract_section_display_name(section)
        visual_containers = extract_visuals_from_section(section)
        visuals_info = [extract_visual_properties(vis) for vis in visual_containers]
        md = render_section_md(section, visuals_info, nomeprojeto, visual_file_names)
        fname = f"{display_name.replace('/', '_').replace(' ', '_')}.md"
        with open(os.path.join(sections_path, fname), "w", encoding="utf-8") as fout:
            fout.write(md)

    # Gerando os arquivos dos visualcontainers com tipo_nome-literal ou tipo_unnamed
    visualcontainers_path = os.path.join(autodoc_dir, nomeprojeto, "dataviz", "visualcontainers")
    os.makedirs(visualcontainers_path, exist_ok=True)
    for section in sections:
        display_name = extract_section_display_name(section)
        section_file_name = normalize_name(display_name)
        visual_containers = extract_visuals_from_section(section)
        for vis in visual_containers:
            vis_info = extract_visual_properties(vis)
            vis_md = render_visualcontainer_md(vis_info, display_name, section_file_name, nomeprojeto)
            vis_title_literal = vis_info.get("visual_nomeliteral")
            vis_type = vis_info.get("visual_type", "unnamed").lower()
            vis_id = vis_info.get("id", "sem_id")
            if vis_title_literal:
                fname = f"{vis_type}_{normalize_name(vis_title_literal)}_{vis_id}.md"
            else:
                fname = f"{vis_type}_unnamed_{vis_id}.md"
            with open(os.path.join(visualcontainers_path, fname), "w", encoding="utf-8") as fout:
                fout.write(vis_md)