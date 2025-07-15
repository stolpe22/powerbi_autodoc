from .base_md_renderer import BaseMDRenderer

class ResumoMDRenderer(BaseMDRenderer):
    def render(self, resumo: dict) -> str:
        tabelas_desconectadas = (
            ', '.join(f'`{nome}`' for nome in resumo['tabelas_desconectadas'])
            if resumo['tabelas_desconectadas'] else ''
        )
        nomes_roles = (
            ', '.join(f'`{nome}`' for nome in resumo['nomes_roles'])
            if resumo['roles'] else 'Nenhuma'
        )

        return f"""# Resumo do Projeto Power BI: {resumo.get('nome_projeto', 'Desconhecido')}

- **Tabelas:** {resumo['tabelas']}
- **Colunas:** {resumo['total_colunas']} (média: {resumo['media_colunas']}, máximo: {resumo['maior_tabela']['qtd_colunas']} em {resumo['maior_tabela']['nome']})
- **Medidas:** {resumo['medidas']} ({resumo['medidas_longas']} longas, {resumo['medidas_complexas']} complexas, {resumo['medidas_duplicadas']} duplicadas)
- **Colunas calculadas:** {resumo['colunas_calculadas']}
- **Tabelas calculadas:** {resumo['tabelas_calculadas']}
- **Hierarquias:** {resumo['hierarquias']}
- **Perspectivas:** {resumo['perspectivas']}
- **Relacionamentos:** {resumo['relacionamentos']} ({resumo['relacionamentos_ativos']} ativos, {resumo['relacionamentos_inativos']} inativos)
    - OneToMany: {resumo['relacionamentos_tipo']['OneToMany']}
    - ManyToOne: {resumo['relacionamentos_tipo']['ManyToOne']}
    - ManyToMany: {resumo['relacionamentos_tipo']['ManyToMany']}
- **Tabelas desconectadas:** {len(resumo['tabelas_desconectadas'])} {tabelas_desconectadas}
- **Tabelas de datas:** {', '.join(resumo['tabelas_datas']) if resumo['tabelas_datas'] else 'Nenhuma'}
- **Objetos com descrição:** {resumo['objetos_com_descricao']}
- **Tabelas ocultas:** {resumo['tabelas_ocultas']}
- **Roles (RLS):** {resumo['roles']} ({nomes_roles})
- **Filtros RLS:** {resumo['filtros_rls']}
- **KPIs:** {resumo['kpis']}
- **Parâmetros Power Query:** {resumo['parametros']}
- **Queries M:** {resumo['queries_m']}
"""