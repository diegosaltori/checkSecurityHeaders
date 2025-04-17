import os
import shutil

def clean_pycache(directory="."):
    """Remove todos os diretórios __pycache__ recursivamente."""
    for root, dirs, files in os.walk(directory):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            shutil.rmtree(pycache_path)
            #print(f"Removido: {pycache_path}")

