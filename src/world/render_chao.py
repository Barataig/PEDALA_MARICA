"""Monta, uma única vez, a imagem do chão do mapa (água + areia + grama)."""
import pygame

from src.core.config import TILE
from src.world.autotile import escolher_celula

REVESTIMENTOS = {
    "calcada_pedra": "mundo/calcada_pedra.png",
    "trilha_terra": "mundo/trilha_terra.png",
    "morro_verde": "mundo/morro_verde.png",
}


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
    agua_mar = recursos.imagem("mundo/agua_mar.png")
    agua_lagoa = recursos.imagem("mundo/agua_lagoa.png")
    tiles_lagoa = {(p["col"], p["linha"]) for p in mapa.dados.get("agua_laguna", [])}
    for l in range(mapa.altura):
        for c in range(mapa.largura):
            textura = agua_lagoa if (c, l) in tiles_lagoa else agua_mar
            sup.blit(textura, (c * TILE, l * TILE))
    _camada(sup, mapa, recursos.terreno("areia"), {"S", "G"})   # areia por baixo
    _camada(sup, mapa, recursos.terreno("grama"), {"G"})        # grama por cima
    for revestimento in mapa.dados.get("revestimentos", []):
        imagem = recursos.imagem(REVESTIMENTOS[revestimento["tipo"]])
        sup.blit(imagem, (revestimento["col"] * TILE, revestimento["linha"] * TILE))
    return sup
