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


def main():
    """Run the full game."""

    print(__doc__)
    options = AuxiliaryTools.parse_args()

    world_file = './worlds/Debugland/states.json'
    wb = WarBot.WarBot(world_file)
    wb.run(**options["WarBot.run"])


app = Flask(__name__)


@app.route("/")
def home():
    text = "Hello! welcome to warbot"
    bold_text = "Whup Whup!"
    return render_template('home.html', text=text, bold_text=bold_text)


@app.route("/play", methods=["POST", "GET"])
def play():
    if request.method == "POST":
        world = request.form["world"]
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        main()
        sys.stdout = old_stdout
        return render_template('warbot_game.html', text=mystdout.getvalue())
    else:
        return render_template('warbot_game.html')
