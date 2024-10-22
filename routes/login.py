from bottle import post, response, request, template
from icecream import ic
import bcrypt
import json
import x
import psycopg2

##############################
@post("/login")
def _():
    try:
        user_email = x.validate_user_email()
        ic("User email validated:", user_email)
        
        user_password = x.validate_user_password()
        ic("User password validated:", user_password)
        
        db = x.db()
        cursor = db.cursor()
        ic("Database connection established")
        
        cursor.execute('SELECT * FROM users WHERE user_email = %s', (user_email,))
        user = cursor.fetchone()
        ic("User fetched from DB:", user)
        
        if user:
            # try:
            #     # Ensure the stored password is a valid bcrypt hash
            #     stored_password_bytes = user["user_password"].encode()
            #     if not bcrypt.checkpw(user_password.encode(), stored_password_bytes): 
            #         raise Exception("Invalid credentials", 400)
            # except ValueError as e:
            #     ic(e)
            #     raise Exception("Invalid stored password format", 500)
            if user['user_is_blocked'] == '1':
                return """
                        <template mix-redirect="/user_blocked">
                        </template>
                    """
            elif '1' in user['user_is_verified']:
                if user['user_deleted_at'] != '0':
                    return f"""
                        <template mix-redirect="/profile_restore_agent/{user['user_pk']}">
                        </template>
                    """
                else:
                    for key in user:
                        if isinstance(user[key], bytes):
                            user[key] = user[key].decode('utf-8')
                    user_data = json.dumps(user, default=x.datetime_converter)
                    response.set_cookie("user", user_data, secret=x.COOKIE_SECRET, httponly=True, secure=x.is_cookie_https())
                    return """
                        <template mix-redirect="/" is_logged=True>
                        </template>
                    """
            else:
                return """
                    <template mix-redirect="/not_verified" is_logged=False>
                    </template>
                """
        else:
            return """
                <template mix-target="#error" mix-replace>
                    <div id="error">User doesn't exist</div>
                </template>
            """
    except Exception as ex:
        ic("Error occurred:", ex)
        if len(ex.args) > 1 and "user_password" in ex.args[1]:
            return """
                <template mix-target="#error" mix-replace>
                    <div id="error">User password invalid</div>
                </template>
            """
        if len(ex.args) > 1 and "user_email" in ex.args[1]:
            return """
                <template mix-target="#error" mix-replace>
                    <div id="error">User email invalid</div>
                </template>
            """
        # Return more detailed error message for debugging
        return f"""
            <template mix-target="#error" mix-replace>
                <div mix-ttl="2000">System under maintenance: {str(ex)}</div>
            </template>
        """
    finally:
        if "db" in locals():
            db.close()
