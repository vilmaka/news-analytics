class Article:
    def __init__(self, url: str, title: str, content: str, lang: str, tags: list, date: str):
        self.url = url
        self.title = title
        self.content = content
        self.lang = lang
        self.tags = tags
        self.date = date

    def to_dict(self):
        return {
            'url': self.url,
            'title': self.title,
            'content': self.title,
            'lang': self.lang,
            'tags': self.tags,
            'date': self.date
        }