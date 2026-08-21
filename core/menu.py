# ============================================================
#  Menu lógico — interruptores (P1.6)
# ============================================================
from core import config
from core.interpretacao import normalizar


def status():
    return {
        "api_respostas": config.API_RESPOSTAS,
        "api_conferencia": config.API_CONFERENCIA,
        "auto_aprender_ia": config.AUTO_APRENDER_IA,
    }


def set_api_respostas(ligado: bool):
    config.API_RESPOSTAS = bool(ligado)
    return config.API_RESPOSTAS


def set_auto_aprender(ligado: bool):
    config.AUTO_APRENDER_IA = bool(ligado)
    return config.AUTO_APRENDER_IA


def processar_comando_menu(texto):
    """
    Comandos de texto. Devolve mensagem de confirmação ou None.
    """
    p = normalizar(texto)

    if p in ("desliga api", "desligar api", "api off", "sem api"):
        set_api_respostas(False)
        return "API de respostas desligada. Uso só a base local."

    if p in ("liga api", "ligar api", "api on", "com api"):
        set_api_respostas(True)
        return "API de respostas ligada (quando a base não souber)."

    if p in ("status", "status api", "como esta"):
        s = status()
        return (
            f"API respostas: {'on' if s['api_respostas'] else 'off'} | "
            f"Auto-aprender IA: {'on' if s['auto_aprender_ia'] else 'off'}"
        )

    if p in ("nao aprende com api", "desliga auto aprender"):
        set_auto_aprender(False)
        return "Não vou gravar respostas da API no banco."

    if p in ("aprende com api", "liga auto aprender"):
        set_auto_aprender(True)
        return "Vou gravar respostas da API no banco (use com cuidado)."

    return None