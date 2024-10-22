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
            return

        db = x.db()
        cursor = db.cursor()

        cursor.execute('SELECT * FROM users WHERE user_pk = %s AND user_role_fk = %s', (user_data['user_pk'], user_data['user_role_fk']))
        user = cursor.fetchone()

        if user['user_role_fk'] == '2':
            cursor.execute('SELECT * FROM users WHERE user_role_fk != %s', ('2',))  # Fix: compare user_role_fk as string
            user_list = cursor.fetchall()
            cursor.execute("SELECT * FROM properties ORDER BY property_created_at")
            properties = cursor.fetchall()
            db.commit()

            return template('profile_admin.html', user_list=user_list, is_logged=True, is_admin=True, properties=properties)

        cursor.execute('SELECT * FROM properties WHERE property_user_fk = %s', (user_data['user_pk'],))
        users_properties = cursor.fetchall()

        return template('profile.html', user=user, users_properties=users_properties, is_logged=True, is_admin=False, in_profile=True)
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
        <template mix-target='#modal_content' mix-replace>
            <div id="modal_content" class="flex flex-col gap-4">
                <div>
                    <h2>Are you sure you want to delete your profile?</h2>
                    <p>Write your email and press 'confirm' to delete your profile.</p>
                </div>
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
                        autofocus
                    />
                    <div id="error_message"></div>
                    <div id="modal_buttons" class="flex flex-row gap-4">
                        <button
                            id='confirm_delete_button'
                            class="flex items-center justify-center bg-accentCol text-white"
                            mix-put="/profile"
                            mix-data="#delete_form"
                        >
                            Confirm deletion
                        </button>
                        <button id="modal_close" class="flex items-center justify-center border border-pink-400 bg-white p-4">
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </template>
        <template mix-function="showModal"></template>
    """

@put('/profile')
def _():
    try:
        user_data = x.get_cookie_data()

        if user_data['user_email'] == x.validate_user_email():
            db = x.db()
            cursor = db.cursor()
            cursor.execute('UPDATE users SET user_deleted_at = CURRENT_TIMESTAMP WHERE user_pk = %s', (user_data['user_pk'],))
            x.delete_cookie('user')
            x.send_mail(user_data['user_email'], 'admin@bottleBnB.com', "Profile has been deleted", template('email_profile_restore', user_pk=user_data['user_pk']))
            db.commit()
            return """
                <template mix-redirect="/user_deleted" is_logged=False>
                </template>
                <template mix-function="closeModal"></template>
            """
        else:
            return """
                <template mix-target="#error_message" mix-replace>
                    <div id="error-message" class="flex justify-center rounded-md">
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