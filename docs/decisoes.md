# Decisões do projeto

## Aprovadas
- Tecnologia: Python + Pygame CE (decisão do Prompt Mestre).
- Formato: RPG de exploração em grade, estilo FireRed (mudança em relação ao GDD v1.0, que era um quiz web).
- Visual: mundo Tiny Swords em tiles de 64 px + personagens Tiny Neighbours (16 px) ampliados 4x, sem suavização.
- Janela 960x640 (15x10 tiles).

## Regras confirmadas (GDD v1.0 = Prompt Mestre)
3 fases, 5 perguntas por fase, 100 pts/acerto, +50 fase perfeita (máx. 550/fase, 1650 total),
vale a melhor pontuação por fase, fase seguinte libera ao concluir a anterior, explicação em toda resposta.
Implementado e testado em `src/systems/pontuacao.py`.

## Decididas nesta rodada (revise!)
- Fases: F1 = hist_002,003,004 + patr_003,004 · F2 = pers_001 + nat_002,003,004,005 · F3 = econ_001,002,004 + cult_002 + trad_001.
- 1 NPC guia por pergunta; 4 alternativas mantidas; bicicleta = modo rápido (B).
- As 12 perguntas restantes viraram reservas: cada guia (12 deles) tem uma 2ª pergunta e, a cada nova tentativa, usa a próxima.
- Regra nova (pedido do dono): só passa de região com >= 3 acertos de 5 (`MINIMO_ACERTOS`). Menos que isso: a fase recomeça, o recorde fica. Substitui a regra do GDD "libera ao concluir".
- Conchas (15 na areia + 6 de presente): H na pergunta elimina 1 alternativa errada. Tecla C abre o caderno.
- O mapa mantém 3 fases e 3 passagens de progressão, mas organiza visualmente quatro bairros: Ponta Negra, Araçatiba, Espraiado e Centro. A representação é adaptada à grade do jogo, não um mapa geograficamente preciso.
- Revestimentos visuais do mapa usam calçada de pedra em Araçatiba e no Centro, trilha sinuosa em Espraiado e textura de terreno elevado nas encostas. Mar e lagoa têm texturas próprias; essas camadas não alteram colisões.

- Chefões (pedido do dono): um por região, cada um com uma dinâmica diferente; precisam de >= 3 acertos nos guias para serem enfrentados. O selo e a passagem agora saem ao vencer o chefão. O Farol final é a caça ao lugar (110 s).

## Pendentes
1. Quais 15 das 27 perguntas entram e em qual fase (nenhuma tem campo `fase`).
2. Alternativas por pergunta: o GDD diz 3/3/5; o banco tem 4 em todas.
3. Como as perguntas aparecem no mundo (NPC treinador? 1 NPC por pergunta?) e papel da bicicleta.
4. Licenças dos packs (ver assets/CREDITOS.md).
5. Revisão factual das perguntas e fontes (GDD exige 2ª pessoa revisando).
6. Ranking: começar local; remoto depois.
