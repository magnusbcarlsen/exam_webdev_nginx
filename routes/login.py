from bottle import post, response, request
import x

##############################
@post("/login")
def _():
  try:
    # TODO: Validate the email and password
    user_email = x.validate_user_email()
    user_password = x.validate_user_password()
    db = x.db()
    sql = db.execute('SELECT * FROM users WHERE user_email = ? AND user_password = ?', (user_email, user_password))
    user = sql.fetchone()
    if user:
        response.set_cookie("name", user['user_name'], secret="my_secret", httponly=True)
        return """
            <template mix-redirect="/admin">
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
                <div id="error">User password invalid</div>
            </template>
        """
    if "user_email" in ex.args[1]:
        return """
            <template mix-target="#error" mix-replace>
                <div id="error">User email invalid</div>
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