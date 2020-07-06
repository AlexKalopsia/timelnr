import datetime


class Label():
    def __init__(self, slug: str, name: str, color: str):
        self.slug = slug
        self.name = name
        self.color = color

    def __str__(self):
        return 'Label(slug:{}, name:{}, color:{})'.format(self.slug, self.name, self.color)
