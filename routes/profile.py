from bottle import get, template, redirect, HTTPResponse
from icecream import ic
import x

@get('/profile')
def _():
    try:
        user_data = x.get_cookie_data()
        
        if user_data is None:
            redirect('/login')

        db = x.db()

        user_q = db.execute('SELECT * FROM users WHERE user_pk = ?', (user_data['user_pk'],))
        user = user_q.fetchone()
    
        property_q = db.execute('SELECT * FROM properties WHERE property_user_fk = ?', (user_data['user_pk'],))
        users_properties = property_q.fetchall()

        return template('profile.html', user=user, users_properties=users_properties, is_logged=True, is_admin=False)
    except HTTPResponse:
        raise
    except Exception as ex:
        ic(ex)
    finally:
        if "db" in locals(): 
            db.close()