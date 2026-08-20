# ============================================================
#  Conhecimento local (SQLite) + similaridade
# ============================================================
import random
import difflib
import os
import sqlite3

from core import config
from core.interpretacao import (
    palavras_conteudo,
    set_vocabulario,
    normalizar,
)

BASE = {}
_ultima_chave_match = None


def carregar_base():
    global BASE
    base = {}
    caminho = config.ARQUIVO_DB

    if not os.path.exists(caminho):
        print("ERRO: conhecimento.db não encontrado em:")
        print(" ", caminho)
        print("Rode: python scripts/criar_banco.py && python scripts/importar_info.py")
        BASE = base
        return base

    conexao = sqlite3.connect(caminho)
    cursor = conexao.cursor()
    cursor.execute(
        """
        SELECT pergunta, resposta, vezes_usada
        FROM conhecimento
        ORDER BY vezes_usada DESC
        """
    )
    for pergunta, resposta, _vezes in cursor.fetchall():
        if pergunta not in base:
            base[pergunta] = []
        base[pergunta].append(resposta)
    conexao.close()

    vocab = set()
    for pergunta in base.keys():
        for palavra in pergunta.split():
            if len(palavra) >= 2:
                vocab.add(palavra)
    set_vocabulario(vocab)

    BASE = base
    print(f"[Sexta-feira] Base SQLite: {len(base)} perguntas")
    return base


def jaccard(texto1, texto2):
    p1 = palavras_conteudo(texto1)
    p2 = palavras_conteudo(texto2)
    if not p1 or not p2:
        return 0.0
    return len(p1 & p2) / len(p1 | p2)


def similaridade_letras(texto1, texto2):
    c1 = " ".join(sorted(palavras_conteudo(texto1)))
    c2 = " ".join(sorted(palavras_conteudo(texto2)))
    if not c1 or not c2:
        return 0.0
    return difflib.SequenceMatcher(None, c1, c2).ratio()


def escolher_resposta(respostas):
    if not respostas:
        return None
    if len(respostas) == 1 or random.random() < 0.70:
        return respostas[0]
    return random.choice(respostas)


def registrar_uso(pergunta, resposta):
    if not pergunta or not resposta:
        return
    try:
        conexao = sqlite3.connect(config.ARQUIVO_DB)
        cursor = conexao.cursor()
        cursor.execute(
            """
            UPDATE conhecimento
            SET vezes_usada = vezes_usada + 1
            WHERE pergunta = ? AND resposta = ?
            """,
            (pergunta, resposta),
        )
        conexao.commit()
        conexao.close()
    except Exception:
        pass


def salva_sugestao(pergunta, resposta):
    global BASE
    pergunta = normalizar(pergunta)
    resposta = resposta.strip()
    if pergunta not in BASE:
        BASE[pergunta] = []
    BASE[pergunta].append(resposta)

    conexao = sqlite3.connect(config.ARQUIVO_DB)
    cursor = conexao.cursor()
    cursor.execute(
        """
        INSERT INTO conhecimento (pergunta, resposta, vezes_usada)
        VALUES (?, ?, 0)
        """,
        (pergunta, resposta),
    )
    conexao.commit()
    conexao.close()


def busca_por_similaridade(texto):
    global _ultima_chave_match
    melhor_j = 0.0
    melhor_l = 0.0
    pergunta_j = pergunta_l = None
    resp_j = resp_l = None

    for pergunta_base, respostas in BASE.items():
        score_j = jaccard(texto, pergunta_base)
        score_l = similaridade_letras(texto, pergunta_base)
        if score_j > melhor_j:
            melhor_j = score_j
            pergunta_j = pergunta_base
            resp_j = escolher_resposta(respostas)
        if score_l > melhor_l:
            melhor_l = score_l
            pergunta_l = pergunta_base
            resp_l = escolher_resposta(respostas)

    if melhor_j >= config.LIMIAR_JACCARD and resp_j is not None:
        _ultima_chave_match = pergunta_j
        registrar_uso(pergunta_j, resp_j)
        return resp_j

    if melhor_l >= config.LIMIAR_DIGITACAO and resp_l is not None:
        if palavras_conteudo(texto) & palavras_conteudo(pergunta_l):
            inter = palavras_conteudo(texto) & palavras_conteudo(pergunta_l)
            if len(inter) >= 2 or melhor_l >= 0.85:
                _ultima_chave_match = pergunta_l
                registrar_uso(pergunta_l, resp_l)
                return resp_l
    return None


def match_exato(pergunta):
    global _ultima_chave_match
    if pergunta in BASE:
        resposta = escolher_resposta(BASE[pergunta])
        registrar_uso(pergunta, resposta)
        _ultima_chave_match = pergunta
        return resposta
    return None


def get_ultima_chave():
    return _ultima_chave_match
