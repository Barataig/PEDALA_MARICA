"""Câmera que segue o jogador sem sair do mapa."""


class Camera:
    def __init__(self, largura_tela, altura_tela, largura_mundo, altura_mundo):
        self.lt, self.at = largura_tela, altura_tela
        self.lm, self.am = largura_mundo, altura_mundo
        self.x = self.y = 0

    @staticmethod
    def _limitar(valor, tela, mundo):
        if mundo <= tela:
            return (mundo - tela) / 2
        return max(0, min(valor, mundo - tela))

    def seguir(self, cx, cy):
        self.x = round(self._limitar(cx - self.lt / 2, self.lt, self.lm))
        self.y = round(self._limitar(cy - self.at / 2, self.at, self.am))
