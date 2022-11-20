from typing import Callable, Optional

from item_types import Book, Item, DevelopmentTool, Software, Video


def create_book(name, icon, url, author, recommended):
    return Book(name, icon, url, author, recommended)


def create_software(name, icon, url, recommended, platforms):
    return Software(name, icon, url, recommended, platforms)


def create_video(name, icon, url, recommended, platforms):
    return Video(name, icon, url, recommended)


def create_development_tool(name, icon, url, recommended, platforms):
    return DevelopmentTool(name, icon, url, recommended, platforms)


# These are known cases of content that is not a game
# In some cases, you'd want to keep it in sync with name_fixes.py
TYPE_FOR_NAME: dict[str, Callable[[str, str, str, bool, Optional[list[str]]], Item]] = {
    "Ashampoo Photo Optimizer 7": create_software,
    "Discover Unity Game Development - From Zero to 12 Games": create_development_tool,
    "Double Fine Adventure": create_video,
    "FlowCanvas": create_development_tool,
    "Gaia": create_development_tool,
    "GameFlow": create_development_tool,
    "GameGuru": create_development_tool,
    "GameMaker Studio 2 Creator 12 Months": create_development_tool,
    "Heroic Fantasy Creatures Full Pack Volume 1": create_development_tool,
    "Intro to Game Development with Unity": create_development_tool,
    "Inventory Pro": create_development_tool,
    "Music Maker EDM Edition": create_software,
    "Pathfinder Second Edition Core Rulebook and Starfinder Core Rulebook": create_book,
    "PDF-Suite Standard": create_software,
    "Polygon Farm, Polygon City, and Polygon Prototype": create_development_tool,
    "Realistic Effects Pack 4": create_development_tool,
    "RPG Maker VX": create_development_tool,
    "Starfinder: Pact Worlds Campaign Setting": create_book,
    "UFPS: Ultimate FPS": create_development_tool,
    "Ultimate Game Music Collection": create_development_tool,
    "uMMORPG": create_development_tool,
    "Universal Sound FX": create_development_tool,
}
