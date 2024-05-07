from bottle import get, template
from icecream import ic
import x

@get('/profile')
def _():
    user = x.get_cookie_data()
    is_logged = False
    try:    
        x.validate_user_logged()
        is_logged = True
    except:
        pass
        
    return template('profile.html', user=user, is_logged=is_logged)