import os
from pathlib import Path

# DEFININDO O DIR ROOT
# os.chdir(str(Path(__file__).parent))

from src.app import load_app

# INICIANDO O DATA APP
load_app()
