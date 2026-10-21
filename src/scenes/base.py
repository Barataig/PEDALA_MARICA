"""Interface comum das cenas."""


class Cena:
    def __init__(self, jogo):
        self.jogo = jogo

    def processar_evento(self, ev):
        pass

    def atualizar(self, dt):
        pass

    def desenhar(self, tela):
        pass
