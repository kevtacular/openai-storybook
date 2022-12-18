"""
A Flask web app for generating and viewing children's stories using Open AI
APIs.
"""
import json
import uuid
from flask import Flask, redirect, render_template, request, session, url_for
from model import animals, situations, genres, StoryGenerationParams, Story
from generation import StoryService
from util import to_json


app = Flask(__name__)
app.secret_key = str(uuid.uuid4())

story_service = StoryService()


@app.route("/", methods=["GET", "POST"])
def index():
    """
    GET /

    Return story generation form.

    Params:

        errs - error string for display; multiple occurrences supported
    """
    errors = []
    if "errs" in request.args:
        errors = request.args.getlist("errs")

    story_params = StoryGenerationParams()
    if "story_params" in session:
        story_params.__dict__ = json.loads(session["story_params"])
    else:
        session["story_params"] = to_json(story_params)

    return render_template(
        "index.html",
        animals=animals,
        situations=situations,
        genres=genres,
        params=story_params,
        errs=errors,
    )


@app.route("/story", methods=["GET"])
def storypage():
    """
    GET /story

    Display the specified page of the user's story (as stored in the session).

    Params:

        pagenum - the (zero-based) page number of the story
    """
    story_to_render = Story()
    if "story" not in session:
        return redirect(url_for("index"))
    else:
        story_to_render.__dict__ = json.loads(session["story"])

        try:
            pagenum_arg = int(request.args.get("pagenum"))
            pagenum = (
                pagenum_arg
                if pagenum_arg in range(0, len(story_to_render.pages))
                else 0
            )
        except ValueError:
            pagenum = 0

        return render_template("story.html", story=story_to_render, pagenum=pagenum)


@app.route("/story", methods=["POST"])
def post_storypage():
    """
    POST /story

    Generate a new children's story and store it in the session, then display
    the first page of the generated story.

    Params:

        animal - one or more animals to be characters in the story
        situation - a situation the animals find themselves in
        genre - a literary genre in which the story is to be told
    """
    story_params, errors = _get_story_gen_params()
    session["story_params"] = to_json(story_params)
    if len(errors) > 0:
        return redirect(url_for("index", errs=errors))

    print(
        f"animals={story_params.animals}; "
        f"situation={story_params.situation}; "
        f"genre={story_params.genre}"
    )

    story = story_service.generate_story(story_params)
    session["story"] = to_json(story)

    return redirect(url_for("storypage", pagenum=0))


def _get_story_gen_params() -> StoryGenerationParams:
    """
    Read the HTTP params and construct a StoryGenerationParams object from
    them.
    """
    story_animals = []
    story_situation = ""
    story_genre = ""
    errors = []

    if "animal" in request.form:
        story_animals = request.form.getlist("animal")
    else:
        errors.append("One or more animals are required.")

    if "situation" in request.form:
        story_situation = request.form["situation"]
    else:
        errors.append("Situation is required.")

    if "genre" in request.form:
        story_genre = request.form["genre"]
    else:
        errors.append("Genre is required.")

    print(errors)

    return StoryGenerationParams(story_animals, story_situation, story_genre), errors
