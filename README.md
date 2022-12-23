# OpenAI Storybook - A sample OpenAI app in Python

This is a basic children's story generation app implemented using Python and
[Flask](https://flask.palletsprojects.com/en/2.0.x/). The app allows you to
select the characters, situation, and literary genre for a story to be
generated. Once the parameters are selected, a story is generated using the
`openai.Completion` API and illustrated using the `openai.Image` API.

Follow the instructions below to set up and run the app.

## Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/)

2. Clone this repository

3. Navigate into the project directory

   ```bash
   $ cd openai-storybook
   ```

4. Create a new virtual environment

   ```bash
   $ python -m venv venv
   $ . venv/bin/activate
   ```

5. Install the requirements

   ```bash
   $ pip install -r requirements.txt
   ```

6. Make a copy of the example environment variables file

   ```bash
   $ cp .env.example .env
   ```

7. Add your OpenAI [API key](https://beta.openai.com/account/api-keys) to the
newly created `.env` file

8. Run the app

   ```bash
   $ flask run
   ```

You should now be able to access the app at [http://localhost:5000](http://localhost:5000)!

For more context behind this example app, check out the OpenAI quick start
[tutorial](https://beta.openai.com/docs/quickstart).
