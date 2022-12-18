"""
Model for children's stories.

Classes:

    Page
    Story
    StoryGenerationParams

Misc variables:

    animals
    situations
    genres
"""

animals = ["Horse", "Hippo", "Camel"]
situations = [
    "trying out for a Broadway musical",
    "building a raft to escape a deserted island",
    "flying a rickety spaceship that is in danger of being sucked into a black hole",
]

# Genres taken from https://www.cde.ca.gov/ci/cr/rl/litrlgenres.asp
genres = [
    "Drama",
    "Fable",
    "Fairy Tale",
    "Fantasy",
    "Fiction",
    "Fiction in Verse",
    "Folklore",
    "Historical Fiction",
    "Horror",
    "Humor",
    "Legend",
    "Mystery",
    "Mythology",
    "Poetry",
    "Realistic Fiction",
    "Science Fiction",
    "Short Story",
    "Tall Tale",
]


class StoryGenerationParams:
    """
    Class holding the parameters necessary to generate a Story.
    """

    animals = []
    situation = ""
    genre = ""

    def __init__(self, story_animals=None, story_situation="", story_genre="") -> None:
        if story_animals is None:
            story_animals = []
        self.animals = story_animals
        self.situation = story_situation
        self.genre = story_genre


class Page:
    """
    Class representing a page within a children's Story.
    """

    text = ""
    illustration = ""

    def __init__(self, text, illustration) -> None:
        self.text = text
        self.illustration = illustration


class Story:
    """
    Class representing an illustrated children's story.
    """

    title = ""
    pages = []

    def __init__(self, title="Empty Story", pages=None) -> None:
        if pages is None:
            pages = [Page("Once upon a time...", "storybook.png")]  # a default
        self.title = title
        self.pages = pages
