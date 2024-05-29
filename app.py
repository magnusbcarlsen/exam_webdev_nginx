from bottle import default_app, error, get, HTTPResponse, post, put, redirect, response, request, run, static_file, template
import sqlite3
from icecream import ic
import bcrypt
import json
import git
import os
import x
import credentials

import routes.login
import routes.logout
import routes.not_verified
##############################
import routes.signup
import routes.verify
import routes.reset_password_agent
import routes.reset_password
##############################
import routes.get_more_properties
import routes.delete_property
##############################
import routes.profile
import routes.edit_user
import routes.user_deleted
import routes.profile_restore
##############################
import routes.see_property_details
import routes.add_property
import routes.admin_block_property
import routes.edit_property
import routes.book_property
##############################
import routes.user_blocking
##############################

# Serve style
@get('/app.css')
def _():
    return static_file('app.css', '.')
##############################
@get("/app.js")
def _():
    return static_file("app.js", ".")
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
@get("/images/<property_images>")
def _(property_images): 
    return static_file(property_images, "images")
##############################
# db route
@get('/properties')
def _():
    db = x.db()
    q = db.execute("SELECT * FROM properties ORDER BY property_created_at LIMIT 0, 3")
    properties = q.fetchall()
    db.commit()
    return json.dumps(properties)
##############################
# get mapbox token
@get('/mapbox_token')
def _():
    token = credentials.mapbox_token
    return json.dumps({'mapbox_token': token})


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
        is_logged = False
        is_admin = False
        is_customer = False
        is_partner = False
        try:    
            x.validate_user_logged()
            is_logged = True
        except:
            pass
  
        try:
            user_role = x.get_cookie_data()['user_role_fk']
            is_customer = user_role == '0'
            is_partner = user_role == '1'
            is_admin = user_role == '2'

            # is_customer_partner = x.get_cookie_data()['user_role_fk'] == ['0', '1']
            # is_admin = x.get_cookie_data()['user_role_fk'] == '2'
        except Exception as ex:
            ic(ex)
        query = "SELECT * FROM properties WHERE property_is_blocked != '1' ORDER BY property_created_at LIMIT 0, 3"
        
        q = db.execute(query)
        properties = q.fetchall()
        if is_admin:
            user_list_q = db.execute('SELECT * FROM users WHERE user_role_fk != 2')
            user_list = user_list_q.fetchall()
            properties_q = db.execute("SELECT * FROM properties ORDER BY property_created_at")
            properties = properties_q.fetchall()
            db.commit()

            return template('profile_admin.html', user_list=user_list, is_logged=True, properties=properties)
        else: 
            return template('index.html', properties=properties, is_logged=is_logged,   is_admin=is_admin, mapbox_token= credentials.mapbox_token)
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
@get("/profile_restore_agent/<user_pk>")
def _(user_pk):
    return template("profile_restore_agent.html", user_pk=user_pk)
##############################
@get("/reset_password_agent")
def _():
    return template("reset_password_agent.html")
##############################
@get("/reset_password_form/<key>")
def _(key):
    return template("reset_password_form.html", key=key)

##############################
# Serve 404 Not Found
# @error(404)
# def _(error):
#     ic(error)
#     return template('error.html', is_logged=x.is_user_logged_in())
############################## admin
@get("/db/reset")
def _():
    try:
        x.reset_db()
        redirect("/")
    except HTTPResponse:
        raise
##############################
@get("/db/seed")
def _():
    try:
        x.seed_db()
        redirect("/")
    except HTTPResponse:
        raise
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
