# ============================================================
#  Rastreio de origem (mínimo v01 — expande no P1)
# ============================================================

def novo_rastreio(fonte, **kwargs):
    dados = {"fonte": fonte}
    dados.update(kwargs)
    return dados


def formatar(rastreio):
    if not rastreio:
        return ""
    fonte = rastreio.get("fonte", "?")
    extra = []
    if rastreio.get("chave"):
        extra.append(f"chave={rastreio['chave']}")
    if rastreio.get("score") is not None:
        extra.append(f"score={rastreio['score']}")
    if rastreio.get("modelo"):
        extra.append(f"modelo={rastreio['modelo']}")
    if extra:
        return f"[{fonte} | {', '.join(extra)}]"
    return f"[{fonte}]"
