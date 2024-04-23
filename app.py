from bottle import default_app, error, get, post, redirect, response, run, static_file, template
import sqlite3
from icecream import ic
import bcrypt
import json
import git
import x

##############################
# Serve style
@get('/app.css')
def _():
    return static_file('app.css', '.')
##############################
# Serve Script
@get('/mixhtml.js')
def _():
    return static_file('mixhtml.js', '.')
##############################
# Serve favicon
@get('/favicon.ico')
def _():
    return static_file('favicon.ico', '.')
##############################
# Serve notfound GIF
@get('/images/notfound.gif')
def _():
    return static_file('notfound.gif', 'images')
##############################
# Serve index-page
@get('/')
def _():
    return template('index.html')
##############################
@get("/login")
def _():
    return template("login.html")
##############################
# Serve 404 Not Found
@error(404)
def _(error):
    return template('error.html')

##############################
@post('/a0eb0d133292439b941c063361315db6')
def git_update():
  repo = git.Repo('./exam_webdev')
  origin = repo.remotes.origin
  repo.create_head('main', origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
  origin.pull()
  return ""

##############################
try:
    import production
    application = default_app()
except:
    run(host="0.0.0.0", port=80, debug=True, reloader=True, interval=0)