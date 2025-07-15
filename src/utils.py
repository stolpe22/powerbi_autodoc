import re

def normalize_name(name):
    """Normaliza nomes para arquivos: troca * por x e caracteres inválidos por _."""
    return re.sub(r'[<>:"/\\|?. ]', '_', name.replace("*", "x"))
