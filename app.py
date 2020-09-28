from flask import Flask, render_template, request

from io import StringIO
import sys

### Install requirements.txt
### Run it from warbot folder with 'flask run'
### Look at the webpage http://127.0.0.1:5000/

sys.path.append("src/")

import WarBot
import WorldSelector
import AuxiliaryTools

app = Flask(__name__)


def run_game(world):
    # TODO: this should become easier
    options = AuxiliaryTools.parse_args()
    root = '.'
    dnames = WorldSelector.list_worlds(root)
    world_file = WorldSelector.verify_choice(root, dnames, world)
    wb = WarBot.WarBot(world_file)
    wb.run(**options["WarBot.run"])


@app.route("/")
def home():
    title = "Welcome to warbot"
    text = "Have fun!"
    return render_template('home.html', title=title, text=text)


@app.route("/play", methods=["POST", "GET"])
def play():
    worlds = WorldSelector.list_worlds(".")

    if request.method == "POST":
        world = request.form.get('world')
        old_stdout = sys.stdout
        sys.stdout = output = StringIO()
        run_game(world)
        text = output.getvalue()
        sys.stdout = old_stdout

        # TODO: display correctly the \t
        # We need this trick do add new lines to the text
        # https://stackoverflow.com/a/41694784
        text = text.split('\n')

        return render_template('warbot_game.html', worlds=worlds, text=text)
    else:
        return render_template('warbot_game.html', worlds=worlds)
