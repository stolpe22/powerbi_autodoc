from .base_md_renderer import BaseMDRenderer
from ..utils import normalize_name

class RLSMDRenderer(BaseMDRenderer):
    def render(self, roles, nomeprojeto) -> str:
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
        output.append(f"---\n#{normalize_name(nomeprojeto).replace('.','_')} #datamodel")

        return "\n".join(output)