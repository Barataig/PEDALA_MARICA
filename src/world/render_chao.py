"""Monta, uma única vez, a imagem do chão do mapa (água + areia + grama)."""
import pygame

from src.core.config import TILE
from src.world.autotile import escolher_celula


def _camada(sup, mapa, celulas, terrenos):
    def presente(c, l):
        t = mapa.terreno(c, l)
        return t is None or t in terrenos   # fora do mapa continua o terreno

    for l in range(mapa.altura):
        for c in range(mapa.largura):
            if mapa.terreno(c, l) in terrenos:
                chave = escolher_celula(presente(c, l - 1), presente(c + 1, l),
                                        presente(c, l + 1), presente(c - 1, l))
                sup.blit(celulas[chave], (c * TILE, l * TILE))


def montar_superficie_chao(mapa, recursos):
    sup = pygame.Surface((mapa.largura_px, mapa.altura_px))
    agua = recursos.imagem("mundo/agua.png")
    for l in range(mapa.altura):
        for c in range(mapa.largura):
            sup.blit(agua, (c * TILE, l * TILE))
    _camada(sup, mapa, recursos.terreno("areia"), {"S", "G"})   # areia por baixo
    _camada(sup, mapa, recursos.terreno("grama"), {"G"})        # grama por cima
    return sup
