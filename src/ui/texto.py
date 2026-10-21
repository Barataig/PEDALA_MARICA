"""Quebra de texto em linhas (aceita qualquer objeto com .size(str) -> (w, h))."""


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
