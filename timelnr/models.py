import datetime


class Label():
    def __init__(self, slug: str, name: str, color: str):
        self.slug = slug
        self.name = name
        self.color = color

    def __str__(self):
        return 'Label(slug:{}, name:{}, color:{})'.format(self.slug, self.name, self.color)


class Entry():
    def __init__(self, id: int, content: str, year: int, label: str, imageURL: str):
        self.id = id
        self.content = content
        self.year = year
        self.label = label
        self.imageURL = imageURL

    def __str__(self):
        return 'Entry(id:{}, content:{}, year:{}, label:{}, imageURL:{})'.format(self.id, self.content, self.year, self.label, self.imageURL)
