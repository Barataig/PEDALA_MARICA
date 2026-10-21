"""Caixa de conversa: falas com efeito de digitação e telas de escolha/pergunta.

Itens da fila (dicts):
  {"tipo": "fala", "nome": str, "texto": str}
  {"tipo": "escolha", "nome": str, "texto": str, "opcoes": [str],
   "correta": int | None, "explicacao": str, "fonte": str, "ao_escolher": fn(indice)}
Com "correta" definido a tela mostra acerto/erro + explicação; com None só chama o callback.
"""
from collections import deque

import pygame

from src.ui.texto import quebrar

PAINEL, BORDA, DESTAQUE = (24, 41, 56), (247, 247, 242), (255, 200, 60)
VERDE, VERMELHO, ESCURO = (110, 200, 120), (235, 110, 100), (20, 20, 20)
CARACTERES_POR_SEGUNDO = 55
CONFIRMAR = (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE, pygame.K_e)


class Conversa:
    def __init__(self, fonte, fonte_pequena):
        self.f, self.fp = fonte, fonte_pequena
        self.fila, self.item, self.ao_fim = deque(), None, None
        self.t, self.sel, self.resultado, self._linhas = 0.0, 0, None, None
        self.ocultas = set()

    @property
    def ativa(self):
        return self.item is not None

    def iniciar(self, itens, ao_fim=None):
        self.fila, self.ao_fim = deque(itens), ao_fim
        self._proximo()

    def inserir(self, itens):
        """Coloca itens logo depois do atual (usado dentro de callbacks)."""
        self.fila.extendleft(reversed(list(itens)))

    def _proximo(self):
        if not self.fila:
            self.item = None
            cb, self.ao_fim = self.ao_fim, None
            if cb:
                cb()
            return
        self.item = self.fila.popleft()
        self.t, self.sel, self.resultado, self._linhas = 0.0, 0, None, None
        self.ocultas = set()

    def atualizar(self, dt):
        self.t += dt

    def evento(self, ev):
        if ev.type != pygame.KEYDOWN or not self.ativa:
            return
        ok, it = ev.key in CONFIRMAR, self.item
        if it["tipo"] == "fala":
            if ok:
                if int(self.t * CARACTERES_POR_SEGUNDO) < len(it["texto"]):
                    self.t = 1e9            # primeiro aperto completa o texto
                else:
                    self._proximo()
            return
        if self.resultado is not None:      # tela de feedback
            if ok:
                self._proximo()
            return
        n = len(it["opcoes"])
        if ev.key == pygame.K_h and it.get("ajuda"):
            i = it["ajuda"]()
            if i is not None:
                self.ocultas.add(i)
                if self.sel in self.ocultas:
                    self._mover(1)
        elif ev.key in (pygame.K_UP, pygame.K_w):
            self._mover(-1)
        elif ev.key in (pygame.K_DOWN, pygame.K_s):
            self._mover(1)
        elif pygame.K_1 <= ev.key < pygame.K_1 + n:
            self.sel = ev.key - pygame.K_1
            self._escolher()
        elif ok:
            self._escolher()

    def _mover(self, passo):
        n = len(self.item["opcoes"])
        for _ in range(n):
            self.sel = (self.sel + passo) % n
            if self.sel not in self.ocultas:
                break

    def _escolher(self):
        it = self.item
        if self.sel in self.ocultas:
            return
        if it.get("correta") is not None:
            self.resultado = (self.sel == it["correta"])
        if it.get("ao_escolher"):
            it["ao_escolher"](self.sel)
        if it.get("correta") is None:
            self._proximo()

    # ---------- desenho ----------
    def _painel(self, tela, rect):
        pygame.draw.rect(tela, PAINEL, rect, border_radius=10)
        pygame.draw.rect(tela, BORDA, rect, 3, border_radius=10)

    def _etiqueta(self, tela, nome, x, y):
        if nome:
            img = self.f.render(nome, True, ESCURO)
            pygame.draw.rect(tela, DESTAQUE, (x, y, img.get_width() + 24, 36), border_radius=8)
            tela.blit(img, (x + 10, y + 2))

    def _texto(self, tela, linhas, x, y, cor=BORDA, fonte=None, passo=28):
        fonte = fonte or self.f
        for l in linhas:
            tela.blit(fonte.render(l, True, cor), (x, y))
            y += passo
        return y

    def desenhar(self, tela):
        if not self.ativa:
            return
        (self._fala if self.item["tipo"] == "fala" else self._escolha)(tela, self.item)

    def _fala(self, tela, it):
        self._painel(tela, pygame.Rect(24, 456, 912, 164))
        self._etiqueta(tela, it.get("nome"), 44, 440)
        if self._linhas is None:
            self._linhas = quebrar(it["texto"], self.f, 860)
        restante = int(self.t * CARACTERES_POR_SEGUNDO)
        y = 472
        for l in self._linhas[:5]:
            tela.blit(self.f.render(l[:max(restante, 0)], True, BORDA), (48, y))
            restante -= len(l) + 1
            y += 28
        if restante > 0:    # terminou de digitar: setinha de "continuar"
            pygame.draw.polygon(tela, DESTAQUE, [(900, 592), (916, 592), (908, 604)])

    def _escolha(self, tela, it):
        self._painel(tela, pygame.Rect(24, 36, 912, 584))
        self._etiqueta(tela, it.get("nome"), 44, 14)
        y = self._texto(tela, quebrar(it["texto"], self.f, 860), 48, 62) + 10
        if self.resultado is None:
            for i, op in enumerate(it["opcoes"]):
                linhas = quebrar(f"{i + 1}. {op}", self.f, 820)
                h = 16 + 28 * len(linhas)
                caixa = pygame.Rect(48, y, 864, h)
                oculta = i in self.ocultas
                pygame.draw.rect(tela, (40, 66, 90) if i == self.sel else PAINEL, caixa, border_radius=8)
                pygame.draw.rect(tela, DESTAQUE if i == self.sel else (110, 130, 150), caixa, 3, border_radius=8)
                self._texto(tela, linhas, 62, y + 8, (80, 95, 110) if oculta else BORDA)
                y += h + 8
            dica = "Setas escolhem · Enter ou 1-9 responde"
            if it.get("rotulo"):
                dica += " · " + it["rotulo"]()
            self._texto(tela, [dica], 48, 590, (170, 185, 200), self.fp, 22)
            return
        cor = VERDE if self.resultado else VERMELHO
        y = self._texto(tela, ["Resposta certa!" if self.resultado else "Não foi dessa vez..."], 48, y + 6, cor)
        if not self.resultado:
            y = self._texto(tela, quebrar("Certo: " + it["opcoes"][it["correta"]], self.f, 860), 48, y + 6, VERDE)
        y = self._texto(tela, quebrar(it.get("explicacao", ""), self.fp, 860), 48, y + 12, BORDA, self.fp, 24)
        if it.get("fonte"):
            self._texto(tela, quebrar("Fonte: " + it["fonte"], self.fp, 860), 48, y + 10, (170, 185, 200), self.fp, 22)
        pygame.draw.polygon(tela, DESTAQUE, [(900, 592), (916, 592), (908, 604)])
