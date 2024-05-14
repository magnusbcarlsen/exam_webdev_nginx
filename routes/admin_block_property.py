from bottle import default_app, get, request, template, put
import sqlite3
from icecream import ic
import x

@put ("/block_property/<property_pk>")
def _(property_pk):
    try:
        db = x.db()
        q = db.execute("UPDATE properties SET property_is_blocked = '1' WHERE property_pk = ?", (property_pk,))
        db.commit()
        return f"""
            <template mix-target="[id='{property_pk}']" mix-replace>
                <form id="{property_pk}">
                    <button class="bg-black text-white border-solid"
                        mix-data="[id='{property_pk}'"
                        mix-put="/unblock_property/{property_pk}"
                        >
                        PROPERTY BLOCKED
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
        db.commit()
        return f"""
            <template mix-target="[id='{property_pk}']" mix-replace>
                <form id="{property_pk}">
                    <button class="bg-black text-cyan-50"
                        mix-data="[id='{property_pk}']"
                        mix-put="/block_property/{property_pk}"
                    >
                        Admin block
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
