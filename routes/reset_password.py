from bottle import put, template
import x
import bcrypt
from icecream import ic

@put("/reset_password/<key>")
def _(key):
    try:
        ic(key)
        user_password = x.validate_new_user_password().encode()
        ic(user_password)

        salt = bcrypt.gensalt()
        user_password_hashed = bcrypt.hashpw(user_password, salt)
        ic(user_password_hashed)

        db = x.db()
        q = db.execute("UPDATE users SET user_password = ? WHERE user_pk = ?", (user_password_hashed, key))
        db.commit()

    except Exception as ex:
        ic(ex)
        return ex
    finally:
        if "db" in locals(): db.close()     