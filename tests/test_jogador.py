import pygame

from src.core.config import TEMPO_PASSO, TEMPO_VIRAR, TILE
from src.core.entrada import EntradaDirecional
from src.core.tipos import Direcao
from src.entities.jogador import Jogador
from src.world.mapa import Mapa

MAPA = Mapa.de_dict({"nome": "t", "linhas": ["GGGGG", "GGAGG", "GGGGG"], "inicio": [0, 0]})


def andar(j, direcao, segundos, passo=1 / 60):
    for _ in range(round(segundos / passo)):
        j.atualizar(passo, direcao, MAPA)


def test_so_vira_antes_de_andar():
    j = Jogador(0, 0)
    j.atualizar(1 / 60, Direcao.DIREITA, MAPA)
    assert j.direcao == Direcao.DIREITA and not j.andando
    andar(j, Direcao.DIREITA, TEMPO_VIRAR + 0.05)
    assert j.andando


def test_anda_um_tile_por_passo():
    j = Jogador(0, 0, Direcao.DIREITA)
    j.atualizar(TEMPO_PASSO, Direcao.DIREITA, MAPA)
    assert (j.col, j.linha) == (1, 0) and not j.andando
    assert j.posicao_pixels() == (TILE, 0)


def test_posicao_interpolada_no_meio_do_passo():
    j = Jogador(0, 0, Direcao.DIREITA)
    j.atualizar(TEMPO_PASSO / 2, Direcao.DIREITA, MAPA)
    assert j.andando and abs(j.posicao_pixels()[0] - TILE / 2) < 1e-6


def test_agua_bloqueia():
    j = Jogador(1, 1, Direcao.DIREITA)       # (2,1) é água
    andar(j, Direcao.DIREITA, 1.0)
    assert (j.col, j.linha) == (1, 1) and not j.andando


def test_limite_do_mapa_bloqueia():
    j = Jogador(0, 0, Direcao.ESQUERDA)
    andar(j, Direcao.ESQUERDA, 1.0)
    assert (j.col, j.linha) == (0, 0)


def test_segurar_tecla_anda_varios_tiles_sem_parar():
    j = Jogador(0, 0, Direcao.DIREITA)
    andar(j, Direcao.DIREITA, TEMPO_PASSO * 4 + 0.001)
    assert j.col == 4


def test_soltar_tecla_termina_o_passo_em_andamento():
    j = Jogador(0, 0, Direcao.DIREITA)
    j.atualizar(TEMPO_PASSO / 2, Direcao.DIREITA, MAPA)
    andar(j, None, 1.0)
    assert (j.col, j.linha) == (1, 0) and not j.andando


def test_entrada_usa_a_ultima_tecla_pressionada():
    e = EntradaDirecional()
    ev = lambda tipo, k: pygame.event.Event(tipo, key=k)
    e.processar_evento(ev(pygame.KEYDOWN, pygame.K_RIGHT))
    e.processar_evento(ev(pygame.KEYDOWN, pygame.K_w))
    assert e.direcao_atual() == Direcao.CIMA
    e.processar_evento(ev(pygame.KEYUP, pygame.K_w))
    assert e.direcao_atual() == Direcao.DIREITA
    e.processar_evento(ev(pygame.KEYUP, pygame.K_RIGHT))
    assert e.direcao_atual() is None
