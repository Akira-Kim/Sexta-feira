import sqlite3
from core import config


def _con():
    return sqlite3.connect(config.ARQUIVO_DB)


def get_ultimo_id():
    con = _con()
    cur = con.cursor()
    cur.execute(
        "SELECT valor FROM meta_verificacao WHERE chave = 'ultimo_id'"
    )
    row = cur.fetchone()
    con.close()
    return int(row[0]) if row else 0


def set_ultimo_id(id_):
    con = _con()
    cur = con.cursor()
    cur.execute(
        """
        INSERT INTO meta_verificacao (chave, valor) VALUES ('ultimo_id', ?)
        ON CONFLICT(chave) DO UPDATE SET valor = excluded.valor
        """,
        (str(id_),),
    )
    con.commit()
    con.close()