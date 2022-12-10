import os

import json
import openai
import uuid
from flask import Flask, redirect, render_template, request, session, url_for
from model import Story, Page

pages = [
    Page('Once upon a time, in a faraway land, there was a beautiful princess named Cinderella. She lived with her wicked stepmother and stepsisters, who made her do all the hard work around the house.', 'storybook.png'),
    Page('One day, the royal castle announced that it was holding a ball and inviting all the eligible young ladies in the kingdom to attend. Cinderella''s stepsisters were thrilled, but Cinderella was sad because she knew she had no way of going to the ball.', 'storybook.png'),
    Page('The End', 'storybook.png')
    ]
story = Story('My Story', pages)

for page in story.pages:
    print(f"{page.text}, {page.illustration}")

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    return render_template("index.html")


@app.route("/story", methods=("GET", "POST"))
def storypage():
    if request.method == "POST":
        # animal = request.form["animal"]
        # response = openai.Completion.create(
        #     model="text-davinci-002",
        #     prompt=generate_prompt(animal),
        #     temperature=0.6,
        # )
        session['story'] = json.dumps(story.__dict__, default=lambda o: o.__dict__,)
        print(json.dumps(story.__dict__, default=lambda o: o.__dict__, indent=True))
        return redirect(url_for("storypage", pagenum=0))

    try:
        pagenum_arg = int(request.args.get("pagenum"))
        pagenum = pagenum_arg if pagenum_arg in range(0, len(story.pages)) else 0
    except:
        pagenum = 0
    
    story_to_render = Story()
    if 'story' in session:
        story_to_render.__dict__ = json.loads(session['story'])

    return render_template("story.html", story=story_to_render, pagenum=pagenum)


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )
