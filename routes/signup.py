from bottle import post, request
from icecream import ic
import x
import bcrypt
import uuid

@post("/signup")
def _():
    try:
        # TODO: Get forms data, validate and parse into database

        random_id = uuid.uuid4().hex
        user_pk = random_id
        user_email = x.validate_email()
        user_username = x.validate_user_username()
        user_name = x.validate_user_name()
        user_last_name = x.validate_last_name()
        user_password = x.validate_password().encode()
        user_role_fk = x.validate_role()

        salt = bcrypt.gensalt()
        user_password_hashed = bcrypt.hashpw(user_password, salt)

        db = x.db()
        q = db.execute("INSERT INTO users(user_pk, user_email, user_username, user_name, user_last_name, user_password, user_role_fk) VALUES(?,?,?,?,?,?,?)", (user_pk, user_email, user_username, user_name, user_last_name, user_password, user_role_fk))
        db.commit()

        return """
                <template mix-target="#message" mix-replace>
                <div id="message">
                fisse
                </div>

                </template>
                """

    except Exception as ex:
        ic(ex)
        return ex
    finally:
        pass
