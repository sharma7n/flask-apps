#!flaskr/bin/python
# Flaskr tutorial app from flask.pocoo.org

import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash

# Flaskr app instantiation and configuration

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'flaskr.db'),
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# Database methods

def connect_db():
	"""Connects to the specific database."""
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def get_db():
	"""Opens a new database connection if there is none yet for the
	current application context.
	"""

	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()

@app.cli.command('initdb')
def initdb_command():
	"""Initializes the database from the command line."""
	init_db()
	print("Initialialzed the database.")

@app.teardown_appcontext
def close_db(error):
	"""Closes the database again at the end of the request."""
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

# View functions

@app.route("/")
def show_entries():
	db = get_db()
	cur = db.execute('select title, text from entries order by id desc')
	entries = cur.fetchall()
	return render_template('show_entries.html', entries=entries)

@app.route("/add", methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	db = get_db()
	db.execute('insert into entries (title, text) values (? , ?)',
		[request.form['title'], request.form['text']])
	db.commit()
	flash("New entry was successfuly posted!")
	return redirect(url_for('show_entries'))

@app.route("/login", methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = "Invalid username."
		elif request.form['password'] != app.config['PASSWORD']:
			error = "Invalid password."
		else:
			session['logged_in'] = True
			flash("Login successful.")
			return redirect(url_for('show_entries'))
	return render_template('login.html', error=error)

@app.route("/logout")
def logout():
	session.pop('logged_in', None)
	flash("Logout successful.")
	return redirect(url_for('show_entries'))

# Run app directly

if __name__ == "__main__":
	app.run()