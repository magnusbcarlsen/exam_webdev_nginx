from bottle import get, template
import sqlite3
from icecream import ic
import x

@get ("/all_users")
def _():
    try:
        db = x.db()
        q = db.execute("SELECT * FROM users ORDER BY user_created_at")
        users = q.fetchall()
        ic(users)
        return template("all_users", users=users)
        db.commit()
    except Exception as ex: 
        ic(ex)
        return "System under maintenance"
    finally:
        if "db" in locals():
            db.close() 