from .base_md_renderer import BaseMDRenderer
from .extractors import extract_measures_and_tables_dax
from ..utils import normalize_name

class MedidaMDRenderer(BaseMDRenderer):
    def render(
        self,
        measure,
        nomeprojeto,
        tabela_nome,
        all_measures,
        all_tables,
        measures_reverse_map=None
    ) -> str:
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
        out.append(f"- #{normalize_name(nomeprojeto).replace('.','_')} #datamodel")
        return "\n".join(out)