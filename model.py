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

import re

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


class Snippet:
    """
    A portion of a Story.
    """

    length = 0
    story_lines = []

    def __init__(self, story_lines=None) -> None:
        self.story_lines = story_lines if story_lines is not None else []
        self.length = sum([len(line) for line in story_lines])

    def text(self) -> str:
        """
        Return this Snippet's text.
        """
        return "\n".join(self.story_lines)

    def chapter_nums(self) -> list:
        """
        Return a list of chapter numbers in this Snippet.
        """
        return [chap_tuple[0] for chap_tuple in self.chapter_lengths()]

    def chapter_lengths(self) -> list:
        """
        Return a list of tuples of chapter numbers and their lengths.

        For example: [(1,307), (3,423), (4,239)]
        """
        chapter_num = 0
        length = 0
        chapters = []
        page_regex = re.compile(r"Page (\d+)")

        for line in self.story_lines:
            match = page_regex.match(line)
            if match:
                if chapter_num != 0:
                    chapters.append((chapter_num, length))

                # reset vars for new chapter
                chapter_num = int(match.group(1))
                length = 0
            else:
                # add to cummulative length of current chapter
                length += len(line)

        # Add the last chapter
        chapters.append((chapter_num, length))

        return chapters

    def without_chapter(self, chapter_num):
        """
        Return a new Snippet identical to this Snippet, but without the
        given chapter.
        """
        lines = []
        copy = False
        page_regex = re.compile(r"Page (\d+)")
        for line in self.story_lines:
            match = page_regex.match(line)
            if match:
                copy = False if int(match.group(1)) == chapter_num else True
            if copy:
                lines.append(line)
        return Snippet(lines)


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
    story_lines = []

    def __init__(self, title="Empty Story", pages=None, story_lines=None) -> None:
        if pages is None:
            pages = [Page("Once upon a time...", "storybook.png")]  # a default
        if story_lines is None:
            story_lines = []
        self.title = title
        self.pages = pages
        self.story_lines = story_lines

    def full_snippet(self) -> Snippet:
        """
        Returns a Snippet consisting of all text in this Story.
        """
        return Snippet(self.story_lines)

    # def chapter_count(self):
    #     """
    #     TODO Return the number of chapters.
    #     """
    #     return 1

    # def chapter_len(self, chapter_num: int) -> int:
    #     """
    #     TODO Return the length of the given chapter (in characters).
    #     """
    #     return 1
