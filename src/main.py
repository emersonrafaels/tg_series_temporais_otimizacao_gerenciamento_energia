import os
from pathlib import Path

# DEFININDO O DIR ROOT
# os.chdir(str(Path(__file__).parent))

from app import load_app

# INICIANDO O DATA APP
load_app()