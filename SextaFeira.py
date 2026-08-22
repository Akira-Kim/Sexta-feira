#!/usr/bin/env python3
# ============================================================
#  Sexta-feira — versão CONSOLE 
# ============================================================
import chat as pc

nome_maquina = pc.NOME_ASSISTENTE

pc.saudacoes(nome_maquina)

while True:
    texto = pc.recebeTexto()
    if texto is None:
        continue
    resposta = pc.buscaResposta(texto)
    if pc.exibeResposta(resposta, nome_maquina) == "fim":
        break
