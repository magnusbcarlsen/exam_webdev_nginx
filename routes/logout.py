from bottle import get, response
import x

##############################
@get("/logout")
def _():
    x.delete_cookie("user")
    response.status = 303
    response.set_header('Location', '/')
    return