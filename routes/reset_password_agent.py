from bottle import post, request, template
from icecream import ic
import x
import bcrypt
import uuid

@post("/reset_password_agent")
def _():
    try:
        user_mail = x.validate_email()
        ic(user_mail)

        # TODO: Send email til provided email
        # Lav link, som peger til ny side med nyt password
        # Den skal kunne finde emailen i db og override det gamle password med det nye
        # Lav password og confirm password

        db = x.db()
        user_pk = db.execute("SELECT user_pk FROM users WHERE user_email = ?", (user_mail,)).fetchone()["user_pk"]
        db.commit()
        ic(user_pk)

        x.send_mail(user_mail, user_mail, "Reset your password", template("email_reset_password", key=user_pk))
        return f"""
                <template mix-target="#frm_reset_pw" mix-replace>
                <div>
                An email has been sent to {user_mail}
                </div>
                </template>
                """
    except Exception as ex:
        ic(ex)
        return ex
    finally:
        if "db" in locals(): db.close()