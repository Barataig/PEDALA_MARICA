"""Dados do mapa: terreno, objetos e colisão (sem desenho)."""
from __future__ import annotations

import json
from dataclasses import dataclass

from src.core.config import TILE
from src.world.objetos import CATALOGO

VALIDOS = {"A", "S", "G"}      # Água, Areia, Grama
CAMINHAVEIS = {"S", "G"}


class ErroMapa(ValueError):
    pass


@dataclass(frozen=True)
class ObjetoMapa:
    tipo: str
    col: int
    linha: int
    libera_fase: int = 0     # >0: barreira que some ao concluir essa fase

    def celulas(self):
        d = CATALOGO[self.tipo]
        return [(self.col + i, self.linha - j)
                for j in range(d.profundidade) for i in range(d.largura)]


class Mapa:
    def __init__(self, nome, linhas, inicio, objetos=()):
        self.nome, self.linhas = nome, list(linhas)
        if not self.linhas or any(len(l) != len(self.linhas[0]) for l in self.linhas):
            raise ErroMapa(f"[{nome}] todas as linhas do mapa precisam ter o mesmo tamanho.")
        for y, l in enumerate(self.linhas):
            for x, c in enumerate(l):
                if c not in VALIDOS:
                    raise ErroMapa(f"[{nome}] terreno inválido '{c}' (linha {y}, coluna {x}). Use A, S ou G.")
        self.largura, self.altura = len(self.linhas[0]), len(self.linhas)
        self.dados = {}          # JSON original (npcs, pois, zonas...)
        self.objetos, self._ocupadas = list(objetos), set()
        for o in self.objetos:
            if o.tipo not in CATALOGO:
                raise ErroMapa(f"[{nome}] objeto desconhecido: '{o.tipo}'.")
            for cel in o.celulas():
                if self.terreno(*cel) not in CAMINHAVEIS:
                    raise ErroMapa(f"[{nome}] '{o.tipo}' em {cel} está fora do mapa ou sobre a água.")
                if cel in self._ocupadas:
                    raise ErroMapa(f"[{nome}] '{o.tipo}' em {cel} sobrepõe outro objeto.")
                self._ocupadas.add(cel)
        self.inicio = tuple(inicio)
        if not self.caminhavel(*self.inicio):
            raise ErroMapa(f"[{nome}] a posição inicial {self.inicio} não é caminhável.")

    @property
    def largura_px(self):
        return self.largura * TILE

    @property
    def altura_px(self):
        return self.altura * TILE

    def terreno(self, col, linha):
        if 0 <= linha < self.altura and 0 <= col < self.largura:
            return self.linhas[linha][col]
        return None

    def caminhavel(self, col, linha):
        return self.terreno(col, linha) in CAMINHAVEIS and (col, linha) not in self._ocupadas

    def liberar(self, fase):
        """Remove as barreiras ligadas à fase. Devolve True se algo abriu."""
        saem = [o for o in self.objetos if o.libera_fase == fase]
        for o in saem:
            self._ocupadas.difference_update(o.celulas())
        self.objetos = [o for o in self.objetos if o.libera_fase != fase]
        return bool(saem)

    @classmethod
    def de_dict(cls, dados):
        try:
            objs = [ObjetoMapa(o["tipo"], o["col"], o["linha"], o.get("libera_fase", 0)) for o in dados.get("objetos", [])]
            mapa = cls(dados["nome"], dados["linhas"], dados["inicio"], objs)
            mapa.dados = dados
            return mapa
        except KeyError as e:
            raise ErroMapa(f"Campo ausente no mapa: {e}") from e

    @classmethod
    def carregar(cls, caminho):
        try:
            with open(caminho, encoding="utf-8") as f:
                return cls.de_dict(json.load(f))
        except FileNotFoundError as e:
            raise ErroMapa(f"Arquivo de mapa não encontrado: {caminho}") from e
        except json.JSONDecodeError as e:
            raise ErroMapa(f"Mapa com JSON inválido ({caminho}): {e}") from e
