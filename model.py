class Page:
    text = ''
    illustration = ''

    def __init__(self, text, illustration) -> None:
        self.text = text
        self.illustration = illustration


class Story:
    title = ''
    pages = []

    def __init__(self, title='Empty Story', pages=[Page('Once upon a time...', 'storybook.png')]) -> None:
        self.title = title
        self.pages = pages
