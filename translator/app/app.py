from flask import Flask, render_template, request, url_for, redirect
import os

from modules.speech import rec
from modules import interactive
from modules import translate
from modules.translate import bpencode, detok, tok

from datetime import datetime

gen = None

app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))

# def save_history(src, tgt):
# 	d = datetime.now()
# 	open("data/history/{}{}{}.history".format(d.year, d.month, d.day), "a", encoding="utf-8").write(src + " -> " + tgt + "\n")

@app.route('/')
def translate():
	return redirect("/translate/ne-en")

@app.route('/translate/ne-en')
def ne_en():
	global gen
	gen = interactive.Generator("app/ne_en_bpe20000", "app/models/ne-en.pt")
	return render_template("translate.html", title="Translate", active="translate", type="ne_en")

@app.route('/translate/ne-en/<string:sent>')
def ne_en_translate(sent):
	translated = detok(gen.generate(bpencode(tok(sent, lang="ne"), "ne_en")), lang="en")
	# save_history(sent, translated)
	return render_template("transtext.html", data=translated)

@app.route('/translate/en-ne')
def en_ne():
	global gen
	gen = interactive.Generator("app/en_ne_bpe5000", "app/models/en-ne.pt")
	return render_template("translate.html", title="Translate", active="translate", type="en_ne")

@app.route('/translate/en-ne/<string:sent>')
def en_ne_translate(sent):
	translated = detok(gen.generate(bpencode(tok(sent, lang="en"), "en_ne")), lang="ne")
	# save_history(sent, translated)	
	return render_template("transtext.html", data=translated)

@app.route('/listen')
def listen():
	return render_template("listen.html", title="Listen", data=rec())

@app.route('/save/<string:str1>/<string:str2>')
def save(str1, str2):
	with open("data/saved", "a", encoding="utf-8") as f:
		f.write(str1 + " -> " + str2 + "\n")
		return "s"
	return "n"

@app.route('/saved')
def saved():
	saved = open("data/saved", "r", encoding="utf-8").read().split('\n')
	return render_template("listprint.html", data=saved)

@app.route('/history')
def history():
	dates = [os.path.splitext(path)[0] for path in os.listdir("data/history")]
	return render_template("history.html", data=dates)

@app.route('/history/<string:date>')
def history_date(date):
	saved = open("data/history/"+date+".history", "r", encoding="utf-8").read().split("\n")
	return render_template("listprint.html", data=saved)

@app.route('/about')
def about():
	return render_template("about.html", title="About", active="about")

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=port, debug=True)