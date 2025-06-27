import re

def extract_all_table_names(tables):
    """
    Retorna um set com os nomes de todas as tabelas do modelo.
    """
    return set(table.get("name", "") for table in tables if "name" in table)

def extract_all_measure_names(tables):
    """
    Retorna um set com os nomes de todas as medidas do modelo.
    """
    measures = set()
    for table in tables:
        for measure in table.get("measures", []):
            if "name" in measure:
                measures.add(measure["name"])
    return measures

def extract_measures_and_tables_dax(dax, all_measures, all_tables):
    # Remove comentários multi-linha /* ... */
    dax = re.sub(r"/\*[\s\S]*?\*/", "", dax)
    # Remove tags <...>
    dax = re.sub(r"<[^>]*>", "", dax)
    measures_set = set()
    tables_set = set()

    # Tabelas: 'Tabela Com Espaço'[Coluna]
    for match in re.finditer(r"'([^']+)'\s*\[", dax):
        tables_set.add(match.group(1))

    # Todos os [entre colchetes]
    for match in re.finditer(r"\[([^\[\]]+)\]", dax):
        nome_no_colchete = match.group(1)
        # verifica se é medida (não é precedido por Tabela[)
        before = dax[:match.start()]
        tabela_match = re.search(r"(\b[\w\s]+)\s*$", before)
        is_table = tabela_match and tabela_match.group(1).strip() in all_tables
        if not is_table and nome_no_colchete in all_measures:
            measures_set.add(nome_no_colchete)
    return sorted(measures_set), sorted(tables_set)

def build_measures_reverse_map(tables, all_measures, all_tables, extract_func):
    # Mapeia cada medida para as medidas que a referenciam
    references = {}
    for table in tables:
        for measure in table.get("measures", []):
            measure_name = measure.get("name")
            if not measure_name:
                continue
            expr = measure.get("expression", "")
            if isinstance(expr, list):
                expr = "\n".join(str(x) for x in expr)
            elif not isinstance(expr, str):
                expr = str(expr)
            medidas_referenciadas, _ = extract_func(expr, all_measures, all_tables)
            for ref in medidas_referenciadas:
                references.setdefault(ref, []).append(measure_name)
    return references

def build_measures_using_table_map(tables, all_measures, all_tables, extract_func):
    # Mapeia cada tabela para as medidas que a utilizam
    table_to_measures = {}
    for table in tables:
        for measure in table.get("measures", []):
            measure_name = measure.get("name")
            if not measure_name:
                continue
            expr = measure.get("expression", "")
            if isinstance(expr, list):
                expr = "\n".join(str(x) for x in expr)
            elif not isinstance(expr, str):
                expr = str(expr)
            _, tabelas_utilizadas = extract_func(expr, all_measures, all_tables)
            for tab in tabelas_utilizadas:
                table_to_measures.setdefault(tab, []).append(measure_name)
    return table_to_measures