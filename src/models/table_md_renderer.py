from .base_md_renderer import BaseMDRenderer
from .extractors import (extract_sql_from_m_expression, extract_m_steps)
from ..utils import normalize_name

class TabelaMDRenderer(BaseMDRenderer):
    def render(
        self,
        table,
        nomeprojeto,
        measures_using_table_map=None,
        relationships_by_table=None
    ) -> str:
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
                # Extrai as etapas Power Query
                steps = extract_m_steps(expr)
                if steps:
                    out.append("\n#### Etapas M extraídas do PowerQuery")
                    for step in steps:
                        out.append(f"- **{step['label']}**")
                        for param in step["params"]:
                            out.append(f"  - {param['name']}: {param['value']}")
                        out.append("")
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

        out.append(f"---\n#{normalize_name(nomeprojeto).replace('.','_')}")
        return "\n".join(out)