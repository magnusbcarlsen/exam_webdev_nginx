from bottle import get, template

@get('/user_deleted')
def _():
    return template('user_deleted.html')