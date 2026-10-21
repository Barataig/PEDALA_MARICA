import pytest

from src.core.config import DATA
from src.world.mapa import ErroMapa, Mapa

BASE = {"nome": "t", "linhas": ["GGGGG", "GGAGG", "GGGGG"], "inicio": [0, 0]}


def test_mapa_real_carrega():
    m = Mapa.carregar(DATA / "mapas" / "ponta_negra_teste.json")
    assert m.caminhavel(*m.inicio) and (m.largura, m.altura) == (32, 20)


def test_agua_e_fora_do_mapa_bloqueiam():
    m = Mapa.de_dict(BASE)
    assert m.caminhavel(1, 1) and not m.caminhavel(2, 1)
    assert not m.caminhavel(-1, 0) and not m.caminhavel(5, 0)


def test_objeto_bloqueia_toda_a_base():
    m = Mapa.de_dict({**BASE, "objetos": [{"tipo": "casa_palha_1", "col": 3, "linha": 0}]})
    assert not m.caminhavel(3, 0) and not m.caminhavel(4, 0) and m.caminhavel(2, 0)


@pytest.mark.parametrize("quebra", [
    {"linhas": ["GGG", "GG"]},
    {"linhas": ["GGX"]},
    {"inicio": [2, 1]},
    {"objetos": [{"tipo": "inexistente", "col": 0, "linha": 0}]},
    {"objetos": [{"tipo": "arbusto_1", "col": 2, "linha": 1}]},
])
def test_erros_de_mapa(quebra):
    with pytest.raises(ErroMapa):
        Mapa.de_dict({**BASE, **quebra})


def test_arquivo_inexistente():
    with pytest.raises(ErroMapa):
        Mapa.carregar(DATA / "mapas" / "nao_existe.json")
