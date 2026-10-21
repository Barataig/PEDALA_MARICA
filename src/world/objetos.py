"""Catálogo de objetos do mapa. (coluna, linha) no mapa = tile do canto
inferior esquerdo da área ocupada (a 'base' que bloqueia a passagem)."""
from dataclasses import dataclass


@dataclass(frozen=True)
class DefObjeto:
    arquivo: str
    largura: int = 1        # tiles ocupados na horizontal
    profundidade: int = 1   # tiles ocupados (para cima) na base


CATALOGO = {
    "casa_palha_1": DefObjeto("mundo/casa_palha_1.png", 2),
    "casa_palha_2": DefObjeto("mundo/casa_palha_2.png", 2),
    "arbusto_1": DefObjeto("mundo/arbusto_1.png"),
    "arbusto_2": DefObjeto("mundo/arbusto_2.png"),
    "arbusto_3": DefObjeto("mundo/arbusto_3.png"),
    "pedra_1": DefObjeto("mundo/pedra_1.png"),
    "pedra_2": DefObjeto("mundo/pedra_2.png"),
    "pedra_3": DefObjeto("mundo/pedra_3.png"),
    "placa_seta": DefObjeto("mundo/placa_seta.png"),
    "torre_azul": DefObjeto("mundo/torre_azul.png", 2),  # PROVISÓRIO: faz o papel do farol
}
