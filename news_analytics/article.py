class Article:
    def __init__(self, url: str, title: str, content: str, lang: str, tags: list):
        self.url = url
        self.title = title
        self.content = content
        self.lang = lang
        self.tags = tags