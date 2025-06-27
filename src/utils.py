import re

def normalize_name(name):
    # Troca * por x
    name = name.replace("*", "x")
    # Substitui qualquer caractere inválido e espaço por _
    return re.sub(r'[<>:"/\\|? ]', '_', name)