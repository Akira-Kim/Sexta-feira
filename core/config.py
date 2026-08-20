# ============================================================
#  Sexta-feira — configuração central (v01 modular)
# ============================================================
import os

# Nome de exibição
NOME_ASSISTENTE = "Sexta-feira"

# Pastas
_PASTA_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_DADOS = os.path.join(_PASTA_RAIZ, "dados")
PASTA_BASES = os.path.join(PASTA_DADOS, "bases")

# Banco: tenta dados/bases, senão raiz (compat v01)
_db_novo = os.path.join(PASTA_BASES, "conhecimento.db")
_db_raiz = os.path.join(_PASTA_RAIZ, "conhecimento.db")
ARQUIVO_DB = _db_novo if os.path.exists(_db_novo) else _db_raiz

ARQUIVO_INFO = os.path.join(_PASTA_RAIZ, "info.txt")
ARQUIVO_CHAVE = os.path.join(_PASTA_RAIZ, "api_key.txt")

# Busca
LIMIAR_JACCARD = 0.45
LIMIAR_DIGITACAO = 0.72

# Aprendizado / API
AUTO_APRENDER_IA = False  # conservador: não grava API sem confirmação (mudança v/s Maria)
API_RESPOSTAS = True      # interruptor: usar IA nas respostas
API_CONFERENCIA = True    # interruptor: usar IA na manutenção (futuro)

# Contexto
MAX_HISTORICO = 8
