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


class PrintableModel(Item):
    pass


class Soundtrack(Item):
    pass


class Video(Item):
    pass
