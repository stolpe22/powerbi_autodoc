import streamlit as st
import os
import tempfile
import zipfile
import json
from src.unzip_and_parse import process_all_zips

st.title("Gerador de Documentação Power BI")

# Seleção da pasta de saída
saida_dir = st.text_input("Informe a pasta de saída para os arquivos Markdown", value="autodoc")

# Upload de múltiplos zips
uploaded_files = st.file_uploader("Envie um ou mais arquivos ZIP do projeto", type="zip", accept_multiple_files=True)

# Botões
col1, col2 = st.columns(2)
with col1:
    analisar = st.button("Analisar previamente")
with col2:
    gerar = st.button("Gerar documentação")

def resumir_zip(zip_file, file_name):
    resumo = {}
    try:
        with zipfile.ZipFile(zip_file, "r") as zipf:
            for zinfo in zipf.infolist():
                if zinfo.filename.lower().endswith("datamodelschema"):
                    with zipf.open(zinfo) as file:
                        raw = file.read()
                        text = raw.decode("utf-16-le")
                        data = json.loads(text)
                        model = data.get("model", {})

                        resumo["nome_projeto"] = os.path.splitext(file_name)[0]
                        tables = model.get("tables", [])
                        resumo["tabelas"] = len(tables)
                        total_colunas = sum(len(t.get("columns", [])) for t in tables)
                        resumo["total_colunas"] = total_colunas
                        if tables:
                            max_cols = max(tables, key=lambda t: len(t.get("columns", [])))
                            resumo["maior_tabela"] = {
                                "nome": max_cols.get("name", ""),
                                "qtd_colunas": len(max_cols.get("columns", []))
                            }
                            resumo["media_colunas"] = round(total_colunas / len(tables), 1)
                        else:
                            resumo["maior_tabela"] = {"nome": "", "qtd_colunas": 0}
                            resumo["media_colunas"] = 0

                        resumo["medidas"] = sum(len(t.get("measures", [])) for t in tables)
                        measures = [m for t in tables for m in t.get("measures", [])]
                        resumo["medidas_longas"] = sum(1 for m in measures if isinstance(m.get("expression", ""), str) and len(m.get("expression", "")) > 300)
                        resumo["medidas_complexas"] = sum(
                            1
                            for m in measures
                            if isinstance(m.get("expression", ""), str)
                            and any(fn in m.get("expression", "").upper() for fn in ["CALCULATE", "FILTER", "SUMMARIZE", "VAR "])
                        )
                        dax_expressions = [m.get("expression", "") for m in measures if isinstance(m.get("expression", ""), str)]
                        resumo["medidas_duplicadas"] = len(dax_expressions) - len(set(dax_expressions))

                        resumo["colunas_calculadas"] = sum(1 for t in tables for c in t.get("columns", []) if c.get("type", "").lower() == "calculated")
                        resumo["tabelas_calculadas"] = sum(1 for t in tables if t.get("isCalculated", False))
                        hierarquias = [h for t in tables for h in t.get("hierarchies", [])] if tables else []
                        resumo["hierarquias"] = len(hierarquias)
                        resumo["lista_hierarquias"] = [{"tabela": t.get("name"), "nome": h.get("name"), "niveis": [l.get("name") for l in h.get("levels", [])]} for t in tables for h in t.get("hierarchies", [])]
                        perspectivas = model.get("perspectives", [])
                        resumo["perspectivas"] = len(perspectivas)
                        relationships = model.get("relationships", [])
                        resumo["relacionamentos"] = len(relationships)
                        resumo["relacionamentos_ativos"] = sum(1 for r in relationships if r.get("isActive", True))
                        resumo["relacionamentos_inativos"] = sum(1 for r in relationships if not r.get("isActive", True))
                        resumo["relacionamentos_tipo"] = {
                            "OneToMany": sum(1 for r in relationships if r.get("cardinality") == "OneToMany"),
                            "ManyToOne": sum(1 for r in relationships if r.get("cardinality") == "ManyToOne"),
                            "ManyToMany": sum(1 for r in relationships if r.get("cardinality") == "ManyToMany"),
                        }
                        # Corrigido: só tipos hashable em sets!
                        tabelas_com_rel = set(
                            str(t) for t in [r.get("fromTable") for r in relationships] + [r.get("toTable") for r in relationships]
                            if isinstance(t, (str, int, float))
                        )
                        nomes_tabelas = set(
                            str(t.get("name")) for t in tables if isinstance(t.get("name"), (str, int, float))
                        )
                        resumo["tabelas_desconectadas"] = sorted(list(nomes_tabelas - tabelas_com_rel))
                        resumo["tabelas_datas"] = [t.get("name") for t in tables if t.get("isDateTable", False)]
                        descricoes = 0
                        for t in tables:
                            if t.get("description"): descricoes += 1
                            descricoes += sum(1 for c in t.get("columns", []) if c.get("description"))
                            descricoes += sum(1 for m in t.get("measures", []) if m.get("description"))
                        resumo["objetos_com_descricao"] = descricoes
                        resumo["tabelas_ocultas"] = sum(1 for t in tables if t.get("isHidden", False))
                        roles = model.get("roles", [])
                        resumo["roles"] = len(roles)
                        resumo["nomes_roles"] = [r.get("name") for r in roles]
                        resumo["filtros_rls"] = sum(len(r.get("tablePermissions", [])) for r in roles)
                        resumo["kpis"] = sum(1 for m in measures if m.get("kpi"))
                        queries = data.get("queries", [])
                        resumo["parametros"] = sum(1 for q in queries if q.get("kind") == "Parameter")
                        resumo["queries_m"] = len(queries)
                    break
    except Exception as e:
        resumo["erro"] = str(e)
    return resumo

