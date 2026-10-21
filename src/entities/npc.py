"""NPC parado que olha para o jogador ao conversar."""
from src.core.tipos import Direcao


class NPC:
    def __init__(self, id, nome, col, linha, folha, direcao=Direcao.BAIXO, fase=0,
                 pergunta=None, fala="", papel="guia", falas=(), extras=()):
        self.id, self.nome, self.col, self.linha = id, nome, col, linha
        self.folha, self.direcao, self.fase = folha, direcao, fase
        self.pergunta, self.fala, self.papel = pergunta, fala, papel
        self.falas, self.extras = list(falas), list(extras)   # falas: NPC de conversa; extras: perguntas reserva
        self.tempo_anim = 0.0

    def quadro(self):
        return self.folha.quadro(self.direcao, False, self.tempo_anim)

    def virar_para(self, col, linha):
        dx, dy = col - self.col, linha - self.linha
        if abs(dx) >= abs(dy):
            self.direcao = Direcao.DIREITA if dx > 0 else Direcao.ESQUERDA
        else:
            self.direcao = Direcao.BAIXO if dy > 0 else Direcao.CIMA
