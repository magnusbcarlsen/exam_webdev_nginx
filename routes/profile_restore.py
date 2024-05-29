from bottle import get, template
from icecream import ic
import x

@get('/profile_restore/<user_pk>')
def _(user_pk):
    try:
        db = x.db()
        q = db.execute('UPDATE users SET user_deleted_at = 0 WHERE user_pk = ?', (user_pk,))
        db.commit()

        return"""
            <template mix-target="#message_header" mix-replace>
                <h1 id="message_header" class="text-accentCol text-5xl">
		            Your profile has been restored!
	            </h1>
            </template>
            <template mix-target="#message_content" mix-replace>
                <p id="message_content" class="text-xl">
                    Proceed to log in with your restored profile
                </p>
            </template>
        """
    except Exception as ex:
        ic(ex)
    finally:
        if "db" in locals():
            db.close()

@get('/profile_restore/email/<user_pk>')
def _(user_pk):
    try:
        db = x.db()
        q = db.execute('UPDATE users SET user_deleted_at = 0 WHERE user_pk = ?', (user_pk,))
        db.commit()

        return template('profile_restored')
    except Exception as ex:
        ic(ex)
    finally:
        if "db" in locals():
            db.close()