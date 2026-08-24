# ============================================================
#  Flags da base — P2.2
# ============================================================
import sqlite3
from core import config

FLAGS_VALIDAS = (None, "yellow", "red", "estavel")


def _con():
    return sqlite3.connect(config.ARQUIVO_DB)


def normalizar_flag(flag):
    if flag is None or flag == "" or flag == "neutro":
        return None
    f = str(flag).strip().lower()
    if f not in ("yellow", "red", "estavel"):
        return None
    return f


def set_flag(id_linha, flag):
    """Define a flag de um registro pelo id."""
    flag = normalizar_flag(flag)
    con = _con()
    cur = con.cursor()
    cur.execute("UPDATE conhecimento SET flag = ? WHERE id = ?", (flag, id_linha))
    con.commit()
    n = cur.rowcount
    con.close()
    return n > 0


def set_flag_por_pergunta(pergunta, flag, resposta=None):
    """Define flag por pergunta (e opcionalmente resposta)."""
    flag = normalizar_flag(flag)
    con = _con()
    cur = con.cursor()
    if resposta is not None:
        cur.execute(
            "UPDATE conhecimento SET flag = ? WHERE pergunta = ? AND resposta = ?",
            (flag, pergunta, resposta),
        )
    else:
        cur.execute(
            "UPDATE conhecimento SET flag = ? WHERE pergunta = ?",
            (flag, pergunta),
        )
    con.commit()
    n = cur.rowcount
    con.close()
    return n


def get_flag(id_linha):
    con = _con()
    cur = con.cursor()
    cur.execute("SELECT flag FROM conhecimento WHERE id = ?", (id_linha,))
    row = cur.fetchone()
    con.close()
    return row[0] if row else None


def listar_por_flag(flag, limite=50):
    """Lista registros com determinada flag (None = neutros)."""
    flag = normalizar_flag(flag) if flag is not None else None
    con = _con()
    cur = con.cursor()
    if flag is None:
        cur.execute(
            """
            SELECT id, pergunta, resposta, tipo, flag
            FROM conhecimento
            WHERE flag IS NULL
            LIMIT ?
            """,
            (limite,),
        )
    else:
        cur.execute(
            """
            SELECT id, pergunta, resposta, tipo, flag
            FROM conhecimento
            WHERE flag = ?
            LIMIT ?
            """,
            (flag, limite),
        )
    rows = cur.fetchall()
    con.close()
    return rows


def resumo_flags():
    con = _con()
    cur = con.cursor()
    cur.execute(
        """
        SELECT IFNULL(flag, 'neutro') AS f, COUNT(*)
        FROM conhecimento
        GROUP BY f
        """
    )
    dados = dict(cur.fetchall())
    con.close()
    return dados


def promover_alerta(id_linha):
    """
    Neutro → yellow
    yellow → red
    red → red (já no máximo)
    estavel → não mexe (info fixa)
    """
    atual = get_flag(id_linha)
    if atual == "estavel":
        return "estavel"
    if atual is None:
        set_flag(id_linha, "yellow")
        return "yellow"
    if atual == "yellow":
        set_flag(id_linha, "red")
        return "red"
    return atual or "red"


def limpar_flag(id_linha):
    """Verificação ok → tira alerta (não remove estavel de propósito: use set_flag)."""
    atual = get_flag(id_linha)
    if atual == "estavel":
        return "estavel"
    set_flag(id_linha, None)
    return None