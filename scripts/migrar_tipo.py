import sqlite3
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
from core import config

con = sqlite3.connect(config.ARQUIVO_DB)
cur = con.cursor()

# Descobre se a coluna já existe
cur.execute("PRAGMA table_info(conhecimento)")
colunas = [c[1] for c in cur.fetchall()]

if "tipo" not in colunas:
    cur.execute(
        "ALTER TABLE conhecimento ADD COLUMN tipo TEXT DEFAULT 'geral'"
    )
    con.commit()
    print("Coluna 'tipo' adicionada.")
else:
    print("Coluna 'tipo' já existe.")

con.close()