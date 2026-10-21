"""Tipos compartilhados."""
from enum import Enum


class Direcao(Enum):
    # (dx, dy, linha do sprite na folha: frente, esquerda, costas, direita)
    BAIXO = (0, 1, 0)
    ESQUERDA = (-1, 0, 1)
    CIMA = (0, -1, 2)
    DIREITA = (1, 0, 3)

    @property
    def dx(self):
        return self.value[0]

    @property
    def dy(self):
        return self.value[1]

    @property
    def linha_sprite(self):
        return self.value[2]
