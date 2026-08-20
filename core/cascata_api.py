# ============================================================
#  Cascata de IA — v01: só Gemini (P1 expandirá Groq/OpenRouter)
# ============================================================
import json
import os
import urllib.request
import urllib.error
import urllib.parse

from core import config

MODELOS = [
    "gemini-flash-latest",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash",
]
MAX_TOKENS = 1024
FALLBACK_ATIVO = True


def carregar_chave():
    for var in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        chave = os.environ.get(var, "").strip()
        if chave:
            return chave
    if os.path.exists(config.ARQUIVO_CHAVE):
        with open(config.ARQUIVO_CHAVE, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha and not linha.startswith("#"):
                    return linha
    return None


def fallback_disponivel():
    return FALLBACK_ATIVO and config.API_RESPOSTAS and carregar_chave() is not None


def _montar_prompt(pergunta, historico=None):
    nome = config.NOME_ASSISTENTE
    partes = [
        f"Você é a {nome}, assistente em português do Brasil.",
        "Regras de resposta:",
        "- Responda de forma completa e clara (não corte no meio da frase).",
        "- Use entre 2 e 5 frases curtas, o suficiente para responder bem.",
        "- Não use markdown, listas longas nem títulos.",
        "- Se não souber com certeza, diga isso com honestidade.",
        "",
    ]
    if historico:
        partes.append("Conversa recente:")
        for item in historico[-4:]:
            if item.get("usuario"):
                partes.append(f"Usuário: {item['usuario']}")
            msg = item.get("sexta") or item.get("maria")
            if msg:
                partes.append(f"{nome}: {msg}")
        partes.append("")
    partes.append(f"Pergunta atual do usuário: {pergunta}")
    return "\n".join(partes)


def _chamar_modelo(modelo, chave, prompt):
    corpo = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": MAX_TOKENS,
        },
    }
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{modelo}:generateContent?key={urllib.parse.quote(chave)}"
    )
    dados = json.dumps(corpo).encode("utf-8")
    req = urllib.request.Request(
        url, data=dados,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _extrair_texto(resultado):
    candidatos = resultado.get("candidates") or []
    if not candidatos:
        return None
    cand = candidatos[0]
    razao = cand.get("finishReason") or cand.get("finish_reason")
    if razao and str(razao).upper() in ("MAX_TOKENS", "LENGTH"):
        print("[API] Aviso: resposta pode ter sido cortada (MAX_TOKENS).")
    partes = cand.get("content", {}).get("parts") or []
    textos = [p.get("text", "") for p in partes if isinstance(p, dict) and p.get("text")]
    texto = "\n".join(textos).strip()
    return texto if texto else None


def consultar_ia(pergunta, historico=None):
    """Nome legado usado pelo fluxo v01."""
    if not FALLBACK_ATIVO or not config.API_RESPOSTAS:
        print("[API] Desativada (FALLBACK_ATIVO ou API_RESPOSTAS=False)")
        return None
    chave = carregar_chave()
    if not chave:
        print("[API] Sem chave. Crie api_key.txt ou defina GEMINI_API_KEY.")
        return None

    prompt = _montar_prompt(pergunta, historico)
    for modelo in MODELOS:
        try:
            resultado = _chamar_modelo(modelo, chave, prompt)
            texto = _extrair_texto(resultado)
            if texto:
                print(f"[API] OK via {modelo}")
                return texto
            print(f"[API] {modelo}: resposta vazia")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"[API] {modelo}: cota esgotada (429). Tentando próximo...")
            elif e.code == 404:
                print(f"[API] {modelo}: não encontrado (404). Tentando próximo...")
            else:
                print(f"[API] {modelo} falhou: HTTP {e.code}")
        except Exception as e:
            print(f"[API] {modelo} falhou: {type(e).__name__}: {e}")

    print("[API] Nenhum modelo respondeu.")
    return None
