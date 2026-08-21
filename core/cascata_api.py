# ============================================================
#  Cascata de IA — Gemini → Groq (P1.5)
# ============================================================
import json
import os
import urllib.request
import urllib.error
import urllib.parse

from core import config

# --- Gemini ---
MODELOS = [
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
    "gemini-3.7-flash",
]

# --- Groq ---
ARQUIVO_CHAVE_GROQ = os.path.join(
    os.path.dirname(config.ARQUIVO_CHAVE), "api_key_groq.txt"
)
MODELOS_GROQ = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
]

MAX_TOKENS = 1024
FALLBACK_ATIVO = True


def carregar_chave():
    """Chave Gemini."""
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


def carregar_chave_groq():
    """Chave Groq."""
    for var in ("GROQ_API_KEY",):
        chave = os.environ.get(var, "").strip()
        if chave:
            return chave
    if os.path.exists(ARQUIVO_CHAVE_GROQ):
        with open(ARQUIVO_CHAVE_GROQ, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha and not linha.startswith("#"):
                    return linha
    return None


def fallback_disponivel():
    if not FALLBACK_ATIVO or not config.API_RESPOSTAS:
        return False
    return carregar_chave() is not None or carregar_chave_groq() is not None


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
        url,
        data=dados,
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
    textos = [
        p.get("text", "")
        for p in partes
        if isinstance(p, dict) and p.get("text")
    ]
    texto = "\n".join(textos).strip()
    return texto if texto else None


def _consultar_gemini(pergunta, historico=None):
    chave = carregar_chave()
    if not chave:
        print("[API Gemini] Sem chave (api_key.txt).")
        return None

    prompt = _montar_prompt(pergunta, historico)
    for modelo in MODELOS:
        try:
            resultado = _chamar_modelo(modelo, chave, prompt)
            texto = _extrair_texto(resultado)
            if texto:
                print(f"[API Gemini] OK via {modelo}")
                return texto
            print(f"[API Gemini] {modelo}: resposta vazia")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"[API Gemini] {modelo}: cota (429). Próximo...")
            elif e.code == 404:
                print(f"[API Gemini] {modelo}: não encontrado (404). Próximo...")
            else:
                print(f"[API Gemini] {modelo}: HTTP {e.code}")
        except Exception as e:
            print(f"[API Gemini] {modelo}: {type(e).__name__}: {e}")
    return None


def _consultar_groq(pergunta, historico=None):
    chave = carregar_chave_groq()
    if not chave:
        print("[API Groq] Sem chave (api_key_groq.txt ou GROQ_API_KEY).")
        return None

    prompt = _montar_prompt(pergunta, historico)
    url = "https://api.groq.com/openai/v1/chat/completions"

    for modelo in MODELOS_GROQ:
        corpo = {
            "model": modelo,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.4,
            "max_tokens": MAX_TOKENS,
        }
        dados = json.dumps(corpo).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=dados,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {chave}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                resultado = json.loads(resp.read().decode("utf-8"))
            choices = resultado.get("choices") or []
            if not choices:
                print(f"[API Groq] {modelo}: sem choices")
                continue
            texto = (choices[0].get("message") or {}).get("content") or ""
            texto = texto.strip()
            if texto:
                print(f"[API Groq] OK via {modelo}")
                return texto
            print(f"[API Groq] {modelo}: texto vazio")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"[API Groq] {modelo}: cota (429). Próximo...")
            else:
                print(f"[API Groq] {modelo}: HTTP {e.code}")
        except Exception as e:
            print(f"[API Groq] {modelo}: {type(e).__name__}: {e}")
    return None


def consultar_ia(pergunta, historico=None):
    if not FALLBACK_ATIVO or not config.API_RESPOSTAS:
        print("[API] Desativada (FALLBACK_ATIVO ou API_RESPOSTAS=False)")
        return None

    # 1) Gemini
    texto = _consultar_gemini(pergunta, historico)
    if texto:
        return texto

    # 2) Groq
    print("[API] Gemini não respondeu. Tentando Groq...")
    texto = _consultar_groq(pergunta, historico)
    if texto:
        return texto

    print("[API] Nenhum provedor respondeu.")
    return None