from flask import Flask, render_template, request, url_for, redirect
from os import environ
from speech import rec

app = Flask(__name__)

port = int(environ.get("PORT", 5000))

@app.route('/')
def index():
    return render_template("home.html", title="Nepali Translator", active="home")

@app.route('/translate')
def translate():
	return render_template("translate.html", title="Translate", active="translate")

@app.route('/listen')
def listen():
	record = rec()
	return render_template("listen.html", title="Listen", data=record)

@app.route('/about')
def about():
	return render_template("about.html", title="About", active="about")

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=port, debug=True)