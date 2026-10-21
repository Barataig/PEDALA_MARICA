"""Configurações centrais do jogo."""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ASSETS = RAIZ / "assets"
DATA = RAIZ / "data"
WEB = sys.platform == "emscripten"

TITULO = "Pedala, Maricá!"
LARGURA, ALTURA, FPS = 960, 640, 60
TILE = 64
ESCALA_PERSONAGEM = 4      # sprites de 16 px viram 64 px
TEMPO_PASSO = 0.22         # segundos para andar 1 tile
TEMPO_VIRAR = 0.09         # pausa ao só virar de direção
JOGADOR_FOLHA, JOGADOR_TOM = "NPC_7.png", 1
