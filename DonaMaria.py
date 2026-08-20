#!/usr/bin/env python3
# Compat: redireciona para SextaFeira.py
import runpy
import os
runpy.run_path(os.path.join(os.path.dirname(__file__), "SextaFeira.py"), run_name="__main__")
