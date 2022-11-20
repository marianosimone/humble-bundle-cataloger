class Item:
    def __init__(self, name, icon, url, recommended):
        self.name = name
        self.icon = icon
        self.url = url
        self.recommended = recommended

    def merge(self, other):
        self.icon = self.icon or other.icon
        self.url = self.url or other.url

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class Book(Item):
    def __init__(self, name, icon, url, author, recommended):
        super().__init__(name, icon, url, recommended)
        self.author = author

    def merge(self, other):
        super().merge(other)
        self.author = self.author or other.author


class Game(Item):
    def __init__(self, name, icon, url, recommended, platforms):
        super().__init__(name, icon, url, recommended)
        self.platforms = platforms

    def merge(self, other):
        if "android" in self.platforms:
            # The android version of the icon and the URL tend to be worse
            self.icon = other.icon or self.icon
            self.url = other.url or self.url
        else:
            super().merge(other)

        self.platforms = sorted(set(self.platforms + other.platforms))


class Software(Item):
    def __init__(self, name, icon, url, recommended, platforms):
        super().__init__(name, icon, url, recommended)
        self.platforms = platforms

    def merge(self, other):
        super().merge(other)
        self.platforms = sorted(set(self.platforms + other.platforms))


class DevelopmentTool(Software):
    def __init__(self, name, icon, url, recommended, platforms):
        super().__init__(name, icon, url, recommended, platforms)


class PrintableModel(Item):
    pass


class Soundtrack(Item):
    pass


class Video(Item):
    pass