def gerar_resumo_md(resumo):
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

def salvar_resumo_md(resumo, saida_dir):
    nome_proj = resumo.get("nome_projeto", "projeto")
    pasta_proj = os.path.join(saida_dir, nome_proj)
    os.makedirs(pasta_proj, exist_ok=True)
    caminho_md = os.path.join(pasta_proj, "Resumo.md")
    with open(caminho_md, "w", encoding="utf-8") as f:
        f.write(gerar_resumo_md(resumo))
    return caminho_md

if uploaded_files:
    if analisar:
        st.subheader("Resumo dos arquivos ZIP enviados:")
        for uploaded_file in uploaded_files:
            # Salvar temporário só para abrir
            with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
                tmp.write(uploaded_file.getbuffer())
                tmp_path = tmp.name
            resumo = resumir_zip(tmp_path, uploaded_file.name)
            st.markdown(f"**Projeto:** {resumo.get('nome_projeto', 'Desconhecido')}")
            if "erro" in resumo:
                st.error(f"Erro ao processar: {resumo['erro']}")
            else:
                st.markdown(gerar_resumo_md(resumo))
            os.unlink(tmp_path)

    if gerar:
        if not saida_dir:
            st.error("Informe a pasta de saída antes de gerar a documentação.")
        else:
            os.makedirs(saida_dir, exist_ok=True)
            # Salvar todos os arquivos enviados na pasta temporária para processar
            with tempfile.TemporaryDirectory() as tempdir:
                for uploaded_file in uploaded_files:
                    temp_zip_path = os.path.join(tempdir, uploaded_file.name)
                    with open(temp_zip_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    # Gera o resumo para cada arquivo zip
                    resumo = resumir_zip(temp_zip_path, uploaded_file.name)
                    if "erro" not in resumo:
                        caminho_md = salvar_resumo_md(resumo, saida_dir)
                        st.info(f"Resumo salvo em: `{caminho_md}`")
                # Rodar o parser usando sua função já existente
                process_all_zips(tempdir, saida_dir)
            st.success(f"Documentação gerada em: `{saida_dir}`")