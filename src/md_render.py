from .extractors import (extract_measures_and_tables_dax, extract_sql_from_m_expression)
from .utils import normalize_name

def render_medida_md(
    measure, nomeprojeto, tabela_nome, all_measures, all_tables, measures_reverse_map=None
):
    nome = measure.get("name", "Medida sem nome")
    expression = measure.get("expression", "")
    if isinstance(expression, list):
        expression = "\n".join(str(x) for x in expression)
    elif not isinstance(expression, str):
        expression = str(expression)

    medidas_referenciadas, tabelas_utilizadas = extract_measures_and_tables_dax(
        expression, all_measures, all_tables
    )
    used_by = []
    if measures_reverse_map is not None:
        used_by = measures_reverse_map.get(nome, [])

    # Determina o tipo da medida
    if not used_by:
        tipo = "medida fim"
    elif not medidas_referenciadas:
        tipo = "medida inicial"
    else:
        tipo = "medida meio"
    # Se for inicial e fim ao mesmo tempo, prevalece fim
    if not used_by and not medidas_referenciadas:
        tipo = "medida fim"

    out = []
    out.append("---")
    out.append(f"tipo medida: {tipo}")
    out.append("---")
    out.append(f"# {nome}")
    out.append("")
    out.append("```dax")
    out.append(expression)
    out.append("```")
    out.append("")
    out.append("**Medidas referenciadas:**")
    if medidas_referenciadas:
        for m in medidas_referenciadas:
            ref = f"- [[{nomeprojeto}/medidas/{normalize_name(m)}|{m}]]"
            out.append(ref)
    else:
        out.append("- Nenhuma")
    out.append("")
    out.append("**Medidas que utilizam esta medida:**")
    if used_by:
        for m in used_by:
            ref = f"- [[{nomeprojeto}/medidas/{normalize_name(m)}|{m}]]"
            out.append(ref)
    else:
        out.append("- Nenhuma")
    out.append("")
    out.append("**Tabelas utilizadas:**")
    if tabelas_utilizadas:
        for t in tabelas_utilizadas:
            out.append(f"- [[{nomeprojeto}/tabelas/{normalize_name(t)}|{t}]]")
    else:
        out.append("- Nenhuma")
    out.append("---")
    out.append(f"- #{normalize_name(nomeprojeto).replace(".","_")} #datamodel")
    return "\n".join(out)

#Renderizador Tabela
def render_tabela_md(table, nomeprojeto, measures_using_table_map=None, relationships_by_table=None):
    nome = table.get("name", "Tabela sem nome")
    out = []
    out.append(f"# {nome}")
    out.append("")
    
     # Relacionamentos
    if relationships_by_table:
        rels = relationships_by_table.get(nome, [])
        if rels:
            out.append("## Relacionamentos Power BI")
            for rel in rels:
                from_table = rel.get("fromTable", "")
                from_column = rel.get("fromColumn", "")
                from_cardinality = rel.get("fromCardinality", "")
                to_table = rel.get("toTable", "")
                to_column = rel.get("toColumn", "")
                to_cardinality = rel.get("toCardinality", "")
                # Formata o sentido do relacionamento
                if from_table == nome:
                    # Esta tabela é origem
                    out.append(f"- De: Esta tabela (**{from_table}**) [[#({from_column})]]\n")
                    out.append(f"- Para: [[{nomeprojeto}/tabelas/{normalize_name(to_table)}#({to_column})|{to_table}]] [{to_column}]\n")
                    if to_cardinality:
                        out.append(f"- Cardinalidade from {from_cardinality} to **{to_cardinality}**")
                elif to_table == nome:
                    # Esta tabela é destino
                    out.append(f"- De: [[{nomeprojeto}/tabelas/{normalize_name(from_table)}#({from_column})|{from_table}]] [{from_column}]\n")
                    out.append(f"- Para: Esta tabela (**{to_table}**) [[#({to_column})]]\n")
                    if to_cardinality:
                        out.append(f"- Cardinalidade from {from_cardinality} to **{to_cardinality}**")
                out.append("---")
            out.append("")
    
    # Medidas que utilizam
    out.append("**Medidas que utilizam esta tabela:**")
    used_by = []
    if measures_using_table_map is not None:
        used_by = measures_using_table_map.get(nome, [])
    if used_by:
        for m in used_by:
            ref = f"- [[{nomeprojeto}/medidas/{normalize_name(m)}|{m}]]"
            out.append(ref)
    else:
        out.append("- Nenhuma")
    out.append("")
    
    # Colunas
    out.append("## Colunas\n")
    for column in table.get("columns", []):
        col_nome = column.get("name", "Coluna sem nome")
        out.append(f"### {col_nome}\n")
        out.append("```powerquery")
        for k, v in column.items():
            out.append(f"{k}: {v}")
        out.append("```")
        out.append("")

    # Partitions
    partitions = table.get("partitions", [])
    for partition in partitions:
        out.append(f"## Partição")
        out.append("```powerquery")
        out.append(f"partition '{partition.get('name','')}' = m")
        out.append(f"\tmode: {partition.get('mode','')}")
        source = partition.get("source", {})
        expr = source.get("expression", "")
        if source.get("type") == "m":
            if isinstance(expr, list):
                expr = "\n".join(expr)
            out.append(f"\tsource =\n{expr}")
            out.append("")
            out.append("annotation PBI_ResultType = Table")
            out.append("```")
            # Extrai e exibe o SQL, se existir
            sql = extract_sql_from_m_expression(expr)
            if sql:
                out.append("\n#### SQL extraído do PowerQuery\n```sql")
                out.append(sql)
                out.append("```")
        else:
            # Para calculated, etc: apenas mostra a expressão e fecha bloco
            out.append(f"\tsource =\n{expr}")
            out.append("")
            out.append("annotation PBI_ResultType = Table")
            out.append("```")
        out.append("")

    # Annotations
    annotations = table.get("annotations", [])
    if annotations:
        out.append("### Annotations")
        out.append("```")
        for ann in annotations:
            out.append(f"{ann.get('name','')}: {ann.get('value','')}")
        out.append("```")
        out.append("")

    out.append(f"---\n#{normalize_name(nomeprojeto).replace(".","_")}")
    return "\n".join(out)

def render_rls_md(roles, nomeprojeto):
    output = []
    output.append("# Regras de RLS (Row-Level Security)\n")
    output.append("Este documento lista todas as roles (funções de segurança) e suas expressões de filtro de RLS definidas no modelo.\n")
    output.append("## Roles e Filtros\n")
    for role in roles:
        output.append(f"### Role: {role.get('name','')}")
        if role.get("modelPermission"):
            output.append(f"- **Model Permission:** {role['modelPermission']}")
        if role.get("tablePermissions"):
            output.append("\n#### Permissões por tabela:")
            for tp in role["tablePermissions"]:
                output.append(f"- **Tabela:** {tp.get('name','')}")
                output.append(f"- **Filtro:**")
                output.append("\t```dax")
                output.append(f"\t{tp.get('filterExpression','')}")
                output.append("\t```")
        if role.get("annotations"):
            output.append("\n#### Anotações:")
            for ann in role["annotations"]:
                output.append(f"- **{ann.get('name','')}:** {ann.get('value','')}")
        output.append("\n---\n")
    output.append(f"---\n#{normalize_name(nomeprojeto).replace(".","_")} #datamodel")

    return "\n".join(output)