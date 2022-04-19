from typing import Callable, Optional

from item_types import Item, Software, Video


def create_software(name, icon, url, recommended, platforms):
    return Software(name, icon, url, recommended, platforms)


def create_video(name, icon, url, recommended, platforms):
    return Video(name, icon, url, recommended)


# These are known cases of content that is not a game
# In some cases, you'd want to keep it in sync with fixes.py
TYPE_FOR_NAME: dict[str, Callable[[str, str, str, bool, Optional[list[str]]], Item]] = {
    "Ashampoo Photo Optimizer 7": create_software,
    "GameGuru": create_software,
    "Music Maker EDM Edition": create_software,
    "PDF-Suite Standard": create_software,
    "RPG Maker VX": create_software,
    "Double Fine Adventure": create_video,
}
