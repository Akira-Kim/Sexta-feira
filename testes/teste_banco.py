import os
import sys
import sqlite3

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
from core import config

conexao = sqlite3.connect(config.ARQUIVO_DB)
cursor = conexao.cursor()
cursor.execute("SELECT COUNT(*) FROM conhecimento")
print("Total de registros:", cursor.fetchone()[0])
cursor.execute(
    "SELECT pergunta, resposta FROM conhecimento WHERE pergunta LIKE '%python%' LIMIT 3"
)
print("Exemplos python:")
for p, r in cursor.fetchall():
    print("-", p, "->", r[:50])
cursor.execute("SELECT pergunta, resposta FROM conhecimento WHERE pergunta = 'o que e c'")
for p, r in cursor.fetchall():
    print("Match 'o que e c':", r)
conexao.close()
print("OK — banco legível.")
