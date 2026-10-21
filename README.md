# Pedala, Maricá! 🚲

RPG educativo de exploração e perguntas sobre a história, a natureza e a cultura de **Maricá (RJ)**.
Feito em **Python + Pygame CE** para o Hackathon.

## 1. Problema e solução

**Problema:** conteúdo sobre a história e a cultura local costuma chegar aos jovens de forma seca (texto, prova,
slide), e por isso o morador de Maricá, em especial o estudante, conhece pouco do próprio território.

**Solução:** um jogo de exploração em grade, estilo "Pokémon FireRed", em que o jogador pedala pelo mapa de Maricá
e aprende conversando com moradores (NPCs guias), lendo placas e enfrentando chefões temáticos.

**Como o jogo funciona**
- Seu Zeca pede que você reacenda o Farol de Ponta Negra.
- São 3 regiões (Ponta Negra, Lagoas e Costões, Centro), com 5 guias por região. Cada guia faz 1 pergunta.
- Com **3 ou mais acertos em 5**, libera-se o **chefão** da região. Com menos, a fase recomeça e os guias trocam de pergunta.
- Vencer o chefão dá o **Selo** e abre a passagem. Com os 3 selos, o Farol final propõe uma caça ao lugar contra o relógio.
- Toda resposta vem com **explicação** e **fonte**. Placas e pedras dão curiosidades, que ficam no caderno.
- Pontuação: 100 pts por acerto, +50 por fase perfeita (máx. 550 por fase, 1650 no total). Vale o melhor recorde de cada fase.

| Região | Chefão | Dinâmica |
|---|---|---|
| Ponta Negra | Guardião da Memória | Linha do tempo: ordenar fatos do mais antigo ao mais novo |
| Lagoas e Costões | Senhora das Lagoas | Ligar pares: lugar + fato que combina |
| Centro | Boitatá | Mito ou verdade (8 frases) |
| Farol | A Ressaca | Caça ao lugar: 3 pistas pelo mapa contra o relógio (use a bicicleta) |

## 2. Arquitetura

A lógica de regras fica separada do desenho. Pontuação, progresso e desafios rodam sem Pygame e são testados.

```
main.py                ponto de entrada (assíncrono, preparado para Pygbag)
src/
  core/                configuração, carga de recursos, câmera, entrada, ciclo do jogo
  world/               mapa, colisão, autotile do terreno, catálogo de objetos
  entities/            jogador e NPCs
  scenes/              cena do mundo (orquestra tudo)
  systems/             pontuação, perguntas, progresso (save), desafios dos chefões
  ui/                  caixas de texto, conversa e telas de desafio
data/                  perguntas.json, chefoes.json, historia.json, mapas/*.json
tools/gerar_mapa.py    gera data/mapas/marica.json (NPCs, placas, barreiras)
tests/                 55 testes automatizados (pytest)
docs/decisoes.md       decisões de projeto e pendências
```

**Decisões principais**
- Conteúdo em **JSON** (perguntas, chefões, história, mapas), então dá para editar sem mexer no código.
- Cada desafio de chefão é uma classe com a mesma interface, o que facilita criar dinâmicas novas.
- O progresso é salvo em `data/save.json` (fora do git).
- Mais detalhes em [`docs/decisoes.md`](docs/decisoes.md).

## 3. Tecnologias e IA usadas

**Tecnologias**
- Python 3 e [Pygame CE](https://pyga.me/)
- pytest para os testes
- Pygbag (publicação no navegador; ainda não testada)
- Git e GitHub

**Uso de IA**
- Ferramenta: **Claude (Anthropic)**, a única IA usada no projeto.
- Onde foi usada: _[PREENCHER: ex.: estrutura do código, testes, banco de perguntas, textos da história]_
- O que foi revisado por humanos: _[PREENCHER: ex.: revisão factual das perguntas e fontes, teste do jogo, ajuste do mapa]_

**Assets:** ver [`assets/CREDITOS.md`](assets/CREDITOS.md).

## 4. Como executar

Requisitos: Python 3.10+.

```bash
git clone <URL-DO-REPOSITORIO>
cd pedala-marica
python -m pip install -r requirements.txt
python main.py
```

**Controles:** setas/WASD andar · E, Espaço ou Enter falar/ler · C caderno · B bicicleta · H (na pergunta) usa uma
concha para eliminar uma resposta errada · F3 info · Esc sai.

Para recomeçar do zero, apague `data/save.json`.

**Testes**
```bash
python -m pytest
```

**Adicionar perguntas:** acrescente ao `data/perguntas.json` (mesmo formato), ponha o id em `EXTRAS` em
`tools/gerar_mapa.py` e rode `python tools/gerar_mapa.py`.

## 5. Divisão de tarefas — _[PREENCHER]_

| Integrante | Responsabilidade |
|---|---|
| _Nome 1_ | _ex.: mundo, mapa e colisão_ |
| _Nome 2_ | _ex.: perguntas, pontuação e conteúdo_ |
| _Nome 3_ | _ex.: chefões e interface_ |
| _Nome 4_ | _ex.: testes, README e publicação_ |

## 6. Limitações conhecidas
- Mapa e torre-farol são provisórios. A bicicleta ainda não tem sprite (só anda mais rápido).
- Terreno sem "cantos internos": formas côncavas mostram pequenas falhas nas quinas.
- Publicação no navegador (Pygbag) ainda não foi testada.
