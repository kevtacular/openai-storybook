class StoryGenerationParams:
    animals = []
    situation = ''
    genre = ''

    def __init__(self, animals=[], situation='', genre='') -> None:
        self.animals = animals
        self.situation = situation
        self.genre = genre

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
