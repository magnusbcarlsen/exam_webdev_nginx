from bottle import put, template
import sqlite3
from icecream import ic
import x

@put ("/block_property/<property_pk>")
def _(property_pk):
    try:
        db = x.db()
        q = db.execute("UPDATE properties SET property_is_blocked = '1' WHERE property_pk = ?", (property_pk,))

        q_email = db.execute("SELECT users.user_email FROM properties JOIN users ON properties.property_user_fk = users.user_pk WHERE properties.property_pk = ?", (property_pk,))

        user_email = q_email.fetchone()['user_email']
        ic(user_email)

        db.commit()

        x.send_mail("jachobwesth@gmail.com", "jachobwesth@gmail.com", "One of your properties has been suspended", template("email_profile_blocked"))

        return f"""
            <template mix-target="[id='{property_pk}']" mix-replace>
                <form id="{property_pk}">
                    <button class="bg-black text-cyan-50 px-1 py-1 h-fit"
                        mix-data="[id='{property_pk}'"
                        mix-put="/unblock_property/{property_pk}"
                        >
                        UNBLOCK
                    </button>
                    
                </form>
            </template>
        """
    except Exception as ex:
        ic(ex)
        return ex
    finally: 
        if "db" in locals():
            db.close()

@put ("/unblock_property/<property_pk>")
def _(property_pk):
    try:
        db = x.db()
        q = db.execute("UPDATE properties SET property_is_blocked = '0' WHERE property_pk = ?", (property_pk,))
        q_email = db.execute("SELECT users.user_email FROM properties JOIN users ON properties.property_user_fk = users.user_pk WHERE properties.property_pk = ?", (property_pk,))

        user_email = q_email.fetchone()['user_email']
        ic(user_email)

        db.commit()

        x.send_mail("jachobwesth@gmail.com", "jachobwesth@gmail.com", "One of your properties has been unblocked", template("email_profile_blocked"))
        return f"""
            <template mix-target="[id='{property_pk}']" mix-replace>
                <form id="{property_pk}">
                    <button class="bg-black text-cyan-50 px-6 py-1 h-fit"
                        mix-data="[id='{property_pk}']"
                        mix-put="/block_property/{property_pk}"
                    >
                        BLOCK
                    </button>
                </form>
            </template>
        """
    except Exception as ex:
        ic(ex)
        return ex
    finally: 
        if "db" in locals():
            db.close()
