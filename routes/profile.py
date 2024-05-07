from bottle import get, template
from icecream import ic
import x

@get('/profile')
def _():
    try:
        user_pk = x.get_cookie_data()['user_pk']
        db = x.db()
        q = db.execute('SELECT * FROM users WHERE user_pk = ?', (user_pk,))
        user = q.fetchone()
        return template('profile.html', user=user)
    except Exception as ex:
        ic(ex)
    finally:
        if "db" in locals(): 
            db.close()