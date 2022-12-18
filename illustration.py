"""
Illustration of Stories using the Open AI DALL-E API.
"""
from model import Story


class IllustrationService:
    """
    A service for illustrating Stories with images generated from the Open AI
    DALL-E API.
    """

    def illustrate_story(self, story: Story) -> None:
        """
        Updates the given Story with images generated from DALL-E.
        """
        for page in story.pages:
            # TODO: Generate illustrations for each page
            page.illustration = "storybook.png"
