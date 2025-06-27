import re

def extract_all_table_names(tables):
    """Retorna um set com os nomes de todas as tabelas do modelo."""
    return {table.get("name", "") for table in tables if "name" in table}

def extract_all_measure_names(tables):
    """Retorna um set com os nomes de todas as medidas do modelo."""
    return {measure["name"] for table in tables for measure in table.get("measures", []) if "name" in measure}

def extract_measures_and_tables_dax(dax, all_measures, all_tables):
    """
    Extrai listas de medidas e tabelas referenciadas em uma expressão DAX.
    Não faz mais limpeza de comentários ou tags HTML, pois assume que a entrada já está filtrada.
    """
    import re
    measures_set = set()
    tables_set = set()

    # Tabelas do tipo: 'Tabela Com Espaço'[Coluna]
    for match in re.finditer(r"'([^']+)'\s*\[", dax):
        tables_set.add(match.group(1))

    # Medidas: [entre colchetes] não precedidos de Tabela[
    for match in re.finditer(r"\[([^\[\]]+)\]", dax):
        nome_no_colchete = match.group(1)
        before = dax[:match.start()]
        import re as _re
        tabela_match = _re.search(r"(\b[\w\s]+)\s*$", before)
        is_table = tabela_match and tabela_match.group(1).strip() in all_tables
        if not is_table and nome_no_colchete in all_measures:
            measures_set.add(nome_no_colchete)
    return sorted(measures_set), sorted(tables_set)

def build_measures_reverse_map(tables, all_measures, all_tables, extract_func):
    """Mapeia cada medida para as medidas que a referenciam"""
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
    """Mapeia cada tabela para as medidas que a utilizam"""
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

def extract_sql_from_m_expression(expr):
    import re
    if isinstance(expr, list):
        expr = "\n".join(expr)
    expr = expr.replace('#(lf)', '\n')
    oracle_params = [
        "CreateNavigationProperties",
        "NavigationPropertyNameGenerator",
        "Query",
        "CommandTimeout",
        "ConnectionTimeout",
        "HierarchicalNavigation"
    ]
    params_pattern = "|".join(re.escape(p) for p in oracle_params if p != "Query")
    pat = (
        r'Query\s*=\s*["\']'
        r'(.*?)'
        r'(?:'
            r'(?=,\s*(?:' + params_pattern + r')\s*=)'   # vírgula + parâmetro
            r'|(?=["\']\s*\]\))'                        # aspa + ])
        r')'
    )
    m = re.search(pat, expr, re.DOTALL)
    if m:
        return m.group(1).strip()
    return None