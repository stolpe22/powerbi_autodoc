import re

def normalize_name(name):
    """Normaliza nomes para arquivos: troca * por x e caracteres inválidos por _."""
    return re.sub(r'[<>:"/\\|?. ]', '_', name.replace("*", "x"))

def split_params(params_str):
    # Remove espaços do início/fim
    params_str = params_str.strip()
    params = []
    current = ''
    level = 0
    in_string = False
    i = 0
    while i < len(params_str):
        c = params_str[i]
        if c in ('"', "'"):
            in_string = not in_string
            current += c
        elif not in_string and c in "([{":
            level += 1
            current += c
        elif not in_string and c in ")]}":
            level -= 1
            current += c
        elif not in_string and c == ',' and level == 0:
            params.append(current.strip())
            current = ''
        else:
            current += c
        i += 1
    if current:
        params.append(current.strip())
    return params