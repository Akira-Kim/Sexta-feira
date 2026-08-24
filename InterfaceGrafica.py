import chat as pc
from tkinter import *
import re

nome_maquina = pc.NOME_ASSISTENTE if hasattr(pc, "NOME_ASSISTENTE") else "Sexta-feira"

main_window = Tk()
main_window.title("Sexta-feira")
main_window.geometry("700x600")

entrada_sugestao = False
ultima_pergunta = ""
ultima_chave_base = None

texto_conversa = Text(
    main_window, width=80, height=25, state=DISABLED, wrap=WORD
)
texto_conversa.pack(pady=10)

frame = Frame(main_window)
frame.pack()

entrada = Entry(frame, width=60)
entrada.grid(row=0, column=0, padx=5)


def escrever(mensagem):
    texto_conversa.config(state=NORMAL)
    texto_conversa.insert(END, mensagem + "\n")
    texto_conversa.config(state=DISABLED)
    texto_conversa.see(END)


def contem_palavra_proibida(texto):
    texto_normalizado = pc.normalizar(texto)
    for palavra in pc.PALAVRAS_PROIBIDAS:
        if re.search(
            rf"\b{re.escape(pc.remover_acentos(palavra.lower()))}\b",
            texto_normalizado,
        ):
            return True
    return False


def _usuario_disse_nao_sei(texto):
    try:
        from core.aprender import usuario_disse_nao_sei
        return usuario_disse_nao_sei(texto)
    except ImportError:
        p = pc.normalizar(texto)
        if not p:
            return True
        if p in ("nao sei", "sei la", "ignora", "passa", "skip", "tanto faz"):
            return True
        if p.startswith("nao sei") or p.startswith("sei la"):
            return True
        if "nao faco ideia" in p or "nao grava" in p or "nao salva" in p:
            return True
        return False


def enviar(event=None):
    global entrada_sugestao, ultima_pergunta, ultima_chave_base

    texto = entrada.get().strip()
    if texto == "":
        return

    entrada.delete(0, END)
    escrever("Você: " + texto)

    # 1) Linguagem livre / educada
    try:
        from core import politica_linguagem
        msg_cmd = politica_linguagem.processar_comando_linguagem(texto)
    except ImportError:
        msg_cmd = None
    if msg_cmd:
        escrever(nome_maquina + ": " + msg_cmd)
        return

    # 1b) Menu API
    try:
        from core import menu
        msg_menu = menu.processar_comando_menu(texto)
    except ImportError:
        msg_menu = None
    if msg_menu:
        escrever(nome_maquina + ": " + msg_menu)
        return

    # 1c) Info fixa
    try:
        from manutencao import info_fixa
        msg_fixa = info_fixa.processar_comando_info_fixa(texto, ultima_chave_base)
    except ImportError:
        msg_fixa = None
    if msg_fixa:
        escrever(nome_maquina + ": " + msg_fixa)
        return

    # 2) Modo ensino
    if entrada_sugestao:
        if _usuario_disse_nao_sei(texto):
            escrever(nome_maquina + ": Tudo bem, não vou gravar. Seguimos.")
            entrada_sugestao = False
            return
        pc.salva_sugestao(ultima_pergunta, texto)
        escrever(nome_maquina + ": Obrigado! Aprendi uma nova resposta.")
        entrada_sugestao = False
        return

    # 3) Lista de evitar
    if contem_palavra_proibida(texto):
        try:
            from core import politica_linguagem
            bloquear = politica_linguagem.deve_bloquear_palavra_proibida()
        except ImportError:
            bloquear = True
        if bloquear:
            escrever(
                nome_maquina
                + ": Prefiro evitar esse tipo de linguagem. "
                'Se quiser, diga "linguagem livre" ou "seja honesto".'
            )
            return

    # 4) Despedida
    pergunta = pc.normalizar(texto)
    if pergunta in ["tchau", "adeus", "até logo", "ate logo"]:
        pc.limpar_contexto()
        escrever(nome_maquina + ": Volte sempre!")
        return

    # 5) Busca resposta
    resposta = pc.buscaResposta_GUI(texto)

    if resposta is None:
        escrever(nome_maquina + ": Não sei responder isso.")
        escrever(nome_maquina + ": Qual deveria ser a resposta?")
        ultima_pergunta = texto
        entrada_sugestao = True
    else:
        escrever(nome_maquina + ": " + resposta)
        ultima_chave_base = pc.preparar_pergunta(texto)


Button(frame, text="Enviar", command=enviar).grid(row=0, column=1)
entrada.bind("<Return>", enviar)

escrever(pc.saudacoes_GUI(nome_maquina))
entrada.focus()
main_window.mainloop()