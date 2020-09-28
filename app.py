from flask import Flask, redirect, url_for, render_template, request
from flask import render_template

from io import StringIO
import sys

### Install requirements.txt
### Run it from warbot folder with 'flask run'
### Look at the webpage http://127.0.0.1:5000/

sys.path.append("src/")

import WarBot
import WorldSelector
import AuxiliaryTools
import HistoricStatistician as hs





app = Flask(__name__)


def run_game(world):
    """Run the full game."""

    options = AuxiliaryTools.parse_args()
    root='.'
    dnames = WorldSelector.list_worlds(root)
    world_file = WorldSelector.verify_choice(root, dnames, world)
    wb = WarBot.WarBot(world_file)
    wb.run(**options["WarBot.run"])

@app.route("/")
def home():
    text = "Hello! welcome to warbot"
    bold_text = "Whup Whup!"
    return render_template('home.html', text=text, bold_text=bold_text)


@app.route("/play", methods=["POST", "GET"])
def play():
    worlds = WorldSelector.list_worlds(".")

    if request.method == "POST":
        world = request.form.get('world')
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        run_game(world)
        sys.stdout = old_stdout
        asd=mystdout.getvalue()
        print(asd)

        asd = asd.replace('\n', '<br>')

        return render_template('warbot_game.html', worlds=worlds, text=asd)
    else:
        return render_template('warbot_game.html', worlds=worlds)
