from bottle import post, put
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
                    <button class="bg-accentCol border border-transparent rounded-lg text-white hover:border-accentCol hover:text-accentCol hover:bg-white duration-100 w-full py-2"
                        mix-data="[id='{property_pk}']"
                        mix-put="/unbook_property/{property_pk}"
                    >
                        unbook property
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
        db.execute("UPDATE bookings SET booking_deleted_at = CURRENT_TIMESTAMP WHERE booking_property_fk = ?", (property_pk,))
        db.execute("UPDATE properties SET property_booking_fk = 0 WHERE property_pk = ?", (property_pk,))
        db.commit()
        return f"""
            <template mix-target="[id='{property_pk}']" mix-replace>
                <form id="{property_pk}">
                    <button class="bg-accentCol border border-transparent rounded-lg text-white hover:border-accentCol hover:text-accentCol hover:bg-white duration-100 w-full py-2"
                        mix-data="[id='{property_pk}']"
                        mix-post="/book_property/{property_pk}"
                    >
                        book property
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





