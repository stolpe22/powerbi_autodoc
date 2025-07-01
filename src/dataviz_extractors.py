import json

def extract_sections_from_layout(layout_json):
    """Extrai todas as sections (páginas) do layout."""
    return layout_json.get("sections", [])

def extract_section_display_name(section):
    """Extrai o displayName (nome amigável) da seção."""
    return section.get("displayName", "")

def extract_visuals_from_section(section):
    """Extrai todos os visualContainers (visuais) de uma section."""
    return section.get("visualContainers", [])

import json

def extract_visual_nomeliteral_from_config(config):
    try:
        config_json = json.loads(config) if isinstance(config, str) else config
        single_visual = config_json.get("singleVisual")
        if not single_visual:
            return None
        vcobjects = single_visual.get("vcObjects") or single_visual.get("vcobjects")
        if not vcobjects:
            return None
        title_arr = vcobjects.get("title")
        if not title_arr or not isinstance(title_arr, list) or len(title_arr) == 0:
            return None
        properties = title_arr[0].get("properties", {})
        text_expr = properties.get("text", {}).get("expr", {})
        value = text_expr.get("Literal", {}).get("Value")
        if value and isinstance(value, str):
            return value.strip("'")
    except Exception:
        pass
    return None

def extract_visual_properties(visual):
    vis_id = visual.get("id")
    x = visual.get("x")
    y = visual.get("y")
    width = visual.get("width")
    height = visual.get("height")
    config = visual.get("config")
    visual_type = ""
    visual_name = ""
    visual_nomeliteral = None
    if config:
        visual_nomeliteral = extract_visual_nomeliteral_from_config(config)
        try:
            config_json = json.loads(config) if isinstance(config, str) else config
        except Exception:
            config_json = {}
        if "singleVisual" in config_json:
            visual_type = config_json["singleVisual"].get("visualType", "")
            visual_name = config_json.get("name", "")
        elif "singleVisualGroup" in config_json:
            visual_type = "group"
            visual_name = config_json.get("name", "")
    return {
        "id": vis_id,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "visual_type": visual_type,
        "visual_name": visual_name,
        "config": config,
        "visual_nomeliteral": visual_nomeliteral,
    }
    
def extract_column_displaynames_and_measures(config):
    """
    Recebe o config (JSON ou str).
    Retorna uma lista de tuplas (displayName, nome_da_medida) para as colunas que têm displayName.
    """
    try:
        config_json = json.loads(config) if isinstance(config, str) else config
        single_visual = config_json.get("singleVisual", {})
        col_props = single_visual.get("columnProperties", {})
        result = []
        for col, props in col_props.items():
            display_name = props.get('displayName')
            if not display_name:
                continue
            # nome da medida = parte depois do primeiro ponto
            parts = col.split('.', 1)
            if len(parts) == 2:
                measure_name = parts[1]
            else:
                measure_name = col
            result.append((display_name, measure_name))
        return result
    except Exception:
        return []