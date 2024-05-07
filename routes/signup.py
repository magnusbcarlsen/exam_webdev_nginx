from bottle import post, request, template
from icecream import ic
import x
import bcrypt
import uuid

@post("/signup")
def _():
    try:


        random_id = uuid.uuid4().hex
        user_pk = random_id
        user_email = x.validate_user_email()
        user_username = x.validate_user_username()
        user_name = x.validate_user_name()
        user_last_name = x.validate_user_last_name()
        user_password = x.validate_new_user_password().encode()
        user_role_fk = x.validate_user_role()
        salt = bcrypt.gensalt()
        user_password_hashed = bcrypt.hashpw(user_password, salt)
        db = x.db()
        q = db.execute("INSERT INTO users(user_pk, user_email, user_username, user_name, user_last_name, user_password, user_role_fk) VALUES(?,?,?,?,?,?,?)", (user_pk, user_email, user_username, user_name, user_last_name, user_password_hashed, user_role_fk))
        db.commit()
        x.send_mail(user_email, user_email, "Verify your account", template("email_verification", key=user_pk))

        return f"""
                <template mix-target="#message" mix-replace>
                    <div id="message">
                        <p>Thank you for signing up {user_username}!</p>
                        <p>We have sent you an email to ({user_email}) to verify your account</p>
                    </div>

                </template>
                """

    except Exception as ex:
        ic(ex)
        return ex
    finally:
        if "db" in locals(): db.close()
