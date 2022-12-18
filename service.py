import json
import openai
import os
import re
from model import Story, StoryGenerationParams, Page
from util import to_json

# For unit testing, we can simply load a previously-generated Completion
# response from a test file. This is the default behavior. To enable AI
# (i.e., calls to the Open AI API), set this env var to True.
_ENABLE_AI = (os.getenv('STORY_ENABLE_AI', 'False') == 'True')

_OPENAI_MODEL = 'text-davinci-003'
_OPENAI_TEMP = 0.6

openai.api_key = os.getenv('OPENAI_API_KEY')


"""
A service for generating children's stories using the Open AI API.
"""
class StoryService:

    def __init__(self) -> None:
        pass

    """
    Generate a new story from the given parameters.
    """
    def generate_story(self, story_params, temperature=_OPENAI_TEMP) -> Story:
        story_prompt = self._generate_prompt(story_params)
        print('PROMPT')
        print(story_prompt)

        if _ENABLE_AI:
            response = openai.Completion.create(
                model=_OPENAI_MODEL,
                prompt=story_prompt,
                temperature=temperature,
                max_tokens=400,
            )
            print("RESULT")
            print(to_json(response))
            story_text = response.choices[0].text
        else:
            story_text = self._load_story_text('test/testresponse.json')

        print("STORY TEXT")
        print(story_text)

        return self._parse_story(story_text)

    """
    Generate an Open AI prompt to generate a new story.
    """
    def _generate_prompt(self, story_params: StoryGenerationParams):  # """.format(", ".join(story_params.animals))
        return """Generate a childrens story involving these animals: {}. 

The animals are {}. The story should be written in the genre of "{}".

Generate a title on the first line (with no other text) and divide the story
into multiple pages, each with a header of the form "Page N".

""".format(
        ", ".join(story_params.animals),
        story_params.situation,
        story_params.genre
    )

    """
    Used during development only!
    """
    def _load_story_text(self, response_file) -> str:
        response = None
        with open(response_file, 'r') as f:
            response = json.load(f)
        return response['_previous']['choices'][0]['text']

    """
    Parse a Completion response into a Story.
    """
    def _parse_story(self, story_text) -> Story:
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