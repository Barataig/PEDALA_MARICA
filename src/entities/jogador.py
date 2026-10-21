"""Jogador: movimento em grade, tile a tile, com interpolação suave."""
from src.core.config import TEMPO_PASSO, TEMPO_VIRAR, TILE
from src.core.tipos import Direcao


class Jogador:
    def __init__(self, col, linha, direcao=Direcao.BAIXO):
        self.col, self.linha, self.direcao = col, linha, direcao
        self.tempo_passo = TEMPO_PASSO
        self.destino = None
        self.progresso = 0.0
        self.espera_virar = 0.0
        self.tempo_anim = 0.0

    @property
    def andando(self):
        return self.destino is not None

    def posicao_pixels(self):
        if self.destino is None:
            return self.col * TILE, self.linha * TILE
        dc, dl = self.destino
        p = self.progresso
        return (self.col + (dc - self.col) * p) * TILE, (self.linha + (dl - self.linha) * p) * TILE

    def atualizar(self, dt, desejada, mapa):
        """desejada: Direcao mantida pressionada, ou None."""
        self.tempo_anim += dt
        restante, chegou_agora = dt, False
        while restante > 1e-9:
            if self.destino is not None:
                falta = (1 - self.progresso) * self.tempo_passo
                if restante < falta:
                    self.progresso += restante / self.tempo_passo
                    return
                restante -= falta
                self.col, self.linha = self.destino
                self.destino, self.progresso, chegou_agora = None, 0.0, True
                continue
            if desejada is None:
                self.espera_virar = 0.0
                return
            if desejada != self.direcao:
                self.direcao = desejada
                if not chegou_agora:          # só vira antes de andar (como no FireRed)
                    self.espera_virar = TEMPO_VIRAR
                    return
            if self.espera_virar > 0:
                gasto = min(restante, self.espera_virar)
                self.espera_virar -= gasto
                restante -= gasto
                if self.espera_virar > 0:
                    return
            alvo = (self.col + self.direcao.dx, self.linha + self.direcao.dy)
            if not mapa.caminhavel(*alvo):
                return
            self.destino, self.progresso, chegou_agora = alvo, 0.0, False
