import json
from collections import defaultdict
from ..utils import normalize_name  # ajuste o import se necessário

def _describe_literal(value):
    # Remove aspas simples e null do Power BI
    if isinstance(value, str) and value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    if value == "null":
        return "nulo"
    return str(value)

def _get_entity_and_column(expr):
    """Extrai o nome da tabela (entity) e coluna (property) de um filtro do Power BI."""
    entity = ""
    column = ""
    try:
        # Tenta pegar do SourceRef.Entity
        entity = expr["Column"]["Expression"]["SourceRef"].get("Entity")
    except Exception:
        # Se não achar, tenta SourceRef.Source
        try:
            entity = expr["Column"]["Expression"]["SourceRef"].get("Source")
        except Exception:
            entity = ""
    try:
        column = expr["Column"].get("Property")
    except Exception:
        column = ""
    return entity, column

def _describe_condition(cond):
    """Tenta descrever a condição de filtro de maneira natural."""
    if not isinstance(cond, dict):
        return str(cond)
    for key, value in cond.items():
        if key == "In":
            expressions = value.get("Expressions", [])
            colname = None
            if expressions:
                expr = expressions[0]
                colname = expr.get("Column", {}).get("Property", "coluna desconhecida")
            values = []
            for v in value.get("Values", []):
                if isinstance(v, list) and v:
                    lit = v[0].get("Literal", {}).get("Value")
                    values.append(_describe_literal(lit))
            return f"{colname or 'Coluna'} igual a {', '.join(values)}"
        if key == "Not":
            not_expr = _describe_condition(value.get("Expression"))
            return f"Exclui: {not_expr}"
        if key == "Between":
            lower = value.get("LowerBound", {}).get("Literal", {}).get("Value")
            upper = value.get("UpperBound", {}).get("Literal", {}).get("Value")
            return f"Entre {lower} e {upper}"
        if key == "And":
            return " e ".join([_describe_condition(c) for c in value])
        if key == "Or":
            return " ou ".join([_describe_condition(c) for c in value])
        return f"{key}: {_describe_condition(value)}"
    return str(cond)

def _group_filters_by_entity(filters_json, nomeprojeto):
    """Agrupa os filtros por tabela (entity) e gera wikilink para cada tabela."""
    grouped = defaultdict(list)
    for f in filters_json:
        expr = f.get("expression", {})
        entity, column = _get_entity_and_column(expr)
        normalized_entity = normalize_name(entity or "")
        where = f.get("filter", {}).get("Where", [])
        cond_desc = None
        if where:
            cond = where[0].get("Condition", {})
            cond_desc = _describe_condition(cond)
        inverted = None
        try:
            inverted = f["objects"]["general"][0]["properties"]["isInvertedSelectionMode"]["expr"]["Literal"]["Value"]
        except Exception:
            pass

        col_line = f"- **Coluna:** {column or '?'}"
        if cond_desc:
            col_line += f"\n  - **Filtro:** {cond_desc}"
        if inverted == "true":
            col_line += "\n  - **Seleção invertida**"
        grouped[(entity or "?", normalized_entity)].append(col_line)
    return grouped

