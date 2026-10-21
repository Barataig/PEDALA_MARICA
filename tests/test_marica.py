import json
from collections import deque

import pytest

from src.core.config import DATA
from src.systems.perguntas import ErroPerguntas, carregar_perguntas, verificar_npcs
from src.systems.pontuacao import PERGUNTAS_POR_FASE, TOTAL_FASES
from src.systems.progresso import Progresso
from src.ui.texto import quebrar
from src.world.mapa import Mapa

MAPA = DATA / "mapas" / "marica.json"
BANCO = DATA / "perguntas.json"


@pytest.fixture(scope="module")
def mapa():
    return Mapa.carregar(MAPA)


class FonteFalsa:
    def size(self, t):
        return (len(t) * 10, 20)


def test_quebrar_respeita_largura_e_paragrafos():
    linhas = quebrar("um dois tres quatro\ncinco", FonteFalsa(), 100)
    assert linhas == ["um dois", "tres", "quatro", "cinco"]
    assert quebrar("palavragigantesca", FonteFalsa(), 50) == ["palavragigantesca"]


def test_cinco_npcs_por_fase_e_perguntas_unicas(mapa):
    guias = [n for n in mapa.dados["npcs"] if n.get("papel", "guia") == "guia"]
    for f in range(1, TOTAL_FASES + 1):
        assert len([n for n in guias if n["fase"] == f]) == PERGUNTAS_POR_FASE
    ids = [n["pergunta"] for n in guias]
    assert len(ids) == len(set(ids))


def test_mapa_representa_quatro_bairros_com_npcs(mapa):
    zonas = mapa.dados["zonas"]
    assert [z["nome"] for z in zonas] == ["Ponta Negra", "Araçatiba", "Espraiado", "Centro"]
    assert zonas[0]["col_ini"] == 0 and zonas[-1]["col_fim"] == mapa.largura - 1
    assert all(a["col_fim"] + 1 == b["col_ini"] for a, b in zip(zonas, zonas[1:]))
    for zona in zonas:
        assert any(zona["col_ini"] <= n["col"] <= zona["col_fim"] for n in mapa.dados["npcs"])


def test_farol_em_ponta_negra_e_lagoa_com_contorno_variado(mapa):
    farol = [p for p in mapa.dados["pois"] if p["id"] == "farol"]
    torre = next(o for o in mapa.dados["objetos"] if o["tipo"] == "torre_azul")
    assert len(farol) == 2 and all(p["col"] < 22 for p in farol)
    assert torre["col"] < 22
    assert mapa.terreno(27, 12) == "A"
    assert mapa.terreno(25, 12) != "A"
    assert mapa.terreno(27, 10) == "A" and mapa.terreno(26, 10) != "A"


def test_revestimentos_visuais_diferenciam_orla_trilhas_e_centro(mapa):
    revestimentos = mapa.dados["revestimentos"]
    assert {"calcada_pedra", "trilha_terra", "morro_verde"} <= {r["tipo"] for r in revestimentos}
    assert any(22 <= r["col"] <= 33 for r in revestimentos)
    assert any(34 <= r["col"] <= 45 and r["tipo"] == "trilha_terra" for r in revestimentos)
    assert any(r["col"] >= 46 and r["tipo"] == "calcada_pedra" for r in revestimentos)
    assert any(34 <= r["col"] <= 45 and r["tipo"] == "morro_verde" for r in revestimentos)
    assert all(mapa.caminhavel(r["col"], r["linha"]) for r in revestimentos)


def test_lagoa_tem_textura_distinta_e_mantem_agua_no_terreno(mapa):
    lagoa = mapa.dados["agua_laguna"]
    assert len(lagoa) > 100
    assert all(mapa.terreno(p["col"], p["linha"]) == "A" for p in lagoa)


@pytest.mark.skipif(not BANCO.exists(), reason="coloque o banco em data/perguntas.json")
def test_npcs_apontam_para_perguntas_existentes(mapa):
    verificar_npcs(mapa.dados["npcs"], carregar_perguntas(BANCO))


def test_verificar_npcs_acusa_id_inexistente():
    with pytest.raises(ErroPerguntas):
        verificar_npcs([{"id": "x", "pergunta": "nao_existe"}], {})


def test_tudo_alcancavel_a_partir_do_inicio(mapa):
    for f in range(1, TOTAL_FASES + 1):
        mapa.liberar(f)
    npcs = {(n["col"], n["linha"]) for n in mapa.dados["npcs"]}
    visto, fila = {mapa.inicio}, deque([mapa.inicio])
    while fila:
        c, l = fila.popleft()
        for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (c + d[0], l + d[1])
            if p not in visto and p not in npcs and mapa.caminhavel(*p):
                visto.add(p)
                fila.append(p)
    alvos = [(n["col"], n["linha"]) for n in mapa.dados["npcs"]] + [(p["col"], p["linha"]) for p in mapa.dados["pois"]]
    for c, l in alvos:
        assert any((c + dc, l + dl) in visto for dc, dl in ((1, 0), (-1, 0), (0, 1), (0, -1))), (c, l)


