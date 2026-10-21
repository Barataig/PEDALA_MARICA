"""Gera data/mapas/marica.json (mapa grande, 3 regiões, NPCs, placas). Rode: python tools/gerar_mapa.py
Para mudar o mapa, edite aqui (ou o JSON gerado) e rode de novo."""
import json
import random
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from src.world.mapa import Mapa  # noqa: E402  (valida o resultado)

W, H = 64, 34
g = [["A"] * W for _ in range(H)]
for r in range(3, 31):
    for c in range(2, 62):
        g[r][c] = "G"


def agua(c0, c1, r0, r1):
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            g[r][c] = "A"


for c0 in (19, 43):                       # canais com travessias controladas na linha central
    agua(c0, c0 + 4, 0, 14)
    agua(c0, c0 + 4, 19, 33)
contorno_lagoa = {
    7: (30, 35), 8: (28, 37), 9: (27, 38), 10: (27, 39),
    11: (26, 39), 12: (26, 39), 13: (26, 39), 14: (27, 39),
    15: (27, 38), 16: (28, 38), 17: (28, 37), 18: (29, 36),
    19: (31, 35),
}
for r, (c0, c1) in contorno_lagoa.items():
    agua(c0, c1, r, r)


def trilha(pontos):
    """Marca caminhos de areia entre pontos, sem cobrir água ou canais."""
    celulas = set()

    def marcar(c, r):
        if g[r][c] == "G":
            g[r][c] = "S"
        if g[r][c] == "S":
            celulas.add((c, r))

    for (c0, r0), (c1, r1) in zip(pontos, pontos[1:]):
        while c0 != c1:
            marcar(c0, r0)
            c0 += 1 if c1 > c0 else -1
        while r0 != r1:
            marcar(c0, r0)
            r0 += 1 if r1 > r0 else -1
        marcar(c1, r1)
    return celulas


# Travessia principal e caminhos locais: a lagoa é contornada pelo sul.
trilha([(3, 17), (18, 17), (24, 17), (24, 22), (41, 22), (41, 17), (61, 17)])
trilha([(9, 19), (10, 17), (10, 12), (14, 9), (14, 5)])
trilha([(4, 11), (7, 11), (7, 17)])
orla = trilha([(25, 8), (25, 21), (27, 22), (39, 22), (41, 20), (41, 8)])
trilha_espraiado = trilha([(34, 27), (36, 24), (36, 21), (39, 19), (40, 17), (40, 13), (37, 10), (37, 6)])
ruas_centro = set()
for r in (10, 16, 23):
    ruas_centro.update(trilha([(48, r), (61, r)]))
for c in (49, 55, 60):
    ruas_centro.update(trilha([(c, 5), (c, 29)]))
morros_espraiado = {
    (c, r)
    for c, r in (
        (35, 4), (36, 4), (37, 4), (38, 4),
        (34, 5), (35, 5), (36, 5), (37, 5),
        (40, 7), (41, 7), (40, 8),
        (35, 25), (36, 25), (37, 25),
        (34, 26), (35, 26), (36, 26), (37, 26), (38, 26),
        (35, 27), (36, 27), (37, 27),
        (40, 28), (41, 28), (40, 29),
    )
}

