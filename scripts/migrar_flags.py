import sqlite3
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
from core import config

con = sqlite3.connect(config.ARQUIVO_DB)
cur = con.cursor()
cur.execute("PRAGMA table_info(conhecimento)")
colunas = [c[1] for c in cur.fetchall()]

if "flag" not in colunas:
    cur.execute(
        "ALTER TABLE conhecimento ADD COLUMN flag TEXT DEFAULT NULL"
    )
    con.commit()
    print("Coluna 'flag' adicionada.")
else:
    print("Coluna 'flag' já existe.")

# contagem opcional
cur.execute(
    "SELECT IFNULL(flag, 'neutro') AS f, COUNT(*) FROM conhecimento GROUP BY f"
)
print("Flags atuais:")
for f, n in cur.fetchall():
    print(f"  {f}: {n}")

con.close()