# Lista de funções M relevantes para documentação
MQUERY_FUNCTIONS = [
    {
        "function": "SharePoint.Files",
        "label": "Carregar arquivos do SharePoint",
        "params": [
            {"name": "URL do SharePoint", "pos": 0},
            {"name": "Opções", "pos": 1, "optional": True}
        ]
    },
    {
        "function": "Table.SelectRows",
        "label": "Selecionar Linhas",
        "params": [
            {"name": "Etapa", "pos": 0},
            {"name": "Condição", "pos": 1}
        ]
    },
    {
        "function": "Excel.Workbook",
        "label": "Importar do Excel",
        "params": [
            {"name": "Arquivo Excel", "pos": 0},
            {"name": "Opções", "pos": 1, "optional": True}
        ]
    },
    {
        "function": "Table.PromoteHeaders",
        "label": "Promover cabeçalhos",
        "params": [
            {"name": "Tabela", "pos": 0},
            {"name": "Opções", "pos": 1, "optional": True}
        ]
    },
    {
        "function": "Table.NestedJoin",
        "label": "Join",
        "params": [
            {"name": "Tabela Origem", "pos": 0},
            {"name": "Colunas Origem", "pos": 1},
            {"name": "Tabela Destino", "pos": 2},
            {"name": "Colunas Destino", "pos": 3},
            {"name": "Nome da Coluna Expandida", "pos": 4, "optional": True},
            {"name": "Tipo de Join", "pos": 5, "optional": True}
        ]
    },
    {
        "function": "Table.ExpandTableColumn",
        "label": "Expandir Coluna",
        "params": [
            {"name": "Tabela", "pos": 0},
            {"name": "Coluna Expandida", "pos": 1},
            {"name": "Colunas Originais", "pos": 2},
            {"name": "Novos Nomes", "pos": 3}
        ]
    },
    {
        "function": "Table.RenameColumns",
        "label": "Renomear Colunas",
        "params": [
            {"name": "Etapa", "pos": 0},
            {"name": "Renomeações", "pos": 1}
        ]
    },
    {
        "function": "Table.RemoveColumns",
        "label": "Remover Colunas",
        "params": [
            {"name": "Tabela", "pos": 0},
            {"name": "Colunas Removidas", "pos": 1}
        ]
    },
    {
        "function": "Table.TransformColumnTypes",
        "label": "Alterar Tipo de Coluna",
        "params": [
            {"name": "Tabela", "pos": 0},
            {"name": "Alterações", "pos": 1}
        ]
    },
    {
        "function": "Table.Distinct",
        "label": "Aplicar Distinct",
        "params": [
            {"name": "Registro", "pos": 0}
        ]
    },
    {
        "function": "Table.DuplicateColumn",
        "label": "Duplicar Coluna",
        "params": [
            {"name": "Etapa", "pos": 0},
            {"name": "Coluna Original", "pos": 1},
            {"name": "Coluna Duplicada", "pos": 2}
        ]
    },
    {
    "function": "Table.ReplaceValue",
    "label": "Substituir Valor",
    "params": [
        {"name": "Tabela", "pos": 0},
        {"name": "Valor a ser substituído", "pos": 1},
        {"name": "Novo valor", "pos": 2},
        {"name": "Função de substituição", "pos": 3},
        {"name": "Colunas para buscar", "pos": 4}
        ]
    },
    {
    "function": "Table.Sort",
    "label": "Ordenar Tabela",
    "params": [
        {"name": "Tabela", "pos": 0},
        {"name": "Critério de Ordenação", "pos": 1}
    ]
    },
    {
        "function": "Table.AddColumn",
        "label": "Adicionar Coluna",
        "params": [
            {"name": "Tabela", "pos": 0},
            {"name": "Nome Nova Coluna", "pos": 1},
            {"name": "Função Geradora da Coluna", "pos": 2},
            {"name": "Tipo da Coluna", "pos": 3, "optional": True}
        ]
    },
    {
        "function": "Table.RemoveColumns",
        "label": "Remover Colunas",
        "params": [
            {"name": "Tabela", "pos": 0},
            {"name": "Colunas Removidas", "pos": 1},
            {"name": "Campo ausente", "pos": 2, "optional": True}
        ]
    },
    {
        "function": "Table.ExpandRecordColumn",
        "label": "Expandir Coluna de Registro",
        "params": [
            {"name": "Tabela", "pos": 0},
            {"name": "Nome da Coluna", "pos": 1},
            {"name": "Lista de Campos", "pos": 2},
            {"name": "Novos Nomes das Colunas", "pos": 3, "optional": True}
        ]
    },
    {
        "function": "Table.ReorderColumns",
        "label": "Reordenar Colunas",
        "params": [
            {"name": "Tabela", "pos": 0},
            {"name": "Ordem das Colunas", "pos": 1},
            {"name": "Campo ausente", "pos": 2, "optional": True}
        ]
    }
     
    # Adicione outras funções conforme necessário!
]