def render_section_md(section, visuals_info, nomeprojeto, visual_file_names):
    """
    Gera markdown para uma section, com lista dos visuais (com wikilink completo e bonito) e mostra o atributo filters (se houver).
    visuals_info deve ser uma lista de dicts (output de extract_visual_properties).
    nomeprojeto é usado para construir o wikilink da tabela.
    visual_file_names: dict de id do visual para nome do arquivo (com .md).
    """
    display_name = section.get("displayName", "Sem Nome")
    section_file_name = normalize_name(display_name) # sem .md para wikilink
    out = [f"# {display_name}", ""]
    out.append("## Visuais nesta página")
    if visuals_info:
        for vis in visuals_info:
            vis_id = vis['id']
            vis_type = vis.get('visual_type', 'unnamed')
            nome_literal = vis.get("visual_nomeliteral") or vis.get("visual_name") or "unnamed"
            wikilink = visual_file_names.get(vis_id, "arquivo_nao_encontrado.md").replace('.md', '')
            wikilink_full = f"[[{nomeprojeto}/dataviz/visualcontainers/{wikilink}|{nome_literal}]]"
            out.append(
                f"- {wikilink_full} (**ID:** `{vis_id}`) - {vis_type}"
            )
    else:
        out.append("Nenhum visual encontrado nesta seção.")
    out.append("")

    filters = section.get("filters", None)
    if filters:
        try:
            filters_json = json.loads(filters)
        except Exception:
            filters_json = filters
        if isinstance(filters_json, list) and filters_json:
            out.append("## Filtros desta página")
            grouped = _group_filters_by_entity(filters_json, nomeprojeto)
            for (entity, normalized_entity), filter_lines in grouped.items():
                wikilink = f"[[{nomeprojeto}/tabelas/{normalized_entity}.md|{entity}]]"
                out.append(f"### {wikilink}")
                out.extend(filter_lines)
                out.append("")
            out.append("<details><summary>Ver JSON completo dos filtros</summary>")
            out.append("")
            out.append("```json")
            out.append(json.dumps(filters_json, indent=2, ensure_ascii=False))
            out.append("```")
            out.append("</details>")
            out.append("")
        else:
            out.append("## Filtros desta página (formato desconhecido)")
            out.append("```json")
            out.append(json.dumps(filters_json, indent=2, ensure_ascii=False))
            out.append("```")
            out.append("")

    out.append("---")
    out.append(f"#{normalize_name(nomeprojeto)} #dataviz")
    return "\n".join(out)

def render_visualcontainer_md(vis_info, section_display_name, section_file_name, nomeprojeto):
    vis_id = vis_info.get("id", "sem_id")
    vis_type = vis_info.get('visual_type', 'unnamed')
    vis_name = vis_info.get('visual_name', '')
    vis_md = []
    vis_md.append(f"# Visual ID: `{vis_id}`")
    vis_md.append(f"- **Tipo:** `{vis_type}`")
    vis_md.append(f"- **Nome:** `{vis_name}`")
    vis_md.append(f"- **Nome literal:** `{vis_info.get('visual_nomeliteral', '')}`")
    section_wikilink = f"[[{nomeprojeto}/dataviz/sections/{section_file_name}|{section_display_name}]]"
    vis_md.append(f"- **Section:** {section_wikilink}")
    vis_md.append(f"- **Posição:** x={vis_info.get('x')} y={vis_info.get('y')}")
    vis_md.append(f"- **Tamanho:** w={vis_info.get('width')} h={vis_info.get('height')}")
    vis_md.append("")
    
    # Adicione este bloco para as colunas da pivottable
    if vis_type and vis_type.lower() == "pivottable":
        from .dataviz_extractors import extract_column_displaynames_and_measures
        columns = extract_column_displaynames_and_measures(vis_info.get("config", ""))
        if columns:
            vis_md.append("")
            vis_md.append("## Colunas da PivotTable\n")
            for display_name, measure_name in columns:
                vis_md.append(f"- **{display_name}**\n\t- [[{nomeprojeto}/medidas/{normalize_name(measure_name)}|{measure_name}]]")
                
    vis_md.append("## Config")
    config = vis_info.get("config", "")
    if isinstance(config, str):
        try:
            config_json = json.loads(config)
            config_str = json.dumps(config_json, indent=2, ensure_ascii=False)
        except Exception:
            config_str = config
    else:
        try:
            config_str = json.dumps(config, indent=2, ensure_ascii=False)
        except Exception:
            config_str = str(config)
    vis_md.append("```json")
    vis_md.append(config_str)
    vis_md.append("```")
    
    
    vis_md.append("")
    vis_md.append("---")
    vis_md.append(f"#{normalize_name(nomeprojeto)} #dataviz")
    return "\n".join(vis_md)