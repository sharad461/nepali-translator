from flask import Flask, render_template, request, url_for, redirect
from os import environ

app = Flask(__name__)

port = int(environ.get("PORT", 5000))

@app.route('/')
def index():
    return render_template("home.html", title="Nepali Translator", active="home")

@app.route('/translate')
def translate():
	return render_template("translate.html", title="Translate", active="translate")

@app.route('/about')
def about():
	return render_template("about.html", title="About", active="about")

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=port, debug=True)