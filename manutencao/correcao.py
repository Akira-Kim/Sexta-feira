# ============================================================
#  Correção de entradas flagadas — P2.4
# ============================================================
import sqlite3
import re

from core import config
from core import cascata_api
from core.interpretacao import normalizar, remover_acentos
from manutencao import flags_base

# Reusa a ideia da lista de evitar (se existir no chat)
try:
    import chat as pc
    PALAVRAS_SENSIVEIS = list(getattr(pc, "PALAVRAS_PROIBIDAS", []))
except Exception:
    PALAVRAS_SENSIVEIS = []


def _con():
    return sqlite3.connect(config.ARQUIVO_DB)


def _eh_sensivel(texto):
    if not texto:
        return False
    t = normalizar(texto)
    for palavra in PALAVRAS_SENSIVEIS:
        p = remover_acentos(str(palavra).lower())
        if not p or len(p) < 3:
            continue
        if re.search(rf"\b{re.escape(p)}\b", t):
            return True
    return False


def _listar_para_corrigir(prioridade="red", limite=3):
    """
    prioridade: 'red' | 'yellow' | 'ambos'
    """
    con = _con()
    cur = con.cursor()
    if prioridade == "red":
        cur.execute(
            """
            SELECT id, pergunta, resposta, tipo, flag
            FROM conhecimento
            WHERE flag = 'red'
            ORDER BY id ASC
            LIMIT ?
            """,
            (limite,),
        )
    elif prioridade == "yellow":
        cur.execute(
            """
            SELECT id, pergunta, resposta, tipo, flag
            FROM conhecimento
            WHERE flag = 'yellow'
            ORDER BY id ASC
            LIMIT ?
            """,
            (limite,),
        )
    else:
        cur.execute(
            """
            SELECT id, pergunta, resposta, tipo, flag
            FROM conhecimento
            WHERE flag IN ('red', 'yellow')
            ORDER BY CASE flag WHEN 'red' THEN 0 ELSE 1 END, id ASC
            LIMIT ?
            """,
            (limite,),
        )
    rows = cur.fetchall()
    con.close()
    return rows


def _prompt_correcao(pergunta, resposta_antiga, tipo):
    return (
        "Você corrige uma base de conhecimento em português do Brasil.\n"
        "Dada a PERGUNTA e a RESPOSTA_ANTIGA, escreva UMA resposta melhor, "
        "curta (2 a 4 frases), clara e factual quando for fato.\n"
        "Sem markdown, sem listas longas.\n"
        f"Tipo: {tipo or 'geral'}\n\n"
        f"PERGUNTA: {pergunta}\n"
        f"RESPOSTA_ANTIGA: {resposta_antiga}\n\n"
        "RESPOSTA_NOVA:"
    )


def _pedir_nova_resposta(pergunta, resposta_antiga, tipo):
    prompt = _prompt_correcao(pergunta, resposta_antiga, tipo)
    texto = None
    if hasattr(cascata_api, "_consultar_gemini"):
        texto = cascata_api._consultar_gemini(prompt, None)
        if not texto and hasattr(cascata_api, "_consultar_groq"):
            texto = cascata_api._consultar_groq(prompt, None)
    else:
        texto = cascata_api.consultar_ia(prompt, None)
    if not texto:
        return None
    # tira prefixo se a IA repetir o rótulo
    t = texto.strip()
    if t.lower().startswith("resposta_nova"):
        t = re.sub(r"(?i)^resposta_nova\s*:?\s*", "", t).strip()
    return t


def _aplicar_resposta(id_, nova_resposta):
    con = _con()
    cur = con.cursor()
    cur.execute(
        "UPDATE conhecimento SET resposta = ? WHERE id = ?",
        (nova_resposta, id_),
    )
    con.commit()
    con.close()
    # limpa alerta após correção
    flags_base.limpar_flag(id_)


def corrigir_lote(prioridade="red", limite=3, aplicar_automatico=True):
    """
    aplicar_automatico=True: grava no banco se não for sensível.
    Se sensível: só reporta, não grava.
    """
    if not config.API_CONFERENCIA:
        print("[correcao] API_CONFERENCIA=False — abortado.")
        return {"corrigidos": 0, "sensiveis": 0, "falhas": 0, "vazios": 0}

    itens = _listar_para_corrigir(prioridade, limite)
    if not itens:
        print("[correcao] Nenhum item com flag", prioridade)
        return {"corrigidos": 0, "sensiveis": 0, "falhas": 0, "vazios": 0}

    cont = {"corrigidos": 0, "sensiveis": 0, "falhas": 0, "vazios": 0}
    print(f"[correcao] {len(itens)} item(ns) (prioridade={prioridade})")

    for id_, pergunta, resposta, tipo, flag in itens:
        print(f"  → id={id_} [{flag}] {(pergunta or '')[:40]}")
        nova = _pedir_nova_resposta(pergunta, resposta or "", tipo)
        if not nova:
            print("    falha: API não respondeu")
            cont["falhas"] += 1
            continue

        if _eh_sensivel(nova) or _eh_sensivel(pergunta):
            print("    SENSÍVEL — não apliquei. Sugestão:")
            print("   ", nova[:200])
            cont["sensiveis"] += 1
            continue

        if aplicar_automatico:
            _aplicar_resposta(id_, nova)
            print("    corrigido e flag limpa")
            cont["corrigidos"] += 1
        else:
            print("    sugestão (não aplicada):", nova[:200])
            cont["vazios"] += 1

    print("[correcao] Resumo:", cont)
    print("[correcao] Flags:", flags_base.resumo_flags())
    return cont