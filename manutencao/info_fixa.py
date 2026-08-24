# ============================================================
#  Info fixa — flag estavel (P2.5)
# ============================================================
import sqlite3
from core import config
from core.interpretacao import normalizar
from manutencao import flags_base


def _con():
    return sqlite3.connect(config.ARQUIVO_DB)


def marcar_por_pergunta(pergunta, resposta=None):
    """Marca registro(s) como estavel."""
    p = normalizar(pergunta)
    return flags_base.set_flag_por_pergunta(p, "estavel", resposta)


def desmarcar_por_pergunta(pergunta, resposta=None):
    p = normalizar(pergunta)
    return flags_base.set_flag_por_pergunta(p, None, resposta)


def marcar_por_id(id_):
    return flags_base.set_flag(id_, "estavel")


def listar_fixas(limite=30):
    return flags_base.listar_por_flag("estavel", limite)


def processar_comando_info_fixa(texto, ultima_chave=None):
    """
    Comandos de texto. ultima_chave = última pergunta da base usada
    na conversa (rastreio), se houver.
    Devolve mensagem ou None.
    """
    p = normalizar(texto)

    if p in ("info fixa", "marcar fixa", "fixa", "isso e fixo", "e fixo"):
        if not ultima_chave:
            return (
                "Não sei qual informação marcar. "
                "Pergunte algo que eu responda da base e depois diga \"info fixa\"."
            )
        n = marcar_por_pergunta(ultima_chave)
        if n:
            return f"Marquei como info fixa: \"{ultima_chave}\"."
        return "Não encontrei essa pergunta no banco para marcar."

    if p in ("nao e fixa", "desmarcar fixa", "remover fixa", "nao fixa"):
        if not ultima_chave:
            return "Não sei qual desmarcar. Use depois de uma resposta da base."
        n = desmarcar_por_pergunta(ultima_chave)
        if n:
            return f"Removi info fixa de: \"{ultima_chave}\"."
        return "Não encontrei essa entrada."

    if p in ("listar fixas", "infos fixas", "o que e fixo"):
        rows = listar_fixas(15)
        if not rows:
            return "Nenhuma info fixa no momento."
        linhas = [f"- {r[1]}" for r in rows]
        return "Infos fixas:\n" + "\n".join(linhas)

    return None