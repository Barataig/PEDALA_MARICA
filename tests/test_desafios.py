import json
import random

from src.core.config import DATA
from src.systems.desafios import LigarPares, LinhaDoTempo, MitoVerdade, criar_desafio

CHEFOES = json.loads((DATA / "chefoes.json").read_text(encoding="utf-8"))


def _jogar_certo(d):
    """Resolve qualquer desafio sem errar (usa só a interface pública + dados)."""
    while not d.terminou:
        if isinstance(d, LinhaDoTempo):
            i = min(range(len(d.restantes)), key=lambda k: d.restantes[k]["chave"])
        elif isinstance(d, LigarPares):
            if d.sel is None:
                d.escolher(0)
                continue
            alvo = next(p["b"] for p in d.pares if p["a"] == d.sel)
            i = d.dir.index(alvo)
        else:
            i = 0 if d.itens[d.i]["verdade"] else 1
        d.escolher(i)


def test_os_tres_chefoes_podem_ser_vencidos_sem_errar():
    for k in ("boss_1", "boss_2", "boss_3"):
        d = criar_desafio(CHEFOES[k]["desafio"], random.Random(1))
        _jogar_certo(d)
        assert d.venceu and d.vidas == d.vidas_max


def test_linha_do_tempo_erro_custa_vida_e_tres_erros_derrotam():
    d = criar_desafio(CHEFOES["boss_1"]["desafio"], random.Random(2))
    for _ in range(3):
        errada = max(range(len(d.restantes)), key=lambda k: d.restantes[k]["chave"])
        ok, msg = d.escolher(errada)
        assert not ok and "depois" in msg
    assert d.terminou and not d.venceu and d.vidas == 0


def test_ligar_pares_par_errado_custa_vida():
    d = criar_desafio(CHEFOES["boss_2"]["desafio"], random.Random(3))
    d.escolher(0)
    a = d.sel
    certo = next(p["b"] for p in d.pares if p["a"] == a)
    errado = next(i for i, b in enumerate(d.dir) if b != certo)
    ok, _ = d.escolher(errado)
    assert not ok and d.vidas == 2 and d.sel is None


def test_mito_verdade_ultimo_erro_com_vida_sobrando_ainda_vence():
    d = MitoVerdade("t", [{"texto": "x", "verdade": True, "explicacao": "e"}], 3, random.Random(0))
    ok, _ = d.escolher(1)                 # errou, mas ainda tem 2 vidas
    assert not ok and d.terminou and d.venceu and d.vidas == 2


def test_pistas_finais_apontam_para_pois_do_mapa():
    ids = {p["id"] for p in json.loads((DATA / "mapas" / "marica.json").read_text(encoding="utf-8"))["pois"]}
    assert all(p["alvo"] in ids for p in CHEFOES["final"]["pistas"])
