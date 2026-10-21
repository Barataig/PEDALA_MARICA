"""Desafios dos chefões (lógica pura, sem pygame).

Todos seguem a mesma interface: prompt(), opcoes(), resolvidas(), escolher(i) -> (ok, mensagem),
progresso(), e os campos vidas, terminou, venceu. A tela só desenha isso.
"""
import random


class Desafio:
    def __init__(self, titulo, vidas=3):
        self.titulo, self.vidas, self.vidas_max = titulo, vidas, vidas
        self.terminou = self.venceu = False

    def _perder_vida(self):
        self.vidas -= 1
        if self.vidas <= 0:
            self.terminou = True

    def _vencer(self):
        self.terminou = self.venceu = True


class LinhaDoTempo(Desafio):
    """Cada rodada: escolher, um a um, o que aconteceu primeiro entre os cartões que sobram."""

    def __init__(self, titulo, rodadas, vidas=3, rng=None):
        super().__init__(titulo, vidas)
        self.rodadas, self.rng, self.r = rodadas, rng or random.Random(), -1
        self._proxima_rodada()

    def _proxima_rodada(self):
        self.r += 1
        self.restantes, self.colocadas = list(self.rodadas[self.r]), []
        certa = sorted(self.restantes, key=lambda c: c["chave"])
        for _ in range(20):                  # não deixa começar já na ordem certa
            self.rng.shuffle(self.restantes)
            if self.restantes != certa:
                break

    def prompt(self):
        return f"Rodada {self.r + 1}/{len(self.rodadas)}: qual destes aconteceu PRIMEIRO?"

    def opcoes(self):
        return [c["texto"] for c in self.restantes]

    def resolvidas(self):
        return [f"{c['rotulo']}: {c['texto']}" for c in self.colocadas]

    def progresso(self):
        return f"Rodada {self.r + 1}/{len(self.rodadas)}"

    def escolher(self, i):
        carta = self.restantes[i]
        if carta is min(self.restantes, key=lambda c: c["chave"]):
            self.restantes.remove(carta)
            self.colocadas.append(carta)
            if not self.restantes:
                if self.r + 1 >= len(self.rodadas):
                    self._vencer()
                else:
                    self._proxima_rodada()
            return True, f"Certo! {carta['rotulo']}."
        self._perder_vida()
        return False, f"Ainda não! \"{carta['texto']}\" veio depois de outro destes."


class LigarPares(Desafio):
    """Escolhe um item da esquerda e depois o fato que combina. Errou o par: perde vida."""

    def __init__(self, titulo, rodadas, vidas=3, rng=None):
        super().__init__(titulo, vidas)
        self.rodadas, self.rng, self.r = rodadas, rng or random.Random(), -1
        self._proxima_rodada()

    def _proxima_rodada(self):
        self.r += 1
        self.pares, self.feitos, self.sel = self.rodadas[self.r], [], None
        self.esq = [p["a"] for p in self.pares]
        self.dir = [p["b"] for p in self.pares]
        self.rng.shuffle(self.esq)
        self.rng.shuffle(self.dir)

    def prompt(self):
        if self.sel is None:
            return f"Rodada {self.r + 1}/{len(self.rodadas)}: escolha um item para ligar."
        return f"Agora escolha o que combina com: {self.sel}"

    def opcoes(self):
        return list(self.esq if self.sel is None else self.dir)

    def resolvidas(self):
        return self.feitos

    def progresso(self):
        return f"Rodada {self.r + 1}/{len(self.rodadas)}"

    def escolher(self, i):
        if self.sel is None:
            self.sel = self.esq[i]
            return True, ""
        a, b, self.sel = self.sel, self.dir[i], None
        if next(p for p in self.pares if p["a"] == a)["b"] == b:
            self.esq.remove(a)
            self.dir.remove(b)
            self.feitos.append(f"{a} = {b}")
            if not self.esq:
                if self.r + 1 >= len(self.rodadas):
                    self._vencer()
                else:
                    self._proxima_rodada()
            return True, "Combina!"
        self._perder_vida()
        return False, f"Não combina: isso não é sobre {a}."


class MitoVerdade(Desafio):
    def __init__(self, titulo, afirmacoes, vidas=3, rng=None):
        super().__init__(titulo, vidas)
        self.itens, self.i, self.feitos = list(afirmacoes), 0, []
        (rng or random.Random()).shuffle(self.itens)

    def prompt(self):
        return f"Frase {self.i + 1}/{len(self.itens)}: {self.itens[self.i]['texto']}"

    def opcoes(self):
        return ["Verdade", "Mito"]

    def resolvidas(self):
        return self.feitos

    def progresso(self):
        return f"Frase {self.i + 1}/{len(self.itens)}"

    def escolher(self, i):
        item = self.itens[self.i]
        ok = (i == 0) == item["verdade"]
        self.feitos.append(("Verdade: " if item["verdade"] else "Mito: ") + item["texto"])
        if not ok:
            self._perder_vida()
        self.i += 1
        if not self.terminou and self.i >= len(self.itens):
            self._vencer()
        return ok, ("Certo! " if ok else "Opa! ") + item["explicacao"]


_TIPOS = {"tempo": (LinhaDoTempo, "rodadas"), "pares": (LigarPares, "rodadas"), "mito": (MitoVerdade, "afirmacoes")}


def criar_desafio(cfg, rng=None):
    classe, campo = _TIPOS[cfg["tipo"]]
    return classe(cfg["titulo"], cfg[campo], cfg.get("vidas", 3), rng)
