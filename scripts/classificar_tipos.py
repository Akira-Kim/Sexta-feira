import sqlite3
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
from core import config
from core.tipos_conhecimento import inferir_tipo

con = sqlite3.connect(config.ARQUIVO_DB)
cur = con.cursor()
cur.execute("SELECT id, pergunta, resposta, tipo FROM conhecimento")
linhas = cur.fetchall()
atualizados = 0

for id_, pergunta, resposta, tipo in linhas:
    if tipo and tipo != "geral":
        continue
    novo = inferir_tipo(pergunta, resposta or "")
    if novo != "geral":
        cur.execute("UPDATE conhecimento SET tipo = ? WHERE id = ?", (novo, id_))
        atualizados += 1

con.commit()
cur.execute("SELECT tipo, COUNT(*) FROM conhecimento GROUP BY tipo")
print("Distribuição:")
for tipo, n in cur.fetchall():
    print(f"  {tipo}: {n}")
print("Atualizados agora:", atualizados)
con.close()