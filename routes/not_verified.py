from bottle import get, template

@get('/not_verified')
def _():
    return template('not_verified.html')