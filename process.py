from collections import defaultdict
from functools import reduce
from itertools import chain
from jinja2 import Environment, FileSystemLoader
import json
from fixes import FIXES
from typing import Any, Callable, Iterable, Optional, Type, TypeVar
import re

TYPES_TO_IGNORE = [
    ["video"],  # these are movies
    [],  # there are cases which are expired or otherwise unredeemable
]


# This is just my list of recommended entries... Feel free to change it ;)
try:
    with open("recommended.txt", "r") as recommended:
        RECOMMENDED = set(map(lambda l: l.strip(), recommended))
except Exception as e:
    print(
        "Couldn't find `recommended.txt`, create one if you want to highlight any entries"
    )
    RECOMMENDED = set()

# This are known entries in Humble Bundle that are not games, but Software utils/packages
try:
    with open("non_games.txt", "r") as non_games:
        NON_GAMES = set(map(lambda l: l.strip(), non_games))
except Exception as e:
    NON_GAMES = set()


class Item:
    def __init__(self, name, icon, url, recommended):
        self.name = name
        self.icon = icon
        self.url = url
        self.recommended = recommended

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class Book(Item):
    def __init__(self, name, icon, url, author, recommended):
        super().__init__(name, icon, url, recommended)
        self.author = author


class Game(Item):
    def __init__(self, name, icon, url, recommended, platforms):
        super().__init__(name, icon, url, recommended)
        self.platforms = platforms


class Software(Item):
    def __init__(self, name, icon, url, recommended, platforms):
        super().__init__(name, icon, url, recommended)
        self.platforms = platforms


class Soundtrack(Item):
    pass


class PrintableModel(Item):
    pass


GroupByKey = TypeVar("GroupByKey")
GroupByType = TypeVar("GroupByType")


def group_by(
    key: Callable[[GroupByType], GroupByKey], seq: Iterable[GroupByType]
) -> dict[GroupByKey, list[GroupByType]]:
    result = defaultdict(list)
    for item in seq:
        result[key(item)].append(item)
    return result


def extract_subproduct(subproduct: dict[str, Any]) -> Optional[Item]:
    icon = subproduct["icon"]
    name = FIXES.get(subproduct["human_name"], subproduct["human_name"])
    url = subproduct["url"]
    type_of_item = detect_type(subproduct["downloads"])
    recommended = name in RECOMMENDED

    if type_of_item in TYPES_TO_IGNORE:
        return None
    if type_of_item == ["other"]:
        return PrintableModel(name, icon, url, recommended)
    if type_of_item == ["ebook"]:
        return Book(name, icon, url, subproduct["payee"]["human_name"], recommended)
    if type_of_item == ["audio"]:
        return Soundtrack(name, icon, url, recommended)

    # if we are here, we can "safely" assume that we are dealing with a game or software
    platforms = sorted(
        set([i for i in type_of_item if i not in ["audio", "ebook", "asmjs"]])
    )
    if platforms:
        if name in NON_GAMES:
            return Software(name, icon, url, recommended, platforms)
        return Game(name, icon, url, recommended, platforms)
    return None


def detect_type(downloads: list[dict[str, str]]) -> list[str]:
    return [d["platform"] for d in downloads]


def extract_steam_game(tpkd: dict[str, str]) -> Optional[str]:
    name = FIXES.get(tpkd["human_name"], tpkd["human_name"])
    name = re.sub(r" Steam Key$", "", name)
    is_expired = tpkd["is_expired"]
    key_type = tpkd["key_type"]
    is_steam = key_type == "steam"
    redeemed = "redeemed_key_val" in tpkd
    is_gift = "is_gift" in tpkd

    if is_steam and not is_expired and not redeemed and not is_gift:
        return name
    return None


def get_data() -> dict[Type[Item], list[Item]]:
    with open("humble_catalog.json", "r") as file:
        data = json.load(file).values()

    subproduct_data = chain.from_iterable(
        map(extract_subproduct, d["subproducts"]) for d in data
    )
    extracted_steam_games = chain.from_iterable(
        map(extract_steam_game, d["tpkd_dict"]["all_tpks"]) for d in data
    )
    typed_data_by_name = {(type(d), d.name): d for d in subproduct_data if d}

    for name in extracted_steam_games:
        if not name:
            continue
        key = (Game, name)
        game = typed_data_by_name.get(key)
        if isinstance(game, Game) and "steam" not in game.platforms:
            game.platforms = sorted(game.platforms + ["steam"])
        else:
            typed_data_by_name[key] = Game(name, "", "", name in RECOMMENDED, ["steam"])

    return group_by(type, typed_data_by_name.values())


def generate_report(data):
    env = Environment(
        loader=FileSystemLoader("."),
    )

    template = env.get_template("template.html").render(
        books=sorted(set(data[Book]), key=lambda b: b.name),
        games=sorted(set(data[Game]), key=lambda g: g.name),
        models=sorted(set(data[PrintableModel]), key=lambda g: g.name),
        soundtracks=sorted(set(data[Soundtrack]), key=lambda g: g.name),
        software=sorted(set(data[Software]), key=lambda g: g.name),
    )
    with open("catalog.html", "w") as file:
        file.write(template)


generate_report(get_data())
