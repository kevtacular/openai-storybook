import re

animals = ['Horse', 'Hippo', 'Camel']
situations = [
    'trying out for a Broadway musical',
    'building a raft to escape a deserted island',
    'flying a rickety spaceship that is in danger of being sucked into a black hole'
]

# Genres taken from https://www.cde.ca.gov/ci/cr/rl/litrlgenres.asp
genres = [
    'Drama', 'Fable', 'Fairy Tale', 'Fantasy', 'Fiction', 'Fiction in Verse',
    'Folklore', 'Historical Fiction', 'Horror', 'Humor', 'Legend', 'Mystery',
    'Mythology', 'Poetry', 'Realistic Fiction', 'Science Fiction', 'Short Story',
    'Tall Tale'
]

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

    @classmethod
    def parse(cls, story_text):
        story_lines = story_text.splitlines()

        title = ''
        while not title:
            title = story_lines[0]
            story_lines = story_lines[1:]

        pages = []
        page = None
        page_regex = re.compile(r'Page \d+')
        for i in range(len(story_lines)):
            if page_regex.match(story_lines[i]):
                page = Page('', 'storybook.png')
                pages.append(page)
            elif page:
                page.text = page.text + story_lines[i] + '\n'

        return Story(title, pages)