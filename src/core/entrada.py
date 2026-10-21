"""Leitura das setas/WASD por eventos (vale a última tecla pressionada)."""
import pygame

from src.core.tipos import Direcao

TECLAS = {
    pygame.K_UP: Direcao.CIMA, pygame.K_w: Direcao.CIMA,
    pygame.K_DOWN: Direcao.BAIXO, pygame.K_s: Direcao.BAIXO,
    pygame.K_LEFT: Direcao.ESQUERDA, pygame.K_a: Direcao.ESQUERDA,
    pygame.K_RIGHT: Direcao.DIREITA, pygame.K_d: Direcao.DIREITA,
}


class EntradaDirecional:
    def __init__(self):
        self._teclas = []

    def processar_evento(self, ev):
        if ev.type == pygame.KEYDOWN and ev.key in TECLAS:
            if ev.key in self._teclas:
                self._teclas.remove(ev.key)
            self._teclas.append(ev.key)
        elif ev.type == pygame.KEYUP and ev.key in self._teclas:
            self._teclas.remove(ev.key)
        elif ev.type == getattr(pygame, "WINDOWFOCUSLOST", -1):
            self._teclas.clear()

    def direcao_atual(self):
        return TECLAS[self._teclas[-1]] if self._teclas else None
