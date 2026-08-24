import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from manutencao.verificacao import rodar_lote

# lote pequeno para não gastar cota
rodar_lote(tamanho=3)