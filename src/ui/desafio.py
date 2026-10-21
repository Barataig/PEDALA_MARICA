"""Tela dos desafios de chefão (desenha qualquer objeto de src/systems/desafios.py)."""
import pygame

from src.ui.conversa import BORDA, DESTAQUE, ESCURO, PAINEL, VERDE, VERMELHO, CONFIRMAR
from src.ui.texto import quebrar

CINZA = (170, 185, 200)


class DesafioUI:
    def __init__(self, fonte, fonte_pequena, desafio, ao_fim, nome=""):
        self.f, self.fp, self.d, self.ao_fim, self.nome = fonte, fonte_pequena, desafio, ao_fim, nome
        self.sel, self.msg, self.fim, self.ativo = 0, ("", True), False, True

    def evento(self, ev):
        if ev.type != pygame.KEYDOWN or not self.ativo:
            return
        ok = ev.key in CONFIRMAR
        if self.fim:
            if ok:
                self.ativo = False
                self.ao_fim(self.d.venceu)
            return
        n = len(self.d.opcoes())
        if ev.key in (pygame.K_UP, pygame.K_w):
            self.sel = (self.sel - 1) % n
        elif ev.key in (pygame.K_DOWN, pygame.K_s):
            self.sel = (self.sel + 1) % n
        elif pygame.K_1 <= ev.key < pygame.K_1 + n:
            self.sel = ev.key - pygame.K_1
            self._escolher()
        elif ok:
            self._escolher()

    def _escolher(self):
        acertou, msg = self.d.escolher(self.sel)
        if msg:
            self.msg = (msg, acertou)
        self.sel = 0
        self.fim = self.d.terminou

    def _linhas(self, tela, linhas, x, y, cor=BORDA, fonte=None, passo=28):
        fonte = fonte or self.f
        for l in linhas:
            tela.blit(fonte.render(l, True, cor), (x, y))
            y += passo
        return y

    def desenhar(self, tela):
        d = self.d
        pygame.draw.rect(tela, PAINEL, (24, 36, 912, 584), border_radius=10)
        pygame.draw.rect(tela, BORDA, (24, 36, 912, 584), 3, border_radius=10)
        etq = self.f.render(f"{self.nome}: {d.titulo}", True, ESCURO)
        pygame.draw.rect(tela, DESTAQUE, (44, 14, etq.get_width() + 24, 36), border_radius=8)
        tela.blit(etq, (56, 22))
        for i in range(d.vidas_max):                      # vidas
            pygame.draw.circle(tela, VERMELHO if i < d.vidas else (70, 70, 80), (880 - i * 28, 32), 10)
        y = self._linhas(tela, quebrar(d.prompt() if not self.fim else self._resultado(), self.f, 860), 48, 62) + 8
        if not self.fim:
            for i, op in enumerate(d.opcoes()):
                linhas = quebrar(f"{i + 1}. {op}", self.f, 820)
                h = 16 + 28 * len(linhas)
                caixa = pygame.Rect(48, y, 864, h)
                pygame.draw.rect(tela, (40, 66, 90) if i == self.sel else PAINEL, caixa, border_radius=8)
                pygame.draw.rect(tela, DESTAQUE if i == self.sel else (110, 130, 150), caixa, 3, border_radius=8)
                self._linhas(tela, linhas, 62, y + 8)
                y += h + 6
        if self.msg[0]:
            y = self._linhas(tela, quebrar(self.msg[0], self.fp, 860), 48, y + 6,
                             VERDE if self.msg[1] else VERMELHO, self.fp, 22)
        feitas = d.resolvidas()[-4:]
        self._linhas(tela, [quebrar("• " + t, self.fp, 860)[0] for t in feitas], 48, 520, CINZA, self.fp, 22)
        dica = "Enter para continuar" if self.fim else "Setas escolhem · Enter ou 1-9 responde"
        self._linhas(tela, [dica], 48, 596, CINZA, self.fp, 22)

    def _resultado(self):
        return "VITÓRIA! Você derrotou o chefão." if self.d.venceu else "DERROTA... as vidas acabaram. Tente de novo!"
