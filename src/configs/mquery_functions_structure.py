# Lista de funções M relevantes para documentação
MQUERY_FUNCTIONS = [
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
            {"name": "Tabela", "pos": 0},
            {"name": "Renomeações", "pos": 1}
        ]
    },
    {
        "function": "Table.AddColumn",
        "label": "Adicionar Coluna",
        "params": [
            {"name": "Tabela", "pos": 0},
            {"name": "Nome Nova Coluna", "pos": 1},
            {"name": "Função", "pos": 2}
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
          {"name": "Etapa", "pos": 0}
      ]  
    },
    # Adicione outras funções conforme necessário!
]