# ============================================================
#  Interpretação: normalizar, digitação, contexto
# ============================================================
import re
import unicodedata
import difflib

from core import config

STOPWORDS = {
    "o", "a", "os", "as", "um", "uma", "de", "do", "da", "dos", "das",
    "e", "ou", "que", "em", "no", "na", "nos", "nas", "para", "por",
    "com", "sem", "como", "qual", "quais", "quem", "onde", "quando",
    "quanto", "quantos", "quantas", "porque", "porquê",
    "meu", "minha", "seu", "sua",
    "me", "te", "se", "eu", "voce", "ele", "ela", "isso", "isto",
    "sobre", "fale", "explica", "dizer", "diz", "ai", "eh",
}

PALAVRAS_PROTEGIDAS = {
    "dos", "das", "do", "da", "de", "em", "no", "na", "nos", "nas",
    "um", "uma", "uns", "umas", "ao", "aos", "pelo", "pela", "pelos", "pelas",
    "eu", "tu", "ele", "ela", "nos", "vos", "eles", "elas",
    "meu", "minha", "teu", "tua", "seu", "sua",
    "mais", "menos", "muito", "pouco", "bem", "mal",
    "presidente", "brasil", "eua", "estados", "unidos",
}

historico_conversa = []
ultimo_tema = None
_ultima_chave_match = None

# Vocabulário injetado por conhecimento após carregar a base
_vocabulario_base = set()


def set_vocabulario(vocab):
    global _vocabulario_base
    _vocabulario_base = set(vocab) if vocab else set()


def remover_acentos(texto):
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )


def normalizar(texto):
    texto = texto.lower().strip()
    texto = remover_acentos(texto)
    texto = re.sub(r"[^\w\s]", "", texto)

    juntadas = {
        "oque": "o que", "oq": "o que", "pq": "por que", "pque": "por que",
        "pd": "pode", "vc": "voce", "vcs": "voces", "tb": "tambem", "tbm": "tambem",
        "blz": "beleza", "msg": "mensagem", "qdo": "quando", "qnto": "quanto",
        "qnt": "quanto", "n": "nao", "ñ": "nao", "eh": "e", "tah": "ta",
        "to": "estou", "tou": "estou", "tmj": "tamo junto", "vlw": "valeu",
        "flw": "falou", "kd": "cade", "cmg": "comigo", "ctg": "contigo",
        "dnv": "de novo", "pf": "por favor", "pfv": "por favor", "q": "que", "ke": "que",
    }
    palavras = texto.split()
    return " ".join(juntadas.get(p, p) for p in palavras)


def corrigir_palavra(palavra, vocabulario):
    if palavra in vocabulario or palavra in PALAVRAS_PROTEGIDAS or len(palavra) < 3:
        return palavra
    candidatos = difflib.get_close_matches(palavra, vocabulario, n=3, cutoff=0.75)
    for cand in candidatos:
        if abs(len(cand) - len(palavra)) <= 1:
            return cand
    return palavra


def corrigir_digitacao(texto):
    return " ".join(corrigir_palavra(p, _vocabulario_base) for p in texto.split())


def interpretar(texto):
    return corrigir_digitacao(normalizar(texto))


def extrair_tema(texto):
    if not texto:
        return None
    palavras = [p for p in normalizar(texto).split() if p not in STOPWORDS and len(p) >= 1]
    return palavras[-1] if palavras else None


def atualizar_contexto(texto_usuario, chave_base, resposta):
    global historico_conversa, ultimo_tema
    tema = extrair_tema(chave_base) or extrair_tema(texto_usuario)
    if tema:
        ultimo_tema = tema
    historico_conversa.append({
        "usuario": texto_usuario,
        "maria": resposta,  # chave legada no histórico
        "sexta": resposta,
        "chave": chave_base,
        "tema": tema,
    })
    if len(historico_conversa) > config.MAX_HISTORICO:
        historico_conversa.pop(0)


def limpar_contexto():
    global historico_conversa, ultimo_tema, _ultima_chave_match
    historico_conversa = []
    ultimo_tema = None
    _ultima_chave_match = None


def tentar_expandir_contexto(pergunta_norm):
    if not pergunta_norm:
        return pergunta_norm
    if len(pergunta_norm.split()) >= 4 and not pergunta_norm.startswith("e "):
        return pergunta_norm

        # "e o presidente dos eua" / "e o presidente do brasil"
    m = re.match(
        r"^e (?:o|a) presidente (?:dos|do|da|de) (.+)$",
        pergunta_norm,
    )
    if m and m.group(1).strip():
        return f"quem e o presidente de {m.group(1).strip()}"

    # "e o dos eua" / "e o do brasil" (sem a palavra presidente, mas com dos/do/da)
    m = re.match(r"^e (?:o|a) (?:dos|do|da) (.+)$", pergunta_norm)
    if m and m.group(1).strip():
        return f"quem e o presidente de {m.group(1).strip()}"

    # "e o de c" / "e a de java" → o que e ...
    m = re.match(r"^e (?:o|a) de (.+)$", pergunta_norm)
    if m and m.group(1).strip():
        return f"o que e {m.group(1).strip()}"

    # "e o c" / "e a java"
    m = re.match(r"^e (?:o|a) (.+)$", pergunta_norm)
    if m and m.group(1).strip():
        resto = m.group(1).strip()
        # evita engolir "e o dos eua" de novo (já tratado)
        return f"o que e {resto}"

    m = re.match(r"^e (?:o|a) (?:de )?(.+)$", pergunta_norm)
    if m and m.group(1).strip():
        return f"o que e {m.group(1).strip()}"

    m = re.match(r"^e (?:sobre|do|da|de) (.+)$", pergunta_norm)
    if m and m.group(1).strip():
        return f"o que e {m.group(1).strip()}"

    m = re.match(r"^e (.+)$", pergunta_norm)
    if m and len(pergunta_norm.split()) <= 3:
        resto = m.group(1).strip()
        if resto and resto not in STOPWORDS:
            return f"o que e {resto}"

    if pergunta_norm in ("me fala mais", "fale mais", "e mais", "continua", "mais"):
        if ultimo_tema:
            return f"o que e {ultimo_tema}"

    return pergunta_norm


def preparar_pergunta(texto):
    pergunta = interpretar(texto)
    expandida = tentar_expandir_contexto(pergunta)
    if expandida != pergunta:
        pergunta = interpretar(expandida)
    return pergunta


def palavras_conteudo(texto):
    return set(p for p in texto.split() if p not in STOPWORDS and len(p) >= 1)
