"""Quebra de texto em linhas e carregamento de fontes com bom suporte tipográfico."""
import pygame


def carregar_fonte(tamanho, negrito=False):
    """Carrega fonte do sistema com bom kerning para português (acentos) ou fallback seguro."""
    preferencias = ["segoeui", "arial", "helvetica", "dejavusans", "sans-serif"]
    for nome in preferencias:
        try:
            f = pygame.font.SysFont(nome, tamanho, bold=negrito)
            if f:
                return f
        except Exception:
            pass
    return pygame.font.Font(None, tamanho)


def quebrar(texto, fonte, largura):
    linhas = []
    for paragrafo in texto.split("\n"):
        atual = ""
        for palavra in paragrafo.split():
            teste = f"{atual} {palavra}".strip()
            if not atual or fonte.size(teste)[0] <= largura:
                atual = teste
            else:
                linhas.append(atual)
                atual = palavra
        linhas.append(atual)
    return linhas
