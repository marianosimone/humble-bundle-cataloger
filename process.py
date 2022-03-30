from collections import defaultdict
from functools import reduce
from itertools import chain
from jinja2 import Environment, FileSystemLoader
import json
from fixes import FIXES

TYPES_TO_IGNORE = [
    ["audio"],  # these are soundtracks
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


class Item:
    def __init__(self, name, icon, url):
        self.name = name
        self.icon = icon
        self.url = url

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class Book(Item):
    def __init__(self, name, icon, url, author):
        super().__init__(name, icon, url)
        self.author = author


class Game(Item):
    def __init__(self, name, icon, url, recommended, platforms, has_steam_key):
        super().__init__(name, icon, url)
        self.recommended = recommended
        self.platforms = platforms
        self.has_steam_key = has_steam_key


class PrintableModel(Item):
    pass


def groupBy(key, seq):
    return reduce(
        lambda grp, val: grp[key(val)].append(val) or grp, seq, defaultdict(list)
    )


def extract_subproduct(subproduct):
    icon = subproduct["icon"]
    name = FIXES.get(subproduct["human_name"], subproduct["human_name"])
    url = subproduct["url"]
    type_of_item = detect_type(subproduct["downloads"])

    if type_of_item in TYPES_TO_IGNORE:
        return None
    if type_of_item == ["other"]:
        return PrintableModel(name, icon, url)
    if type_of_item == ["ebook"]:
        return Book(name, icon, url, subproduct["payee"]["human_name"])

    # if we are here, we can "safely" assume that we are dealing with a game
    platforms = sorted(
        set([i for i in type_of_item if i not in ["audio", "ebook", "asmjs"]])
    )
    if platforms:
        return Game(name, icon, url, name in RECOMMENDED, platforms, False)


def detect_type(downloads):
    return [d["platform"] for d in downloads]


def extract_steam_game(tpkd):
    name = FIXES.get(tpkd["human_name"], tpkd["human_name"])
    is_expired = tpkd["is_expired"]
    key_type = tpkd["key_type"]
    is_steam = key_type == "steam"
    redeemed = "redeemed_key_val" in tpkd
    is_gift = "is_gift" in tpkd

    if is_steam and not is_expired and not redeemed and not is_gift:
        return name


def get_data():
    with open("humble_catalog.json", "r") as file:
        data = json.load(file).values()

    subproduct_data = chain.from_iterable(
        map(extract_subproduct, d["subproducts"]) for d in data
    )
    extracted_steam_games = chain.from_iterable(
        map(extract_steam_game, d["tpkd_dict"]["all_tpks"]) for d in data
    )
    typed_data_by_name = {d.name: d for d in subproduct_data if d}
    games_by_existing = groupBy(
        lambda n: n in typed_data_by_name, extracted_steam_games
    )

    for game in games_by_existing[True]:
        typed_data_by_name[game].has_steam_key = True

    just_steam_games = [
        Game(n, "", "", n in RECOMMENDED, [], True)
        for n in games_by_existing[False]
        if n
    ]

    return groupBy(type, chain(typed_data_by_name.values(), just_steam_games))


def render_template(data):
    return


def generate_report(data):
    env = Environment(
        loader=FileSystemLoader("."),
    )

    template = env.get_template("template.html").render(
        books=sorted(set(data[Book]), key=lambda b: b.name),
        games=sorted(set(data[Game]), key=lambda g: g.name),
        models=sorted(set(data[PrintableModel]), key=lambda g: g.name),
    )
    with open("catalog.html", "w") as file:
        file.write(template)


generate_report(get_data())
