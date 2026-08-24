import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from manutencao.correcao import corrigir_lote

# Só red, no máximo 2 por vez (pouca cota)
corrigir_lote(prioridade="red", limite=2, aplicar_automatico=True)