"""
Illustration of Stories using the Open AI DALL-E API.
"""
import openai

from model import Story
from util import to_json

_MAX_PROMPT_LEN = 1000
_STORY_IMAGE_PROMPT = """An illustration of page {} of the following children's story:
Title: {}
{}
"""


class IllustrationService:
    """
    A service for illustrating Stories with images generated from the Open AI
    DALL-E API.
    """

    def illustrate_story(self, story: Story) -> None:
        """
        Updates the given Story with images generated from DALL-E.
        """
        for pagenum, page in enumerate(story.pages):
            print(f"IMAGE - PG {pagenum}")

            prompt = self._create_image_prompt(story, pagenum)

            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="256x256",
            )

            print(to_json(response))

            image_url = response["data"][0]["url"]
            print(f"image_url = {image_url}")
            page.illustration = image_url

    def _create_image_prompt(self, story: Story, pagenum: int) -> str:
        """
        Generate a prompt for the OpenAI Image API to generate an illustration
        for the given page of the given story.
        """
        snippet = story.full_snippet()
        while snippet.length > _MAX_PROMPT_LEN - len(
            _STORY_IMAGE_PROMPT.format(pagenum + 1, story.title, snippet.text())
        ):
            chapter_nums = snippet.chapter_nums()
            print(f"chapter_nums = {chapter_nums}")
            last_chapter = chapter_nums[len(chapter_nums) - 1]
            if pagenum + 1 == last_chapter:
                chapter_to_remove = chapter_nums[len(chapter_nums) - 2]
            else:
                chapter_to_remove = last_chapter
            snippet = snippet.without_chapter(chapter_to_remove)

        prompt = _STORY_IMAGE_PROMPT.format(pagenum + 1, story.title, snippet.text())
        print(f"prompt len = {len(prompt)}")

        return prompt
