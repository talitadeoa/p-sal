import re

def extrair_informacoes(url):
    # Expressões regulares para cada parte da URL
    padrao = r"https://www\.salario\.com\.br/profissao/([^/]+)/cbo-([0-9]+)/?(.*)"

    # Fazendo a correspondência da URL com o padrão
    match = re.match(padrao, url)
    
    if match:
        cargo = match.group(1).replace("-", " ")
        cbo = match.group(2)
        local_part = match.group(3)
        
        # Determinando o tipo de local
        if not local_part:
            local = ('país', 'br')
        elif len(local_part) == 2:
            local = ('estado', local_part)
        else:
            local = ('cidade', local_part.rstrip('/'))
        
        return cargo, cbo, local
    else:
        raise ValueError("URL não corresponde a nenhum dos padrões esperados.")

# Testando o script com exemplos
urls = [
    "https://www.salario.com.br/profissao/administrador-cbo-252105/",
    "https://www.salario.com.br/profissao/administrador-cbo-252105/pe/",
    "https://www.salario.com.br/profissao/administrador-cbo-252105/recife-pe/"
]

for url in urls:
    cargo, cbo, local = extrair_informacoes(url)
    print(f"Cargo: {cargo}, CBO: {cbo}, Local: {local}")
