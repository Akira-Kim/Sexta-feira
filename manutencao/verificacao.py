# ============================================================
#  Verificação em lotes — P2.3
#  Só JULGA e marca flag. Não reescreve resposta (isso é 2.4).
# ============================================================
import sqlite3
import re

from core import config
from core import cascata_api
from manutencao import flags_base
from manutencao import checkpoint


def _con():
    return sqlite3.connect(config.ARQUIVO_DB)


def _proximo_lote(depois_de_id, tamanho):
    """Pega as próximas linhas após o checkpoint (ignora flag=estavel)."""
    con = _con()
    cur = con.cursor()
    cur.execute(
        """
        SELECT id, pergunta, resposta, tipo, flag
        FROM conhecimento
        WHERE id > ?
          AND (flag IS NULL OR flag != 'estavel')
        ORDER BY id ASC
        LIMIT ?
        """,
        (depois_de_id, tamanho),
    )
    rows = cur.fetchall()
    con.close()
    return rows


def _montar_prompt_verificacao(pergunta, resposta, tipo):
    return (
        "Você é um revisor de base de conhecimento em português do Brasil.\n"
        "Avalie se a RESPOSTA ainda é adequada para a PERGUNTA.\n"
        "Considere o tipo: "
        f"{tipo or 'geral'}.\n"
        "Responda em UMA linha, com exatamente um destes formatos:\n"
        "OK\n"
        "ALERTA: motivo curto\n"
        "Nao invente fatos longos. Se for saudação ou opinião leve, aceite OK.\n\n"
        f"PERGUNTA: {pergunta}\n"
        f"RESPOSTA: {resposta}\n"
    )


def _interpretar_veredito(texto):
    """
    Devolve: 'ok' | 'alerta'
    """
    if not texto:
        return "alerta"
    t = texto.strip().lower()
    if t.startswith("ok") or t == "ok" or re.match(r"^ok\b", t):
        return "ok"
    if "alerta" in t[:20]:
        return "alerta"
    # se a IA divagar, trata como alerta leve
    if "correta" in t or "adequada" in t or "sim" == t[:3]:
        return "ok"
    return "alerta"


def verificar_um(id_, pergunta, resposta, tipo, flag_atual):
    """
    Chama a API de conferência e atualiza flag.
    Retorna dict com resultado.
    """
    if not config.API_CONFERENCIA:
        return {
            "id": id_,
            "status": "pulado",
            "motivo": "API_CONFERENCIA=False",
        }

    if flag_atual == "estavel":
        return {"id": id_, "status": "pulado", "motivo": "estavel"}

    prompt = _montar_prompt_verificacao(pergunta, resposta, tipo)
    # Reusa a cascata (Gemini → Groq). É a mesma API; o interruptor
    # API_CONFERENCIA já foi checado acima.
    # Temporariamente precisamos que cascata responda mesmo se API_RESPOSTAS
    # estiver off — por isso chamamos as funções internas se existirem.
    texto = None
    try:
        # Preferir caminho que ignore API_RESPOSTAS só na conferência:
        if hasattr(cascata_api, "_consultar_gemini"):
            texto = cascata_api._consultar_gemini(prompt, None)
            if not texto and hasattr(cascata_api, "_consultar_groq"):
                texto = cascata_api._consultar_groq(prompt, None)
        else:
            # fallback: consultar_ia normal (exige API_RESPOSTAS=True)
            texto = cascata_api.consultar_ia(prompt, None)
    except Exception as e:
        return {"id": id_, "status": "erro", "motivo": str(e)}

    veredito = _interpretar_veredito(texto)
    if veredito == "ok":
        flags_base.limpar_flag(id_)
        return {"id": id_, "status": "ok", "bruto": (texto or "")[:80]}
    else:
        nova = flags_base.promover_alerta(id_)
        return {
            "id": id_,
            "status": "alerta",
            "flag": nova,
            "bruto": (texto or "")[:80],
        }


def rodar_lote(tamanho=5):
    """
    Verifica o próximo lote a partir do checkpoint.
    tamanho pequeno = pouca cota (ex.: 5).
    """
    if not config.API_CONFERENCIA:
        print("[verificacao] API_CONFERENCIA está False — nada a fazer.")
        return {"ok": 0, "alerta": 0, "erro": 0, "pulado": 0}

    inicio = checkpoint.get_ultimo_id()
    lote = _proximo_lote(inicio, tamanho)

    if not lote:
        # reinicia o ciclo
        print("[verificacao] Fim da base. Checkpoint volta a 0.")
        checkpoint.set_ultimo_id(0)
        return {"ok": 0, "alerta": 0, "erro": 0, "pulado": 0, "ciclo": "reiniciado"}

    contagem = {"ok": 0, "alerta": 0, "erro": 0, "pulado": 0}
    ultimo = inicio

    print(f"[verificacao] Lote de {len(lote)} itens (após id={inicio})")
    for id_, pergunta, resposta, tipo, flag in lote:
        print(f"  → id={id_} | {(pergunta or '')[:40]}")
        r = verificar_um(id_, pergunta, resposta or "", tipo, flag)
        st = r.get("status", "erro")
        contagem[st] = contagem.get(st, 0) + 1
        print(f"    {st}", r.get("flag") or r.get("motivo") or "")
        ultimo = id_

    checkpoint.set_ultimo_id(ultimo)
    print("[verificacao] Checkpoint:", ultimo)
    print("[verificacao] Resumo:", contagem)
    print("[verificacao] Flags:", flags_base.resumo_flags())
    return contagem