#!/usr/bin/env python3
# ============================================================
#  INICIAR — Sexta-feira
#    python iniciar.py          → GUI
#    python iniciar.py console  → terminal
# ============================================================
import os
import sys
import runpy

PASTA = os.path.dirname(os.path.abspath(__file__))
os.chdir(PASTA)
sys.path.insert(0, PASTA)


def verificar_arquivos(modo):
    obrigatorios = ["chat.py", "core/config.py", "core/conhecimento.py"]
    if modo == "gui":
        obrigatorios.append("InterfaceGrafica.py")
    else:
        obrigatorios.append("SextaFeira.py")
    # db em raiz ou dados/bases
    tem_db = os.path.exists("conhecimento.db") or os.path.exists(
        os.path.join("dados", "bases", "conhecimento.db")
    )
    faltando = [f for f in obrigatorios if not os.path.exists(f)]
    if not tem_db:
        faltando.append("conhecimento.db")
    if faltando:
        print("=" * 50)
        print("ERRO: arquivos não encontrados:")
        for f in faltando:
            print(f"  - {f}")
        print(f"\nPasta atual:\n  {PASTA}")
        print("=" * 50)
        input("Pressione Enter para sair...")
        sys.exit(1)


def main():
    modo = "gui"
    if len(sys.argv) > 1 and sys.argv[1].lower() in (
        "console", "-c", "--console", "terminal"
    ):
        modo = "console"
    verificar_arquivos(modo)
    if modo == "console":
        print("[Iniciar] Abrindo console — Sexta-feira...")
        runpy.run_path("SextaFeira.py", run_name="__main__")
    else:
        print("[Iniciar] Abrindo interface gráfica — Sexta-feira...")
        runpy.run_path("InterfaceGrafica.py", run_name="__main__")


if __name__ == "__main__":
    main()
