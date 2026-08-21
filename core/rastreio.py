# ============================================================
#  Rastreio de origem — P1.3
# ============================================================

def novo(fonte, chave=None, score=None, modelo=None):
    """Cria um registro de origem da resposta."""
    return {
        "fonte": fonte,
        "chave": chave,
        "score": score,
        "modelo": modelo,
    }


def formatar(r):
    """Texto curto para debug no console."""
    if not r:
        return "[rastreio: vazio]"
    partes = [f"fonte={r.get('fonte')}"]
    if r.get("chave"):
        partes.append(f"chave={r['chave']}")
    if r.get("score") is not None:
        partes.append(f"score={r['score']:.2f}")
    if r.get("modelo"):
        partes.append(f"modelo={r['modelo']}")
    return "[rastreio] " + " | ".join(partes)


# Último rastreio da conversa (a GUI ainda não usa; o console pode mostrar)
ultimo = None


def registrar(r):
    """Guarda o último rastreio em memória."""
    global ultimo
    ultimo = r
    return r