"""Pedala, Maricá! - ponto de entrada (compatível com Pygbag)."""
import asyncio

from src.core.game import Game


async def main():
    await Game().executar()


asyncio.run(main())
