from bottle import get, put, request, response, template
from icecream import ic
import time
import json
import x

@put('/profile/<user_pk>')
def _(user_pk):
    try:
        user_email = x.validate_user_email()
        user_username = x.validate_user_username()
        user_name = x.validate_user_name()
        user_last_name = x.validate_user_last_name()

        db = x.db()
        q = db.execute('UPDATE users SET user_email = ?, user_username = ?, user_name = ?, user_last_name = ?, user_updated_at = CURRENT_TIMESTAMP WHERE user_pk = ?', (user_email, user_username, user_name, user_last_name, user_pk))
        db.commit()
        return f"""
            <template mix-target="#put_user_email" mix-replace>
                <input
                    id="put_user_email"
                    name="user_email"
                    class="w-full border"
                    type="text"
                    value={user_email}
                    mix-check="{{x.USER_EMAIL_REGEX}}"
                />
            </template>
            <template mix-target="#put_user_username" mix-replace>
                <input
                    id="put_user_username"
                    name="user_username"
                    class="w-full border"
                    type="text"
                    value={user_username}
                    mix-check="{{x.USER_USERNAME_REGEX}}"
                />
            </template>
            <template mix-target="#put_user_name" mix-replace>
                <input
                    id="put_user_name"
                    name="user_name"
                    class="w-full border"
                    type="text"
                    value={user_name}
                    mix-check="{{x.USER_NAME_REGEX}}"
                />
            </template>
            <template mix-target="#put_user_last_name" mix-replace>
                <input
                    id="put_user_last_name"
                    name="user_last_name"
                    class="w-full border"
                    type="text"
                    value={user_last_name}
                    mix-check="{{x.USER_LAST_NAME_REGEX}}"
                />
            </template>
        """
    except Exception as ex:
        ic(ex)
        return 'under maintenance'
    finally:
        if "db" in locals(): 
            db.close()
    