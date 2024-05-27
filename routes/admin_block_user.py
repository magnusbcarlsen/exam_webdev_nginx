from bottle import default_app, get, request, template, put
import sqlite3
import x
from icecream import ic

@put ("/block_user/<user_pk>")
def _(user_pk): 
    try:
        db = x.db()
        q = db.execute("UPDATE users SET user_is_blocked = '1' WHERE user_pk = ?", (user_pk,))
        db.commit()
        email_q = db.execute("SELECT user_email FROM users WHERE user_pk = ?", (user_pk,))
        user_email = email_q.fetchone()
        x.send_mail(user_email, user_email, "Your profile has been blocked", 
        """<p>Your profile has been blocked</p>""")
        
        return f"""
            <template mix-target="[id='{user_pk}']" mix-replace>
                <form id="{user_pk}">
                    <button class="bg-black text-white"
                        mix-data="[id='{user_pk}'"
                        mix-put="/unblock_user/{user_pk}"
                        >
                        Block user?
                    </button>
                </form>
            </template>
        """
    except Exception as ex: 
        ic(ex)
        return ex
    finally: 
        if "db" in locals(): 
            db.close()

@put ("/unblock_user/<user_pk>")
def _(user_pk): 
    try:
        db = x.db()
        q = db.execute("UPDATE users SET user_is_blocked = '0' WHERE user_pk = ?", (user_pk,))
        db.commit()
        return f"""
            <template mix-target="[id='{user_pk}']" mix-replace>
                <form id="{user_pk}">
                    <button class="bg-black text-white"
                        mix-data="[id='{user_pk}'"
                        mix-put="/block_user/{user_pk}"
                        >
                        USER BLOCKED
                    </button>
                </form>
            </template>
        """
    except Exception as ex: 
        ic(ex)
        return ex
    finally: 
        if "db" in locals(): 
            db.close()