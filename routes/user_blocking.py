from bottle import get, put, template
from icecream import ic
import x


@get ("/user_blocked")
def _():
    return template('user_blocked.html')
##############################
@put("/unblock_user/<user_pk>")
def _(user_pk):
    try:
        ic(user_pk)
        db = x.db()
        q = db.execute("UPDATE users SET user_is_blocked = '0' WHERE user_pk = ?", (user_pk,))
        db.commit()
        return f"""
            <template mix-target="#user_row_{user_pk}" mix-replace>
                <form id="user_row_{user_pk}">
                    <button id="{user_pk}_block_btn" mix-data="#user_row_{user_pk}" mix-put="/block_user/{user_pk}" class="bg-black text-cyan-50 px-1 py-1 h-fit">BLOCK</button>
                </form>
            </template>
""" 

    except Exception as ex:
        ic(ex)
        return ex
    finally:
         if "db" in locals():
            db.close()
##############################
@put("/block_user/<user_pk>")
def _(user_pk):
    try:
        ic(user_pk)
        db = x.db()
        q = db.execute("UPDATE users SET user_is_blocked = '1' WHERE user_pk = ?", (user_pk,))
       
        q_mail = db.execute("SELECT user_email FROM users WHERE user_pk = ?", (user_pk,))

        user_email = q_mail.fetchone()
        db.commit()
        
        x.send_mail("jachobwesth@gmail.com", "jachobwesth@gmail.com", "Your account has been suspended", template("email_profile_blocked", key=user_pk))
        return f"""
            <template mix-target="#user_row_{user_pk}" mix-replace>
                <form id="user_row_{user_pk}">
                    <button id="{user_pk}_block_btn" mix-data="#user_row_{user_pk}" mix-put="/unblock_user/{user_pk}" class="bg-black text-cyan-50 px-3 py-1 h-fit" >UNBLOCK</button>
                </form>
            </template>
""" 

    except Exception as ex:
        ic(ex)
        return ex
    finally:
         if "db" in locals():
            db.close()

