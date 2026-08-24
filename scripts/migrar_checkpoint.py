import sqlite3
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
from core import config

con = sqlite3.connect(config.ARQUIVO_DB)
cur = con.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS meta_verificacao (
    chave TEXT PRIMARY KEY,
    valor TEXT
)
""")
cur.execute(
    "INSERT OR IGNORE INTO meta_verificacao (chave, valor) VALUES ('ultimo_id', '0')"
)
con.commit()
con.close()
print("meta_verificacao OK")