def test_barreiras_bloqueiam_ate_liberar(tmp_path):
    m = Mapa.carregar(MAPA)
    assert not m.caminhavel(21, 16) and not m.caminhavel(45, 16)
    assert m.liberar(1) and m.caminhavel(21, 16) and not m.caminhavel(45, 16)
    assert m.liberar(2) and m.caminhavel(45, 16)
    assert not m.liberar(3)


def test_progresso_fecha_fase_com_cinco_respostas(tmp_path):
    p = Progresso(tmp_path / "save.json")
    for i in range(4):
        assert p.responder(1, f"n{i}", True) is None
    res = p.responder(1, "n4", True)
    assert res["pontos"] == 550 and res["perfeita"] and p.placar.concluida(1) and p.placar.liberada(2)
    p.reiniciar_fase(1)
    for i in range(5):
        res = p.responder(1, f"n{i}", False)
    assert res["pontos"] == 0 and not res["melhorou"] and p.placar.total == 550   # recorde mantido


def test_save_e_carregar_ida_e_volta(tmp_path):
    arq = tmp_path / "save.json"
    p = Progresso(arq)
    p.responder(1, "a", True)
    p.curiosidades.add("canal")
    p.intro_vista = True
    p.salvar()
    q = Progresso(arq)
    q.carregar()
    assert q.ja_respondeu(1, "a") and "canal" in q.curiosidades and q.intro_vista


def test_save_corrompido_e_ignorado(tmp_path):
    arq = tmp_path / "save.json"
    arq.write_text("{ isso não é json", encoding="utf-8")
    p = Progresso(arq)
    p.carregar()
    assert p.placar.total == 0


def test_npcs_e_conchas_em_lugares_validos(mapa):
    for n in mapa.dados["npcs"]:
        assert mapa.caminhavel(n["col"], n["linha"]), n["id"]
    assert len(mapa.dados["conchas"]) == 15
    for c in mapa.dados["conchas"]:
        assert mapa.caminhavel(c["col"], c["linha"]), c["id"]


def test_perguntas_do_pool_nao_se_repetem(mapa):
    ids = []
    for n in mapa.dados["npcs"]:
        if n.get("pergunta"):
            ids += [n["pergunta"]] + n.get("extras", [])
    assert len(ids) == len(set(ids))


def test_verificar_npcs_confere_perguntas_extras():
    with pytest.raises(ErroPerguntas):
        verificar_npcs([{"id": "x", "pergunta": "a", "extras": ["b"]}], {"a": 1})


def test_menos_de_tres_acertos_nao_aprova(tmp_path):
    p = Progresso(tmp_path / "s.json")
    for i, ok in enumerate([True, True, False, False, False]):
        res = p.responder(1, f"n{i}", ok)
    assert res["acertos"] == 2 and not res["aprovada"] and not p.placar.liberada(2)
    p.reiniciar_fase(1)
    for i, ok in enumerate([True, True, True, False, False]):
        res = p.responder(1, f"n{i}", ok)
    assert res["aprovada"] and p.placar.liberada(2) and p.tentativas["n0"] == 2


def test_conchas_e_tentativas_sobrevivem_ao_save(tmp_path):
    arq = tmp_path / "s.json"
    p = Progresso(arq)
    p.conchas, p.tentativas = 2, {"nair": 1}
    p.conchas_coletadas.add("concha_1_1")
    p.salvar()
    q = Progresso(arq)
    q.carregar()
    assert q.conchas == 2 and q.tentativas == {"nair": 1} and "concha_1_1" in q.conchas_coletadas


def test_um_chefe_por_regiao_perto_da_passagem(mapa):
    chefes = [n for n in mapa.dados["npcs"] if n.get("papel") == "chefe"]
    assert sorted(n["fase"] for n in chefes) == [1, 2, 3]
    chefoes = json.loads((DATA / "chefoes.json").read_text(encoding="utf-8"))
    assert all(n["id"] in chefoes for n in chefes)


def test_progresso_guarda_chefoes(tmp_path):
    p = Progresso(tmp_path / "s.json")
    p.bosses.update({"boss_1", "final"})
    p.salvar()
    q = Progresso(tmp_path / "s.json")
    q.carregar()
    assert q.bosses == {"boss_1", "final"}
