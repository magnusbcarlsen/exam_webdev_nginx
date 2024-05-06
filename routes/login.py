from bottle import post, response, request
from icecream import ic
import x

##############################
@post("/login")
def _():
  try:
    # TODO: check for if input is an email or username, then validate accordingly
    
    x.validate_user_email()
    x.validate_user_password()

    user_username_or_email = request.forms.get("user_username_or_email")
    user_password = request.forms.get("user_password")
    db = x.db()
    sql = db.execute('SELECT * FROM users WHERE (user_email = ? OR user_username = ?) AND user_password = ?', (user_username_or_email, user_username_or_email, user_password))
    user = sql.fetchone()
    ic(user);
    if user:
        response.set_cookie("name", user['user_username'], secret="my_secret", httponly=True)
        return """
            <template mix-redirect="/">
            </template>
        """
    else:
        return """
            <template mix-target="#error" mix-replace>
                <div id="error">User doesn't exist</div>
            </template>
        """
  except Exception as ex:
    print(f"------------------------------------{ex}------------------------------------")
    if "user_password" in ex.args[1]:
        return """
            <template mix-target="#error" mix-replace>
                <div id="error">User password is invalid</div>
            </template>
        """
    if "user_email" or "user_username" in ex.args[1]:
        return """
            <template mix-target="#error" mix-replace>
                <div id="error">User email or username is invalid</div>
            </template>
        """

    return """
        <template mix-target="#error" mix-replace>
            <div  mix-ttl="2000">System under maintainence</div>
        </template>
    """
  finally:
    if "db" in locals():
        db.close()