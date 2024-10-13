import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from docx import Document
import time
from webdriver_manager.chrome import ChromeDriverManager

# Função para extrair elementos com base em critérios predefinidos
def extrair_elementos(url, tipo):
    # Opções do Chrome para execução em segundo plano
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executar em segundo plano
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        time.sleep(3)  # Espera para garantir que a página carregue (ajuste conforme necessário)
        html = driver.page_source
    finally:
        driver.quit()  # Fecha o navegador

    soup = BeautifulSoup(html, 'html.parser')
    resultados = {}

    # Tags e índices predefinidos para cada tipo
    if tipo == "salário":
        tags = {
            'p': [0, 1, 2, 7, ],  # Exemplo: extrai os três primeiros parágrafos para "salário"
            'h2': [1, 13],  
            'table': [3],
        }
    elif tipo == "dissídio":
        tags = {
            'p': [24, 26, 27, 28, 29],     # Exemplo: extrai o primeiro e o terceiro parágrafo para "dissídio"
            'h2': [10, 11]  # Extrai os três primeiros títulos h2
        }

    for tag, indices in tags.items():
        elementos = soup.find_all(tag)
        resultados[tag] = []
        for i in indices:
            if i < len(elementos):
                resultados[tag].append(elementos[i].get_text())
            else:
                print(f"Índice {i} fora do alcance para a tag <{tag}>.")

    return resultados

# Função para salvar os resultados em um arquivo .docx
def salvar_docx(resultados, arquivo):
    doc = Document()
    for tag, textos in resultados.items():
        doc.add_heading(f'Elementos <{tag}>', level=1)
        for texto in textos:
            doc.add_paragraph(texto)
    doc.save(arquivo)
    return arquivo

# Função chamada ao clicar no botão "Extrair"
def extrair():
    url = url_entry.get()  # Captura a URL digitada no campo
    cbo = cbo_entry.get()  # Captura o CBO digitado
    local = local_entry.get()  # Captura o local digitado
    tipo_selecionado = tipo_var.get()  # Captura o tipo selecionado

    if not cbo or not local:
        messagebox.showerror("Erro", "Por favor, insira o CBO e o Local.")
        return

    try:
        resultados = extrair_elementos(url, tipo_selecionado)
        if tipo_selecionado == "salario":
            arquivo = f'CBO {cbo} - {local} - Salário.docx'
        elif tipo_selecionado == "dissidio":
            arquivo = f'CBO {cbo} - {local} - Dissídio.docx'
        salvar_docx(resultados, arquivo)
        messagebox.showinfo("Sucesso", f'Dados coletados salvos em {arquivo}')
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Criação da janela principal
root = tk.Tk()
root.title("Automação - Pesquisa Salarial")
root.geometry("500x400")

# Variável para armazenar a opção selecionada pelo usuário
tipo_var = tk.StringVar(value="salário")  # Valor padrão

# Layout
tk.Label(root, text="Insira a URL:").grid(row=0, column=0, padx=10, pady=5)
url_entry = tk.Entry(root, width=50)  # Campo de entrada para a URL
url_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="CBO:").grid(row=1, column=0, padx=10, pady=5)
cbo_entry = tk.Entry(root, width=20)  # Campo de entrada para o CBO
cbo_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Local:").grid(row=2, column=0, padx=10, pady=5)
local_entry = tk.Entry(root, width=20)  # Campo de entrada para o Local
local_entry.grid(row=2, column=1, padx=10, pady=5)

# Opções de seleção para o tipo de extração
tk.Radiobutton(root, text="Salário", variable=tipo_var, value="salario").grid(row=3, column=0, padx=10, pady=5)
tk.Radiobutton(root, text="Dissídio", variable=tipo_var, value="dissidio").grid(row=3, column=1, padx=10, pady=5)

# Botão para iniciar a extração
extrair_button = tk.Button(root, text="Extrair", command=extrair)
extrair_button.grid(row=4, column=0, columnspan=2, pady=20)

root.mainloop()