costa = [(r, c) for r in range(H) for c in range(W) if g[r][c] == "G" and any(
    not (0 <= r + dr < H and 0 <= c + dc < W) or g[r + dr][c + dc] == "A"
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
for r, c in costa:
    g[r][c] = "S"

NPCS = [
    ("zeca", "Seu Zeca", "NPC_3.png", 0, 9, 17, "direita", 0, None, "", "mentor"),
    # Fase 1 - Ponta Negra
    ("nair", "Dona Nair", "NPC_1.png", 0, 5, 12, "baixo", 1, "hist_002", "Eu guardo a memória do povoado. Vamos ver se você sabe como tudo começou?"),
    ("marta", "Profa. Marta", "NPC_2.png", 1, 14, 8, "esquerda", 1, "hist_003", "Dou aula sobre o nome da nossa terra. Uma perguntinha pra você!"),
    ("beto", "Seu Beto", "NPC_4.png", 2, 13, 24, "cima", 1, "hist_004", "Maricá já foi só uma freguesia, sabia? Me diga o que você sabe da vila."),
    ("cleide", "Tia Cleide", "NPC_5.png", 0, 6, 27, "direita", 1, "patr_003", "Já viu a capela de Ponta Negra? Tem um jeitão bem diferente!"),
    ("davi", "Davi", "NPC_6.png", 1, 16, 18, "esquerda", 1, "patr_004", "Eu moro pertinho do farol! Aposto que você não sabe a data dele."),
    # Fase 2 - Lagoas e Costões
    ("tati", "Guia Tati", "NPC_8.png", 0, 25, 10, "baixo", 2, "pers_001", "Um visitante ilustre passou por aqui anotando tudo sobre a natureza. Lembra quem?"),
    ("rui", "Biólogo Rui", "NPC_9.png", 1, 31, 5, "baixo", 2, "nat_004", "Essas águas salobras são o coração da cidade. Você conhece o conjunto?"),
    ("ana", "Geóloga Ana", "NPC_10.png", 2, 40, 9, "esquerda", 2, "nat_002", "As rochas do costão são das mais antigas que existem. Chute a idade!"),
    ("jorge", "Pescador Jorge", "NPC_11.png", 0, 30, 26, "cima", 2, "nat_003", "Na praia tem pedra que parece feita de areia colada. Sabe o nome?"),
    ("zefa", "Dona Zefa", "NPC_12.png", 1, 38, 25, "esquerda", 2, "nat_005", "Estão lutando pra proteger essas pedras todas. Sabe qual é o projeto?"),
    # Fase 3 - Centro e Farol
    ("lu", "Lu, comerciante", "NPC_13.png", 0, 50, 8, "baixo", 3, "econ_001", "Aqui na loja a gente aceita a moeda da cidade. Sabe de onde vem o nome dela?"),
    ("wellington", "Wellington", "NPC_14.png", 1, 55, 6, "baixo", 3, "econ_004", "Eu dirijo um ônibus que não cobra passagem! Sabe como chamam eles?"),
    ("vera", "Contadora Vera", "NPC_15.png", 2, 52, 20, "direita", 3, "econ_002", "Faço as contas da moeda social. Quanto vale cada uma?"),
    ("maria", "Vovó Maria", "NPC_1.png", 2, 58, 22, "esquerda", 3, "cult_002", "Meu marido pescava na lagoa. A cidade ganhou um título por causa disso!"),
    ("caca", "Mestre Cacá", "NPC_5.png", 2, 49, 26, "cima", 3, "trad_001", "Aprendi com os antigos o ofício de marcar a areia. Sabe pra que servia?"),
]
# perguntas reserva: a cada nova tentativa o guia usa a próxima (use ids do seu banco)
EXTRAS = {"nair": ["hist_001"], "marta": ["hist_006"], "beto": ["hist_005"], "cleide": ["patr_001"],
          "davi": ["patr_002"], "tati": ["pers_002"], "rui": ["nat_001"], "zefa": ["trad_004"],
          "lu": ["econ_003"], "maria": ["cult_001"], "caca": ["trad_002"], "wellington": ["trad_003"]}
# NPCs só de conversa: dão história, dicas e 1 concha de presente
CONVERSA = [
    {"id": "dalva", "nome": "Dalva", "folha": "NPC_2.png", "tom": 2, "col": 8, "linha": 13, "dir": "baixo", "falas": [
        "Sou de Ponta Negra de berço. Aqui o povo diz que o farol guia quem vem do mar.",
        "Dica de pedaleira: as placas e as pedras guardam curiosidades. Quem lê, acerta mais!"]},
    {"id": "tonho", "nome": "Seu Tonho", "folha": "NPC_7.png", "tom": 0, "col": 11, "linha": 21, "dir": "esquerda", "falas": [
        "Pedra que parece areia colada é coisa antiga: o mar já esteve mais baixo por aqui.",
        "Se errar uma pergunta, não desanima. Pra passar de região você precisa acertar pelo menos 3 de 5."]},
    {"id": "bia", "nome": "Bia, ciclista", "folha": "NPC_12.png", "tom": 0, "col": 26, "linha": 5, "dir": "baixo", "falas": [
        "Eu vivo pedalando pelas lagoas. Esse sistema lagunar é um dos maiores complexos de águas salobras do estado.",
        "Procure conchas na areia! Cada uma vale uma ajuda nas perguntas."]},
    {"id": "gil", "nome": "Gil, pesquisador", "folha": "NPC_4.png", "tom": 0, "col": 35, "linha": 22, "dir": "cima", "falas": [
        "Eu estudo o Geoparque Costões e Lagunas. A ideia é proteger e mostrar as rochas e paisagens da região.",
        "Se um guia falar de rochas ou de Darwin, escute com atenção!"]},
    {"id": "rita", "nome": "Dona Rita", "folha": "NPC_9.png", "tom": 2, "col": 54, "linha": 10, "dir": "baixo", "falas": [
        "No Centro o povo cuida do povo: a cidade tem moeda social e ônibus sem tarifa.",
        "Olha o prédio do museu ali: já foi cadeia, no tempo colonial!"]},
    {"id": "tiao", "nome": "Seu Tião", "folha": "NPC_10.png", "tom": 1, "col": 51, "linha": 15, "dir": "direita", "falas": [
        "Já ouvi muita lenda por aqui: Boitatá, lobisomem em noite de lua cheia...",
        "Dizem que tem tesouro escondido na Pedra de Itaocaia. Vai ver é só história de pescador!"]},
]
for n in CONVERSA:
    n.update(papel="conversa", fase=0)
# chefões: um por região (a dinâmica de cada um está em data/chefoes.json)
BOSSES = [
    {"id": "boss_1", "nome": "Guardião da Memória", "folha": "NPC_14.png", "tom": 2, "col": 20, "linha": 17, "dir": "direita", "fase": 1},
    {"id": "boss_2", "nome": "Senhora das Lagoas", "folha": "NPC_15.png", "tom": 1, "col": 44, "linha": 17, "dir": "direita", "fase": 2},
    {"id": "boss_3", "nome": "Boitatá", "folha": "NPC_13.png", "tom": 2, "col": 56, "linha": 14, "dir": "baixo", "fase": 3},
]
for n in BOSSES:
    n["papel"] = "chefe"

POIS = [
    {"id": "placa_tupis", "col": 11, "linha": 16, "titulo": "Placa: Primeiros moradores", "curiosidade": True,
     "texto": "Antes dos portugueses, povos tupis já ocupavam o litoral de Maricá, por volta do século XI."},
    {"id": "quilombo", "col": 14, "linha": 27, "titulo": "Pedra do Quilombo", "curiosidade": True,
     "texto": "Escravizados fugitivos formaram o Quilombo de Maricá nas matas, por volta de 1812. Foi um reduto de resistência."},
    {"id": "portao1", "col": 18, "linha": 16, "titulo": "Placa: Passagem", "fase": 1,
     "texto": "Mata fechada! A passagem para as Lagoas só abre com o Selo das Raízes. Fale com os 5 guias de Ponta Negra.",
     "texto_ok": "A passagem está aberta. Siga para leste, rumo às Lagoas e Costões!"},
    {"id": "canal", "col": 29, "linha": 24, "titulo": "Pedra do Canal", "curiosidade": True,
     "texto": "O Canal de Ponta Negra foi escavado em 1951 para ligar o sistema lagunar ao mar, renovar as águas e aliviar enchentes."},
    {"id": "itaocaia", "col": 34, "linha": 28, "titulo": "Pedra de Itaocaia", "curiosidade": True,
     "texto": "Dizem que guardiões invisíveis protegem um tesouro escondido na pedra de Itaocaia. Lenda ou verdade? Ninguém sabe."},
    {"id": "portao2", "col": 42, "linha": 16, "titulo": "Placa: Passagem", "fase": 2,
     "texto": "Mata fechada! O caminho do Centro só abre com o Selo das Águas. Fale com os 5 guias das Lagoas.",
     "texto_ok": "A passagem está aberta. O Centro e o Farol ficam a leste!"},
    {"id": "museu", "col": 52, "linha": 12, "titulo": "Casa de Cultura", "curiosidade": True,
     "texto": "O prédio do Museu Histórico já foi a Casa de Câmara e Cadeia, no tempo colonial."},
    {"id": "museu", "col": 53, "linha": 12, "titulo": "Casa de Cultura", "curiosidade": True,
     "texto": "O prédio do Museu Histórico já foi a Casa de Câmara e Cadeia, no tempo colonial."},
    {"id": "colonia", "col": 53, "linha": 25, "titulo": "Pedra da Colônia", "curiosidade": True,
     "texto": "Os pescadores artesanais de Maricá se organizam na Colônia de Pescadores Z-7 para defender sua tradição."},
    {"id": "lagoa", "col": 25, "linha": 12, "titulo": "Lagoa de Maricá", "curiosidade": True,
     "texto": "O Sistema Lagunar Maricá-Guarapina reúne as lagoas Brava, de Maricá, da Barra, do Padre e Guarapina: águas salobras, entre o rio e o mar."},
    {"id": "mar_ponta", "col": 8, "linha": 31, "titulo": "O mar de Ponta Negra", "curiosidade": True,
     "texto": "Do alto do promontório de Ponta Negra, onde fica o farol, se avista a curvatura da Terra."},
    {"id": "mar_leste", "col": 62, "linha": 15, "titulo": "Mar do Centro", "curiosidade": True,
     "texto": "Maricá é reconhecida como Capital Estadual da Pesca Artesanal. A tradição dos pescadores segue viva."},
    {"id": "farol", "col": 14, "linha": 7, "titulo": "Farol de Ponta Negra", "farol": True},
    {"id": "farol", "col": 15, "linha": 7, "titulo": "Farol de Ponta Negra", "farol": True},
]
objetos = [("casa_palha_1", 4, 9), ("casa_palha_2", 8, 9), ("casa_palha_1", 4, 22), ("casa_palha_2", 10, 23),
           ("casa_palha_1", 52, 12), ("casa_palha_2", 55, 17), ("torre_azul", 14, 7),
           ("casa_palha_1", 24, 23), ("casa_palha_2", 48, 7), ("casa_palha_1", 58, 26),
           ("casa_palha_1", 57, 12), ("casa_palha_2", 59, 12), ("casa_palha_1", 40, 26),
           ("pedra_1", 2, 5), ("pedra_2", 3, 5), ("pedra_3", 4, 5), ("pedra_1", 3, 6),
           ("pedra_2", 14, 27), ("pedra_1", 29, 24), ("pedra_3", 34, 28), ("pedra_2", 53, 25),
           ("placa_seta", 11, 16), ("placa_seta", 18, 16), ("placa_seta", 42, 16)]
pedras = ["pedra_1", "pedra_2", "pedra_3"]
barreiras = [{"tipo": pedras[i % 3], "col": c, "linha": 15 + i, "libera_fase": f}
             for f, c in ((1, 21), (2, 45)) for i in range(4)]
ocupado = {(o[1], o[2]) for o in objetos} | {(c + 1, l) for t, c, l in objetos if t.startswith(("casa", "torre"))}
ocupado |= {(b["col"], b["linha"]) for b in barreiras}
perto = [(n[4], n[5]) for n in NPCS] + [(p["col"], p["linha"]) for p in POIS] + [(9, 19)] + [(n["col"], n["linha"]) for n in CONVERSA + BOSSES]
rng = random.Random(7)
faixas_objetos = ((2, 20, 16), (24, 33, 17), (34, 42, 18), (48, 61, 24))
for regiao, (ini, fim, quantidade) in enumerate(faixas_objetos):
    livres = [(c, r) for r in range(3, 31) for c in range(ini, fim + 1)
              if g[r][c] == "G" and (c, r) not in ocupado
              and (c + 1, r) not in ocupado and all(abs(c - a) + abs(r - b) > 2 for a, b in perto)]
    rng.shuffle(livres)
    for i, (c, r) in enumerate(livres[:quantidade]):
        arbusto = rng.choice(["arbusto_1", "arbusto_2", "arbusto_3"])
        tipo = (rng.choice(pedras) if regiao in (0, 2) and i % 2 == 0
                else rng.choice(pedras) if regiao == 1 and i % 4 == 0
                else rng.choice(pedras) if regiao == 3 and i % 5 == 0
                else arbusto)
        objetos.append((tipo, c, r))
        ocupado.add((c, r))

celulas_bloqueadas = ocupado | {(n[4], n[5]) for n in NPCS}
celulas_bloqueadas |= {(n["col"], n["linha"]) for n in CONVERSA + BOSSES}

dados = {
    "nome": "Maricá (protótipo)",
    "linhas": ["".join(l) for l in g],
    "inicio": [9, 19],
    "zonas": [{"nome": "Ponta Negra", "col_ini": 0, "col_fim": 21},
              {"nome": "Araçatiba", "col_ini": 22, "col_fim": 33},
              {"nome": "Espraiado", "col_ini": 34, "col_fim": 45},
              {"nome": "Centro", "col_ini": 46, "col_fim": 63}],
    "agua_laguna": [{"col": c, "linha": r}
                    for r in range(7, 20) for c in range(26, 40) if g[r][c] == "A"],
    "revestimentos": (
        [{"tipo": "morro_verde", "col": c, "linha": r}
         for c, r in sorted(morros_espraiado) if (c, r) not in celulas_bloqueadas]
        + [{"tipo": "calcada_pedra", "col": c, "linha": r}
         for c, r in sorted(orla) if 22 <= c <= 33 and (c, r) not in celulas_bloqueadas]
        + [{"tipo": "trilha_terra", "col": c, "linha": r}
           for c, r in sorted(trilha_espraiado) if 34 <= c <= 45 and (c, r) not in celulas_bloqueadas]
        + [{"tipo": "calcada_pedra", "col": c, "linha": r}
           for c, r in sorted(ruas_centro) if (c, r) not in celulas_bloqueadas]
    ),
    "objetos": [{"tipo": t, "col": c, "linha": l} for t, c, l in objetos] + barreiras,
    "npcs": [dict(zip(("id", "nome", "folha", "tom", "col", "linha", "dir", "fase", "pergunta", "fala", "papel"),
                      n + ("guia",) * (11 - len(n)))) for n in NPCS],
    "pois": POIS,
}
for n in dados["npcs"]:
    if n["id"] in EXTRAS:
        n["extras"] = EXTRAS[n["id"]]
dados["npcs"] += CONVERSA + BOSSES
m = Mapa.de_dict(dados)    # levanta ErroMapa se algo estiver sobreposto/na água
for f in (1, 2, 3):
    m.liberar(f)
bloq = {(n["col"], n["linha"]) for n in dados["npcs"]}
visto, fila = {m.inicio}, [m.inicio]
while fila:
    c, l = fila.pop()
    for dc, dl in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        q = (c + dc, l + dl)
        if q not in visto and q not in bloq and m.caminhavel(*q):
            visto.add(q)
            fila.append(q)
proibidos = {(p["col"], p["linha"]) for p in POIS} | bloq | {m.inicio}
areia = [q for q in sorted(visto) if m.terreno(*q) == "S" and q not in proibidos]
conchas = []
for k, (ini, fim) in enumerate(((0, 21), (22, 45), (46, 63))):    # 5 conchas por fase
    cand = [q for q in areia if ini <= q[0] <= fim and not (19 <= q[0] <= 23 or 43 <= q[0] <= 47)]
    rng.shuffle(cand)
    conchas += [{"id": f"concha_{k + 1}_{i + 1}", "col": c, "linha": l} for i, (c, l) in enumerate(cand[:5])]
dados["conchas"] = conchas
destino = RAIZ / "data" / "mapas" / "marica.json"
destino.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
print("gerado:", destino, f"({W}x{H}, {len(objetos)} objetos, {len(NPCS)} NPCs)")
