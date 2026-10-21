"""Banco de perguntas (data/perguntas.json) e validação."""
import json
from dataclasses import dataclass


class ErroPerguntas(ValueError):
    pass


@dataclass(frozen=True)
class Pergunta:
    id: str
    categoria: str
    dificuldade: str
    texto: str
    alternativas: tuple
    correta: int
    explicacao: str
    fonte_titulo: str
    fonte_url: str


def carregar_perguntas(caminho):
    try:
        with open(caminho, encoding="utf-8") as f:
            bruto = json.load(f)
    except FileNotFoundError as e:
        raise ErroPerguntas(f"Banco de perguntas não encontrado: {caminho}. "
                            "Copie o seu JSON de perguntas para data/perguntas.json.") from e
    except json.JSONDecodeError as e:
        raise ErroPerguntas(f"JSON de perguntas inválido: {e}") from e
    banco = {}
    for q in bruto:
        try:
            alts = tuple(q["alternativas"])
            p = Pergunta(q["id"], q.get("categoria", ""), q.get("dificuldade", ""), q["pergunta"], alts,
                         q["resposta_correta"], q["explicacao"],
                         q.get("fonte", {}).get("titulo", ""), q.get("fonte", {}).get("url", ""))
        except KeyError as e:
            raise ErroPerguntas(f"Pergunta {q.get('id', '?')} sem o campo {e}.") from e
        if len(alts) < 2 or not 0 <= p.correta < len(alts):
            raise ErroPerguntas(f"Pergunta {p.id}: alternativas ou resposta_correta inválidas.")
        if p.id in banco:
            raise ErroPerguntas(f"Id de pergunta repetido: {p.id}")
        banco[p.id] = p
    return banco


def verificar_npcs(npcs, banco):
    """Todo NPC com 'pergunta' precisa apontar para um id existente."""
    faltam = [f"{n['id']}->{q}" for n in npcs
              for q in ([n["pergunta"]] if n.get("pergunta") else []) + list(n.get("extras", []))
              if q not in banco]
    if faltam:
        raise ErroPerguntas("NPCs apontam para perguntas inexistentes: " + ", ".join(faltam))
