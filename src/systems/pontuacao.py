"""Regras de pontuação (GDD v1.0, seção 5.2). Independente de tela e de salvamento."""

PONTOS_POR_ACERTO = 100
BONUS_FASE_PERFEITA = 50
PERGUNTAS_POR_FASE = 5
TOTAL_FASES = 3
MINIMO_ACERTOS = 3          # acertos necessários (de 5) para liberar a próxima região
MAXIMO_FASE = PERGUNTAS_POR_FASE * PONTOS_POR_ACERTO + BONUS_FASE_PERFEITA   # 550
MAXIMO_TOTAL = MAXIMO_FASE * TOTAL_FASES                                     # 1650


def _inteiro(valor):
    return isinstance(valor, int) and not isinstance(valor, bool)


def pontos_da_fase(acertos):
    if not _inteiro(acertos) or not 0 <= acertos <= PERGUNTAS_POR_FASE:
        raise ValueError(f"acertos deve ser um inteiro de 0 a {PERGUNTAS_POR_FASE}, recebido: {acertos!r}")
    bonus = BONUS_FASE_PERFEITA if acertos == PERGUNTAS_POR_FASE else 0
    return acertos * PONTOS_POR_ACERTO + bonus


class PlacarFases:
    """Guarda a MELHOR pontuação de cada fase e quais fases foram concluídas."""

    def __init__(self, melhores=None, concluidas=None):
        self._melhores = list(melhores) if melhores is not None else [0] * TOTAL_FASES
        self._concluidas = list(concluidas) if concluidas is not None else [False] * TOTAL_FASES
        if len(self._melhores) != TOTAL_FASES or len(self._concluidas) != TOTAL_FASES:
            raise ValueError(f"o placar precisa ter {TOTAL_FASES} fases")
        if any(not _inteiro(p) or not 0 <= p <= MAXIMO_FASE for p in self._melhores):
            raise ValueError(f"pontuação de fase deve estar entre 0 e {MAXIMO_FASE}")

    def dados(self):
        return list(self._melhores), list(self._concluidas)

    @staticmethod
    def _indice(fase):
        if not _inteiro(fase) or not 1 <= fase <= TOTAL_FASES:
            raise ValueError(f"fase deve ser de 1 a {TOTAL_FASES}, recebido: {fase!r}")
        return fase - 1

    def registrar(self, fase, acertos):
        """Registra uma tentativa. Só substitui se for maior. Devolve True se melhorou."""
        i, pontos = self._indice(fase), pontos_da_fase(acertos)
        self._concluidas[i] = True
        if pontos > self._melhores[i]:
            self._melhores[i] = pontos
            return True
        return False

    def melhor(self, fase):
        return self._melhores[self._indice(fase)]

    def concluida(self, fase):
        return self._concluidas[self._indice(fase)]

    def aprovada(self, fase):
        """Já fez pelo menos MINIMO_ACERTOS acertos nessa fase (em alguma tentativa)."""
        return self.melhor(fase) >= MINIMO_ACERTOS * PONTOS_POR_ACERTO

    def liberada(self, fase):
        """Fase liberada só quando a anterior foi aprovada (>= MINIMO_ACERTOS)."""
        return fase == 1 or self.aprovada(fase - 1)

    @property
    def total(self):
        return sum(self._melhores)
