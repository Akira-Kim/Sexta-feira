import sqlite3
import os
import sys
import unicodedata
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
from core import config

def remover_acentos(texto):
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )

def normalizar(texto):
    texto = texto.lower().strip()
    texto = remover_acentos(texto)
    return re.sub(r"[^\w\s]", "", texto)

if not os.path.exists(config.ARQUIVO_INFO):
    print("ERRO: info.txt não encontrado")
    raise SystemExit(1)

# importa para o DB ativo
conexao = sqlite3.connect(config.ARQUIVO_DB)
cursor = conexao.cursor()
inseridos = ignorados = 0

with open(config.ARQUIVO_INFO, "r", encoding="utf-8") as arquivo:
    for linha in arquivo:
        linha = linha.strip()
        if ";" not in linha:
            continue
        pergunta_bruta, resposta = linha.split(";", 1)
        pergunta = normalizar(pergunta_bruta)
        resposta = resposta.strip()
        if not pergunta or not resposta:
            ignorados += 1
            continue
        cursor.execute(
            "SELECT id FROM conhecimento WHERE pergunta = ? AND resposta = ?",
            (pergunta, resposta),
        )
        if cursor.fetchone():
            ignorados += 1
            continue
        cursor.execute(
            "INSERT INTO conhecimento (pergunta, resposta) VALUES (?, ?)",
            (pergunta, resposta),
        )
        inseridos += 1

conexao.commit()
cursor.execute("SELECT COUNT(*) FROM conhecimento")
total = cursor.fetchone()[0]
conexao.close()
print("Importação concluída.")
print(f"  Inseridos : {inseridos}")
print(f"  Ignorados : {ignorados}")
print(f"  Total no banco: {total}")
