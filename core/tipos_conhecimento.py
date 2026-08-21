# ============================================================
#  Tipos de conhecimento — P2.1
# ============================================================
from core.interpretacao import normalizar

TIPOS_VALIDOS = ("social", "fato", "procedimento", "opiniao", "geral")


def inferir_tipo(pergunta, resposta=""):
    """
    Heurística barata. Depois você pode corrigir à mão / por verificação.
    """
    p = normalizar(pergunta or "")
    r = normalizar(resposta or "")

    # Social / cumprimento
    sociais = (
        "oi", "ola", "ola", "bom dia", "boa tarde", "boa noite",
        "tchau", "obrigado", "valeu", "tudo bem", "como vai",
        "quem e voce", "qual seu nome",
    )
    if p in sociais or p.startswith("bom dia") or p.startswith("boa tarde"):
        return "social"

    # Procedimento (como fazer)
    if p.startswith("como ") or p.startswith("como fazer") or "passo a passo" in p:
        return "procedimento"

    # Opinião
    if p.startswith("qual melhor") or p.startswith("o que voce acha") or "voce gosta" in p:
        return "opiniao"

    # Fato (o que é / quem / quando / capital…)
    if (
        p.startswith("o que e ")
        or p.startswith("quem e ")
        or p.startswith("quando ")
        or p.startswith("qual a capital")
        or p.startswith("quantos ")
    ):
        return "fato"

    return "geral"


def normalizar_tipo(tipo):
    t = (tipo or "geral").strip().lower()
    return t if t in TIPOS_VALIDOS else "geral"