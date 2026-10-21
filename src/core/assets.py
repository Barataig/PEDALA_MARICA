"""Carregamento e cache de imagens e sprites."""
import pygame

from src.core.config import ASSETS, ESCALA_PERSONAGEM, TILE
from src.core.tipos import Direcao

CELULA = 16              # tamanho de cada quadro nas folhas dos personagens
QUADROS_ANDANDO = 0.11   # segundos por quadro andando
QUADROS_PARADO = 0.40    # segundos por quadro parado


class FolhaPersonagem:
    """Folha Tiny Neighbours: linha 0 = título; depois 3 tons x 4 direções.
    Colunas 0-3 = parado, 4-7 = andando."""

    def __init__(self, superficie, tom, escala=ESCALA_PERSONAGEM):
        lado = CELULA * escala
        self._quadros = {}
        for d in Direcao:
            y = (1 + tom * 4 + d.linha_sprite) * CELULA
            cortes = [
                pygame.transform.scale(
                    superficie.subsurface(pygame.Rect(c * CELULA, y, CELULA, CELULA)), (lado, lado))
                for c in range(8)
            ]
            self._quadros[(d, False)] = cortes[:4]
            self._quadros[(d, True)] = cortes[4:]

    def quadro(self, direcao, andando, tempo):
        passo = QUADROS_ANDANDO if andando else QUADROS_PARADO
        return self._quadros[(direcao, andando)][int(tempo / passo) % 4]


class Recursos:
    def __init__(self, raiz=ASSETS):
        self.raiz = raiz
        self._imagens, self._folhas = {}, {}

    def imagem(self, relativo):
        if relativo not in self._imagens:
            caminho = self.raiz / relativo
            if not caminho.exists():
                raise FileNotFoundError(
                    f"Imagem não encontrada: {caminho}. Confira se a pasta 'assets' está junto do jogo.")
            self._imagens[relativo] = pygame.image.load(str(caminho)).convert_alpha()
        return self._imagens[relativo]

    def personagem(self, arquivo, tom):
        chave = (arquivo, tom)
        if chave not in self._folhas:
            self._folhas[chave] = FolhaPersonagem(self.imagem(f"personagens/{arquivo}"), tom)
        return self._folhas[chave]

    def terreno(self, nome):
        """Devolve {(coluna, linha): Surface} da folha 4x4 de 'grama' ou 'areia'."""
        folha = self.imagem("mundo/terreno_grama_areia.png")
        origem = {"grama": 0, "areia": 320}[nome]
        return {(c, l): folha.subsurface(pygame.Rect(origem + c * TILE, l * TILE, TILE, TILE))
                for c in range(4) for l in range(4)}

    def sombra(self):
        if "sombra" not in self._imagens:
            s = pygame.Surface((44, 16), pygame.SRCALPHA)
            pygame.draw.ellipse(s, (0, 0, 0, 70), s.get_rect())
            self._imagens["sombra"] = s
        return self._imagens["sombra"]
