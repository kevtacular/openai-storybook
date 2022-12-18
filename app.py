import os

import json
import openai
import uuid
from flask import Flask, redirect, render_template, request, session, url_for
from model import animals, situations, genres, StoryGenerationParams, Story

# For unit testing, we can simply load a previously-generated Completion
# response from a test file. This is the default behavior. To enable AI
# (i.e., calls to the Open AI API), set this env var to True.
ENABLE_AI=(os.getenv('STORY_ENABLE_AI', 'False') == 'True')

OPENAI_MODEL='text-davinci-003'
OPENAI_TEMP=0.6


app = Flask(__name__)
app.secret_key = str(uuid.uuid4())
openai.api_key = os.getenv('OPENAI_API_KEY')


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
    story_to_render = Story()
    if 'story' not in session:
        return redirect(url_for("index"))
    else:
        story_to_render.__dict__ = json.loads(session['story'])

        try:
            pagenum_arg = int(request.args.get("pagenum"))
            pagenum = pagenum_arg if pagenum_arg in range(0, len(story_to_render.pages)) else 0
        except:
            pagenum = 0
        
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
    
    story = generate_story(story_params)
    session['story'] = to_json(story)

    return redirect(url_for("storypage", pagenum=0))


"""
Generate a new story from the given parameters.
"""
def generate_story(story_params) -> Story:
    story_prompt = generate_prompt(story_params)
    print('PROMPT')
    print(story_prompt)

    if ENABLE_AI:
        response = openai.Completion.create(
            model=OPENAI_MODEL,
            prompt=story_prompt,
            temperature=OPENAI_TEMP,
            max_tokens=400,
        )
        print("RESULT")
        print(to_json(response))
        story_text = response.choices[0].text
    else:
        story_text = load_story_text('test/testresponse.json')

    print("STORY TEXT")
    print(story_text)

    return Story.parse(story_text)


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


"""
Generate an Open AI prompt to generate a new story.
"""
def generate_prompt(story_params: StoryGenerationParams):  # """.format(", ".join(story_params.animals))
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
def load_story_text(response_file):
    response = None
    with open(response_file, 'r') as f:
        response = json.load(f)
    print('response...')
    print(response['_previous'])
    print(response['_previous']['choices'])
    print(response['_previous']['choices'][0])
    print(response['_previous']['choices'][0]['text'])
    return response['_previous']['choices'][0]['text']


"""
Convert object to JSON string.
"""
def to_json(an_object: object):
    return json.dumps(an_object.__dict__, default=lambda o: o.__dict__, indent=True)