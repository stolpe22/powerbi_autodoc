# POWERBI_AUTODOC

## Descrição

**POWERBI_AUTODOC** é uma solução automatizada para documentação de projetos Power BI, gerando arquivos Markdown (.md) detalhados sobre tabelas, medidas, relacionamentos, regras de RLS e resumo do modelo. O projeto processa arquivos ZIP exportados do Power BI, descompacta e interpreta o schema do modelo, extraindo informações relevantes para facilitar auditoria, governança e compartilhamento de conhecimento.

> **A documentação gerada é otimizada para navegação no [Obsidian](https://obsidian.md), aproveitando links internos e estrutura de arquivos para a criação de knowledge graphs.**  
> Links cruzados entre tabelas, medidas e RLS favorecem explorações contextuais e relacionamentos visuais no Obsidian.

## Principais Funcionalidades

- **Documentação automática** de tabelas, medidas, partições, colunas e relações.
- **Geração de Resumo do projeto** (tabelas, medidas, relacionamentos, hierarquias, roles de segurança, etc).
- **Extração e documentação de regras de RLS** (Row-Level Security).
- **Renderização em Markdown** com links cruzados entre medidas, tabelas e recursos do modelo, no padrão [[arquivo|exibição]].
- **Interface web interativa** via [Streamlit](https://streamlit.io/) para upload e geração dos arquivos.
- **Reconhecimento e documentação de funções M** utilizadas em Power Query.

## Estrutura do Projeto

- `src/configs/mquery_functions_structure.py`: Mapeamento das funções M relevantes para documentação de queries Power Query.
- `src/models/`: Lógica principal de extração, processamento e renderização de documentação:
  - `project_processor.py`: Orquestra todo fluxo de documentação, processando arquivos ZIP e salvando Markdown.
  - `resume_md_renderer.py`: Gera o resumo do projeto Power BI em Markdown.
  - `table_md_renderer.py`: Documenta tabelas, colunas, partições, Power Query, SQL extraído e relacionamentos.
  - `measure_md_renderer.py`: Documenta medidas DAX, dependências e uso cruzado.
  - `rls_md_renderer.py`: Documenta roles e expressões de filtro de RLS.
  - `extractors.py`: Funções utilitárias para extração de nomes, dependências, SQL e etapas M.
  - `base_md_renderer.py`: Classe base abstrata para renderizadores Markdown.
  - `utils.py`: Funções auxiliares para normalização de nomes e parsing de parâmetros.
- `src/dataviz/`: (Opcional) Processamento extra sobre visuais/layout do Power BI.
- `app.py`: Interface web para documentação interativa (Streamlit).
- `main.py`: Execução via linha de comando para processamento em lote.

## Como Usar

**Via linha de comando:**

1. Coloque os arquivos ZIP exportados do Power BI na pasta `projetos/`.
2. Execute:
   ```bash
   python main.py
   ```
3. A documentação será gerada na pasta `autodoc/`.

**Via interface web:**

1. Execute:
   ```bash
   streamlit run app.py
   ```
2. Envie seus arquivos ZIP, escolha a pasta de saída e gere a documentação diretamente pelo navegador.

## Requisitos

- Python 3.8+
- Bibliotecas necessárias listadas em `requirements.txt`

## Instalação de dependências

```bash
pip install -r requirements.txt
```

## Exemplos de Saída

- `autodoc/PROJETO/tabelas/NomeTabela.md`: Documentação detalhada da tabela, colunas, partições, Power Query, relacionamentos, annotations.
- `autodoc/PROJETO/medidas/NomeMedida.md`: Documentação da medida DAX, dependências, uso cruzado e tabelas referenciadas.
- `autodoc/PROJETO/RLS.md`: Resumo das regras de segurança (Row-Level Security) do modelo.
- `autodoc/PROJETO/Resumo.md`: Resumo estatístico do modelo (tabelas, medidas, relacionamentos, roles, etc).

**Navegação no Obsidian:**  
A estrutura e os links internos permitem explorar o modelo como um _knowledge graph_ — clicando para navegar entre tabelas, medidas e regras, aproveitando o mapeamento cruzado.

## Referências e Customização

- Adicione novas funções M relevantes em `mquery_functions_structure.py` conforme evolução dos modelos.
- Expanda as renderizações Markdown conforme necessidade de governança ou compliance.
- O projeto suporta extensões para análise de visuais e layouts via `dataviz`.

---

**POWERBI_AUTODOC**: Documentação automatizada de modelos Power BI para auditoria, governança e compartilhamento de conhecimento.