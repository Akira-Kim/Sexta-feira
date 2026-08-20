# ============================================================
#  chat.py — fachada de compatibilidade (v01 modular → core/)
#  GUI e console importam este módulo como antes.
# ============================================================
import random
import re
import sys
import os

# Garante import do pacote core
_RAIZ = os.path.dirname(os.path.abspath(__file__))
if _RAIZ not in sys.path:
    sys.path.insert(0, _RAIZ)

from core import config
from core import interpretacao as interp
from core import conhecimento as conhe
from core import cascata_api
from core import rastreio

# Reexporta para InterfaceGrafica / console
NOME_ASSISTENTE = config.NOME_ASSISTENTE
PALAVRAS_PROIBIDAS = [
    "idiota", "burro", "otario", "otário", "babaca",
    "imbecil", "otaria", "otária", "palhaço", "palhaco",
    "trouxa", "retardado", "animal", "tapado",
    "merda", "bosta", "porra", "caralho",
    "cacete", "puta", "puta que pariu", "fdp",
    "filho da puta", "desgraçado", "desgracado",
    "arrombado", "arrombada", "cu", "cú",
    "vagabundo", "vagabunda", "lixo",
    "escroto", "escrota", "nojento", "nojenta",
    "gostosa", "gostoso", "delicia", "delícia",
    "manda nude", "nudes", "pelada", "pelado",
    "http://", "https://", "www.",
    ".com", ".net", ".xyz",
    "pix urgente", "ganhe dinheiro",
    "aposta", "cassino", "jogo do tigrinho",
    "cocaina", "cocaína", "maconha",
    "crack", "heroina", "heroína",
    "sexo", "porno", "pornografia",
    "hentai", "onlyfans",
]

normalizar = interp.normalizar
remover_acentos = interp.remover_acentos
interpretar = interp.interpretar
preparar_pergunta = interp.preparar_pergunta
limpar_contexto = interp.limpar_contexto
atualizar_contexto = interp.atualizar_contexto
historico_conversa = interp.historico_conversa  # ref dinâmica: usar interp.historico

salva_sugestao = conhe.salva_sugestao
registrar_uso = conhe.registrar_uso

# Carrega base na importação
conhe.carregar_base()
BASE = conhe.BASE


def saudacoes(nome):
    frases = [
        f"Bom dia! Meu nome é {nome}. Como vai você?",
        f"Olá! Eu sou {nome}.",
        f"Oi! Eu sou {nome}. Como posso ajudar?",
    ]
    print(random.choice(frases))


def saudacoes_GUI(nome):
    frases = [
        f"Bom dia! Meu nome é {nome}. Como vai você?",
        f"Olá! Eu sou {nome}.",
        f"Oi! Eu sou {nome}. Como posso ajudar?",
    ]
    return random.choice(frases)


def recebeTexto():
    texto = input("Você: ").strip()
    texto_normalizado = normalizar(texto)
    for palavra in PALAVRAS_PROIBIDAS:
        if re.search(
            rf"\b{re.escape(remover_acentos(palavra.lower()))}\b",
            texto_normalizado,
        ):
            print(f"{config.NOME_ASSISTENTE}: Desculpe, não posso responder esse tipo de mensagem.")
            return None
    return texto


def tentar_fallback_ia(texto_original, pergunta_preparada=None):
    if not config.API_RESPOSTAS:
        return None
    historico = interp.historico_conversa if interp.historico_conversa else None
    pergunta_para_ia = pergunta_preparada or texto_original
    resposta_ia = cascata_api.consultar_ia(pergunta_para_ia, historico)
    if not resposta_ia:
        return None
    chave_aprender = normalizar(pergunta_para_ia)
    if config.AUTO_APRENDER_IA:
        conhe.salva_sugestao(chave_aprender, resposta_ia)
    interp.atualizar_contexto(texto_original, chave_aprender, resposta_ia)
    return resposta_ia


def buscaResposta(texto):
    pergunta = preparar_pergunta(texto)

    if pergunta in ["tchau", "adeus", "ate logo"]:
        limpar_contexto()
        return "fim"

    # 1) Exato
    resposta = conhe.match_exato(pergunta)
    if resposta is not None:
        interp.atualizar_contexto(texto, pergunta, resposta)
        return resposta

    # 2) Similaridade
    resposta = conhe.busca_por_similaridade(pergunta)
    if resposta is not None:
        interp.atualizar_contexto(texto, conhe.get_ultima_chave(), resposta)
        return resposta

    # 3) API
    resposta = tentar_fallback_ia(texto, pergunta)
    if resposta is not None:
        return resposta

    # 4) Ensina
    print(f"{config.NOME_ASSISTENTE}: Não sei responder isso.")
    resposta = input("Qual deveria ser a resposta? ")
    conhe.salva_sugestao(texto, resposta)
    interp.atualizar_contexto(texto, normalizar(texto), resposta)
    return "Obrigado! Aprendi uma nova resposta."


def buscaResposta_GUI(texto):
    pergunta = preparar_pergunta(texto)

    resposta = conhe.match_exato(pergunta)
    if resposta is not None:
        interp.atualizar_contexto(texto, pergunta, resposta)
        return resposta

    resposta = conhe.busca_por_similaridade(pergunta)
    if resposta is not None:
        interp.atualizar_contexto(texto, conhe.get_ultima_chave(), resposta)
        return resposta

    return tentar_fallback_ia(texto, pergunta)


def exibeResposta(resposta, nome):
    if resposta == "fim":
        print(f"{nome}: Volte sempre!")
        return "fim"
    print(f"{nome}: {resposta}")
    return "continua"


def exibeResposta_GUI(resposta, nome):
    if resposta == "fim":
        return f"{nome}: Volte sempre!"
    return f"{nome}: {resposta}"
