from bottle import get, template
import x
from icecream import ic


@get("/verify/<key>")
def _(key):
    try:
        db = x.db()
        q = db.execute("UPDATE users SET user_is_verified = 1 WHERE user_pk = ?", (key,))
        user_name = db.execute("SELECT user_name FROM users WHERE user_pk = ?", (key,)).fetchone()["user_name"]
        db.commit()
        return template("login")
    except Exception as ex:
        ic(ex)
        return ex
    finally:
        if "db" in locals(): db.close()