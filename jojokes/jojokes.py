# jojokes flask app
# serves up a random JoJo's Bizarre Adventures joke on every page load

from random import seed, choice

from flask import Flask, render_template, redirect, url_for

# app initialization
app = Flask(__name__)
app.config.from_object('config')
seed()

# define all of the jokes
class Joke:

	def __init__(self, setup, punchline):
		self.setup = setup
		self.punchline = punchline

	def __repr__(self):
		return 'Joke({}, {})'.format(self.setup, self.punchline)

jokes = [
	Joke("What is Joseph's favorite type of meat?", "Hamon iberico."),
	Joke("Did you hear what happened to Joseph's hand?", 
		"He lost it in a Kars accident."),
	Joke("If Wham! were your personal butler, what would he say to you every morning?",
		"Awaken, my master."),
	Joke("What is Dio's favorite TV sitcom?",
		"Everybody loves WRYYYYYYYYmond."),
]

# define the views
@app.route("/")
def index():
	joke = choice(jokes)
	return render_template("index.html",
		title="Home",
		joke=joke)

@app.route("/<path:any>")
def to_index(any):
	return redirect(url_for('index'))

# app execution
if __name__ == "__main__":
	app.run()