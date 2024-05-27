from bottle import default_app, error, get, post, put, template
import uuid
import x
from icecream import ic

@post ("/book_property/<property_pk>")
def _(property_pk):
    try:
        db = x.db()
        user_pk = x.get_cookie_data()['user_pk']
        random_id = uuid.uuid4().hex
        booking_pk = random_id
        q = db.execute("INSERT INTO bookings (booking_pk, booking_user_fk, booking_property_fk) VALUES (?, ?, ?)", (booking_pk, user_pk, property_pk))
        db.commit()
        return f"""
            <template mix-target="[id='{property_pk}']" mix-replace>
                <form id="{property_pk}">
                    <button class="bg-black text-cyan-50"
                        mix-data="[id='{property_pk}']"
                        mix-put="/unbook_property/{property_pk}"
                    >
                        PROPERTY BOOKED
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


@put ("/unbook_property/<property_pk>")
def _(property_pk):
    try:
        db = x.db()
        user_pk = x.get_cookie_data()['user_pk']
        random_id = uuid.uuid4().hex
        booking_pk = random_id
        q = db.execute("UPDATE bookings SET booking_deleted_at = CURRENT_TIMESTAMP WHERE booking_pk = ?", (booking_pk,))
        db.commit()
        return f"""
            <template mix-target="[id='{property_pk}']" mix-replace>
                <form id="{property_pk}">
                    <button class="bg-black text-cyan-50"
                        mix-data="[id='{property_pk}']"
                        mix-post="/book_property/{property_pk}"
                    >
                        BOOK PROPERTY
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





