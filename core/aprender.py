# ============================================================
#  Aprender — política de gravação no banco (P1.4)
# ============================================================
from core import config
from core import conhecimento as conhe
from core.interpretacao import normalizar

from core.interpretacao import normalizar

FRASES_NAO_SEI_USUARIO = (
    "nao sei",
    "sei la",
    "sei lá",
    "nao faco ideia",
    "nao faço ideia",
    "faco ideia",  # cuidado: melhor exigir "nao" antes
    "ignora",
    "deixa pra la",
    "deixa para la",
    "tanto faz",
    "passa",
    "skip",
    "nao grava",
    "nao salva",
)


def usuario_disse_nao_sei(texto):
    p = normalizar(texto)
    if not p:
        return True
    # frases curtas típicas
    if p in ("nao sei", "sei la", "ignora", "passa", "skip", "tanto faz"):
        return True
    if p.startswith("nao sei") or p.startswith("sei la"):
        return True
    if "nao faco ideia" in p or "nao faço ideia" in p:
        return True
    if p in ("nao grava", "nao salva", "deixa pra la", "deixa para la"):
        return True
    return False


def aprender_do_usuario(pergunta, resposta):
    """
    Usuário ensinou na hora.
    Sempre grava (é decisão explícita dele).
    """
    if not pergunta or not resposta or not str(resposta).strip():
        return False
    conhe.salva_sugestao(pergunta, resposta)
    return True


def aprender_da_api(pergunta, resposta):
    """
    Resposta veio da IA externa.
    Só grava se AUTO_APRENDER_IA estiver True no config.
    """
    if not config.AUTO_APRENDER_IA:
        return False
    if not pergunta or not resposta or not str(resposta).strip():
        return False
    conhe.salva_sugestao(pergunta, resposta)
    return True


def pode_aprender_da_api():
    """Consulta rápida para debug/menu futuro."""
    return bool(config.AUTO_APRENDER_IA)

def usuario_disse_nao_sei(texto):
    from core.interpretacao import normalizar
    p = normalizar(texto)
    if not p:
        return True
    if p in ("nao sei", "sei la", "ignora", "passa", "skip", "tanto faz"):
        return True
    if p.startswith("nao sei") or p.startswith("sei la"):
        return True
    if "nao faco ideia" in p or "nao grava" in p or "nao salva" in p:
        return True
    return False