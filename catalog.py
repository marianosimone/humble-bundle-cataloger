#!/usr/bin/env python3

import argparse
from parser import get_data
from jinja2 import Environment, FileSystemLoader
from item_types import (
    Book,
    DevelopmentTool,
    Game,
    Software,
    PrintableModel,
    Soundtrack,
    Video,
)


def generate_report(data):
    env = Environment(
        loader=FileSystemLoader("."),
    )

    template = env.get_template("template.html").render(
        books=sorted(set(data[Book]), key=lambda i: i.name),
        development_tools=sorted(set(data[DevelopmentTool]), key=lambda i: i.name),
        games=sorted(set(data[Game]), key=lambda i: i.name),
        models=sorted(set(data[PrintableModel]), key=lambda i: i.name),
        soundtracks=sorted(set(data[Soundtrack]), key=lambda i: i.name),
        software=sorted(set(data[Software]), key=lambda i: i.name),
        videos=sorted(set(data[Video]), key=lambda i: i.name),
    )
    with open("catalog.html", "w") as file:
        file.write(template)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--all",
        action="store_true",
        help="catalog everything, and not only available entries",
    )
    args = arg_parser.parse_args()
    generate_report(get_data(include_all=args.all))


if __name__ == "__main__":
    main()
