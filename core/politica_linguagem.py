# ============================================================
#  Política de linguagem — evitar vs livre (sem botão)
# ============================================================
from core.interpretacao import normalizar

# Estado da sessão (volta ao padrão ao reiniciar o app)
linguagem_livre = False

FRASES_LIBERAR = (
    # originais
    "pode xingar",
    "linguagem livre",
    "honestidade total",
    "sem filtro",
    "pode falar palavrao",
    "modo adulto",
    "pode usar palavrao",
    # naturais (seu pedido)
    "seja honesto",
    "seja honesta",
    "pode ser honesto",
    "pode ser honesta",
    "fala livre",
    "falar livre",
    "falar livremente",
    "permite falar livremente",
    "pode falar livremente",
    "sem censura",
    "pode falar tudo",
    "pode ser direta",
    "pode ser direto",
)

FRASES_RESTRINGIR = (
    # originais
    "evita palavrao",
    "sem xingamento",
    "modo educado",
    "volta a filtrar",
    "linguagem limpa",
    "sem palavrao",
    # naturais (seu pedido)
    "melhore o vocabulario",
    "melhora o vocabulario",
    "melhorar o vocabulario",
    "nao to afim disso",
    "nao estou afim disso",
    "nao to a fim disso",
    "para com isso",
    "respeita",
    "seja educada",
    "seja educado",
    "fala direito",
    "sem grosseria",
)


def processar_comando_linguagem(texto):
    """
    Se a mensagem for só (ou principalmente) um comando de filtro,
    atualiza o estado e devolve uma resposta pronta.
    Senão devolve None e o fluxo normal continua.
    """
    global linguagem_livre
    p = normalizar(texto)

    for f in FRASES_LIBERAR:
        if f in p or p == normalizar(f):
            linguagem_livre = True
            return "Ok. Linguagem livre nesta conversa — posso ser mais direta, inclusive com baixo calão se fizer sentido."

    for f in FRASES_RESTRINGIR:
        if f in p or p == normalizar(f):
            linguagem_livre = False
            return "Ok. Volto a evitar palavrões e xingamentos."

    return None


def deve_bloquear_palavra_proibida():
    """True = aplicar a lista de evitar; False = ignorar a restrição."""
    return not linguagem_livre