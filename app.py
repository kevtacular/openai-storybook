import json
import uuid
from flask import Flask, redirect, render_template, request, session, url_for
from model import animals, situations, genres, StoryGenerationParams, Story
from service import StoryService
from util import to_json


app = Flask(__name__)
app.secret_key = str(uuid.uuid4())

story_service = StoryService()


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
    
    story = story_service.generate_story(story_params)
    session['story'] = to_json(story)

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
