from bottle import default_app, error, get, post, redirect, response, request, run, static_file, template
import sqlite3
from icecream import ic
import bcrypt
import json
import git
import os
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
@get ("/images/<property_images>")
def _(property_images): 
    return static_file(property_images, "images")

# Serve notfound GIF
@get('/images/notfound.gif')
def _():
    return static_file('notfound.gif', 'images')
##############################
# Serve index-page
@get('/')
def _():
    try:
        db = x.db()
        q = db.execute("SELECT * FROM properties ORDER BY property_created_at LIMIT 0, 3")
        properties = q.fetchall()
        is_logged = False
        try:    
            x.validate_user_logged()
            is_logged = True
        except:
            pass
        ic(properties)
        print(properties)
        return template('index.html', properties=properties, is_logged=is_logged)
    except Exception as ex:
        ic(ex)
        return "No no noo, more lemon pledge"
    finally: 
        if "db" in locals(): db.close()

##############################
@get("/login")
def _():
    return template("login.html")
##############################
@get("/signup")
def _():
    return template("signup.html")
##############################
# Serve 404 Not Found
# @error(404)
# def _(error):
#     ic(error)
#     return template('error.html', is_logged=x.is_user_logged_in())
############################## admin
import routes.login
import routes.logout
import routes.not_verified
##############################
import routes.signup
import routes.verify
##############################
import routes.get_more_properties
##############################
import routes.profile
import routes.edit_user

##############################
@post('/a0eb0d133292439b941c063361315db6')
def git_update():
  repo = git.Repo('./exam_webdev')
  origin = repo.remotes.origin
  repo.create_head('main', origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
  origin.pull()
  return ""

##############################

if 'PYTHONANYWHERE_DOMAIN' in os.environ:
    application = default_app()
else:
    run(host="0.0.0.0", port=80, debug=True, reloader=True, interval=0)
