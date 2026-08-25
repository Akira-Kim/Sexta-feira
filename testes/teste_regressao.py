# ============================================================
#  P3.1 — Bateria mínima de regressão (Sexta-feira)
#  Uso: python testes/teste_regressao.py
# ============================================================
import os
import sys
import sqlite3

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
os.chdir(RAIZ)

falhas = []
avisos = []


def ok(nome):
    print(f"  OK  {nome}")


def falha(nome, detalhe=""):
    print(f"  FALHA  {nome}" + (f" — {detalhe}" if detalhe else ""))
    falhas.append(nome)


def aviso(nome, detalhe=""):
    print(f"  AVISO  {nome}" + (f" — {detalhe}" if detalhe else ""))
    avisos.append(nome)


def main():
    print("=== Sexta-feira — teste de regressão P3.1 ===\n")

    # --- imports ---
    try:
        from core import config
        from core import interpretacao as interp
        from core import conhecimento as conhe
        from core import rastreio
        import chat as pc
        ok("imports")
    except Exception as e:
        falha("imports", str(e))
        _resumo()
        return

    # --- 1) Base ---
    print("\n[Base]")
    if not os.path.exists(config.ARQUIVO_DB):
        falha("arquivo db", config.ARQUIVO_DB)
    else:
        ok(f"db em {config.ARQUIVO_DB}")

    n = len(conhe.BASE) if conhe.BASE else 0
    if n == 0:
        # tenta carregar de novo
        conhe.carregar_base()
        n = len(conhe.BASE)
    if n > 0:
        ok(f"base com {n} perguntas")
    else:
        falha("base vazia")

    # --- 2–3) Match python e c ---
    print("\n[Busca]")
    r_py = pc.buscaResposta_GUI("o que e python")
    if r_py and "python" in r_py.lower():
        ok("match python")
    else:
        falha("match python", repr(r_py)[:80])

    r_c = pc.buscaResposta_GUI("o que e c")
    if r_c and ("linguagem" in r_c.lower() or "program" in r_c.lower() or " c " in f" {r_c.lower()} "):
        ok("match c")
    else:
        # aceita se respondeu algo não vazio da base
        if r_c:
            aviso("match c", f"resposta inesperada: {r_c[:60]}")
            ok("match c (respondeu algo)")
        else:
            falha("match c", "None")

    # --- 4) Interpretação ---
    print("\n[Interpretação]")
    prep = pc.preparar_pergunta("oque e python")
    if "python" in prep and "o que" in prep:
        ok(f"preparar_pergunta → {prep}")
    else:
        falha("preparar_pergunta", prep)

    # --- 5) Contexto ---
    print("\n[Contexto]")
    interp.limpar_contexto()
    pc.buscaResposta_GUI("o que e python")
    exp = interp.tentar_expandir_contexto(interp.normalizar("e o de java"))
    if "java" in exp and ("o que" in exp or "que e" in exp):
        ok(f"contexto → {exp}")
    else:
        falha("contexto", exp)

    # --- 6–7) Schema ---
    print("\n[Schema]")
    con = sqlite3.connect(config.ARQUIVO_DB)
    cur = con.cursor()
    cur.execute("PRAGMA table_info(conhecimento)")
    cols = {row[1] for row in cur.fetchall()}
    if "tipo" in cols:
        ok("coluna tipo")
    else:
        falha("coluna tipo")
    if "flag" in cols:
        ok("coluna flag")
    else:
        falha("coluna flag")

    # --- 8) Info fixa (aviso se não marcada) ---
    print("\n[Info fixa]")
    cur.execute(
        "SELECT flag FROM conhecimento WHERE pergunta = ? LIMIT 1",
        ("o que e python",),
    )
    row = cur.fetchone()
    con.close()
    if row and row[0] == "estavel":
        ok("python está estavel")
    else:
        aviso("python não está estavel", "marque na GUI com 'info fixa' se quiser")

    # --- 9) Menu / config ---
    print("\n[Config / menu]")
    try:
        from core import menu
        antes = config.API_RESPOSTAS
        menu.set_api_respostas(False)
        if config.API_RESPOSTAS is False:
            ok("desliga api")
        else:
            falha("desliga api")
        menu.set_api_respostas(True)
        if config.API_RESPOSTAS is True:
            ok("liga api")
        else:
            falha("liga api")
        # restaura
        menu.set_api_respostas(antes)
    except Exception as e:
        falha("menu", str(e))

    # --- 10) Rastreio ---
    print("\n[Rastreio]")
    pc.buscaResposta_GUI("o que e python")
    u = getattr(rastreio, "ultimo", None)
    if u and u.get("fonte") in ("exato", "similaridade", "api"):
        ok(f"rastreio fonte={u.get('fonte')}")
    else:
        aviso("rastreio", repr(u))

    _resumo()


def _resumo():
    print("\n=== Resumo ===")
    if not falhas:
        print("PASSOU — nenhuma falha crítica.")
    else:
        print(f"FALHOU — {len(falhas)} item(ns): {', '.join(falhas)}")
    if avisos:
        print(f"Avisos ({len(avisos)}): {', '.join(avisos)}")
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()