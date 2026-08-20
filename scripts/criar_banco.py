import sqlite3
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
from core import config

os.makedirs(config.PASTA_BASES, exist_ok=True)
# grava em dados/bases e também na raiz para compat
for caminho in (config.ARQUIVO_DB, os.path.join(RAIZ, "conhecimento.db")):
    pasta = os.path.dirname(caminho)
    if pasta:
        os.makedirs(pasta, exist_ok=True)
    conexao = sqlite3.connect(caminho)
    cursor = conexao.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conhecimento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pergunta TEXT NOT NULL,
        resposta TEXT NOT NULL,
        vezes_usada INTEGER DEFAULT 0,
        criado_em TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_pergunta ON conhecimento (pergunta)"
    )
    conexao.commit()
    conexao.close()
    print("Banco OK:", caminho)
