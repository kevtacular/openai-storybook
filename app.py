import os

import json
import openai
import uuid
from flask import Flask, redirect, render_template, request, session, url_for
from model import StoryGenerationParams, Story, Page

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

pages = [
    Page('Once upon a time, in a faraway land, there was a beautiful princess named Cinderella. She lived with her wicked stepmother and stepsisters, who made her do all the hard work around the house.', 'storybook.png'),
    Page('One day, the royal castle announced that it was holding a ball and inviting all the eligible young ladies in the kingdom to attend. Cinderella''s stepsisters were thrilled, but Cinderella was sad because she knew she had no way of going to the ball.', 'storybook.png'),
    Page('The End', 'storybook.png')
    ]
story = Story('My Story', pages)

# for page in story.pages:
#     print(f"{page.text}, {page.illustration}")

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=["GET", "POST"])
def index():
    errors=[]
    if 'errs' in request.args:
        errors = request.args.getlist('errs')
    
    story_params = StoryGenerationParams()
    if 'story_params' in session:
        story_params.__dict__ = json.loads(session['story_params'])
    else:
        session['story_params'] = to_json(story_params)

    return render_template("index.html",
        animals=animals, situations=situations, genres=genres, params=story_params,
        errs=errors)


@app.route("/story", methods=["GET"])
def storypage():
    try:
        pagenum_arg = int(request.args.get("pagenum"))
        pagenum = pagenum_arg if pagenum_arg in range(0, len(story.pages)) else 0
    except:
        pagenum = 0
    
    story_to_render = Story()
    if 'story' in session:
        story_to_render.__dict__ = json.loads(session['story'])

    return render_template("story.html", story=story_to_render, pagenum=pagenum)


@app.route("/story", methods=["POST"])
def post_storypage():
    story_params, errors = get_story_gen_params()
    session['story_params'] = to_json(story_params)
    if len(errors) > 0:
        return redirect(url_for("index", errs=errors))

    print(f'animals={story_params.animals}; '
        f'situation={story_params.situation}; '
        f'genre={story_params.genre}')

    # response = openai.Completion.create(
    #     model="text-davinci-002",
    #     prompt=generate_prompt(animal),
    #     temperature=0.6,
    # )

    session['story'] = to_json(story)
    # print(json.dumps(story.__dict__, default=lambda o: o.__dict__, indent=True))

    return redirect(url_for("storypage", pagenum=0))


def get_story_gen_params():
    animals = []
    situation = ''
    genre = ''
    errors = []
    
    if 'animal' in request.form:
        animals = request.form.getlist('animal')
    else:
        errors.append('One or more animals are required.')

    if 'situation' in request.form:
        situation = request.form['situation']
    else:
        errors.append('Situation is required.')

    if 'genre' in request.form:
        genre = request.form['genre']
    else:
        errors.append('Genre is required.')

    print(errors)

    return StoryGenerationParams(animals, situation, genre), errors


# def generate_prompt(animal):
#     return """Suggest three names for an animal that is a superhero.

# Animal: Cat
# Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
# Animal: Dog
# Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
# Animal: {}
# Names:""".format(
#         animal.capitalize()
#     )

def to_json(an_object: object):
    return json.dumps(an_object.__dict__, default=lambda o: o.__dict__,)