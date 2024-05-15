from bottle import get, HTTPResponse, put, redirect, template
from icecream import ic
import html
import x

@get('/profile')
def _():
    try:
        user_data = x.get_cookie_data()
        
        if user_data is None:
            redirect('/login')

        db = x.db()

        user_q = db.execute('SELECT * FROM users WHERE user_pk = ? AND user_role_fk = ?', (user_data['user_pk'],user_data['user_role_fk']))
        user = user_q.fetchone()

        if user['user_role_fk'] == '2':
            user_list_q = db.execute('SELECT * FROM users')
            user_list = user_list_q.fetchall()
            return template('profile_admin.html', user_list=user_list, is_logged=True)
            
    
        property_q = db.execute('SELECT * FROM properties WHERE property_user_fk = ?', (user_data['user_pk'],))
        users_properties = property_q.fetchall()

        return template('profile.html', user=user, users_properties=users_properties, is_logged=True, is_admin=False)
    except HTTPResponse:
        raise
    except Exception as ex:
        ic(ex)
    finally:
        if "db" in locals(): 
            db.close()

@get('/profile/delete-pop-up')
def _():
    return f"""
        <template mix-target='#delete_user_button' mix-after>
            <form
                id="delete_form"
                class="flex flex-col gap-2 w-full"
            >
                <input
                    name="user_email"
                    class="w-full border"
                    type="text"
                    placeholder="email"
                    mix-check="{html.escape(x.USER_EMAIL_REGEX)}"
                />
                <button
                    id='confirm_delete_button'
                    class="w-full bg-dragon-fruit text-white"
                    mix-put="/profile"
                    mix-data="#delete_form"
                >
                    Confirm deletion
                </button
            </form>
            <div id="error_message"></div>
        </template>
    """

@put('/profile')
def _():
    try:
        user_data = x.get_cookie_data()

        if user_data['user_email'] == x.validate_user_email():
            db = x.db()
            q = db.execute('UPDATE users SET user_deleted_at = CURRENT_TIMESTAMP WHERE user_pk = ?', (user_data['user_pk'],))
            x.delete_cookie('user')
            x.send_mail(user_data['user_email'], 'admin@bottleBnB.com', "Profile has been deleted", template('email_profile_restore', user_pk=user_data['user_pk']))
            db.commit()
            return """
                <template mix-redirect="/user_deleted" is_logged=False>
                </template>
            """
        else:
            return """
                <template mix-target="#error_message" mix-replace>
                    <div class='flex justify-center bg-red-400 rounded-md'>
                        <p>Email is invalid, please write your own email</p>
                    </div>
                </template>
            """
        
    except HTTPResponse:
        raise
    except Exception as ex:
        ic(ex)
    finally:
        if "db" in locals():
            db.close()