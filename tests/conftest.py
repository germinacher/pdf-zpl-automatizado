import sys
import os
 
# Agrega el directorio raíz del proyecto al path para que pytest pueda importar main.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))