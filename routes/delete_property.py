from bottle import get, put, template
from icecream import ic
import x

@put('/property/delete/<property_pk>')
def _(property_pk):
    try:
        db = x.db()
        q = db.execute('UPDATE properties SET property_deleted_at = CURRENT_TIMESTAMP WHERE property_pk = ?', (property_pk,))
        db.commit()
        return f"""
            <template mix-target="#property_{property_pk}" mix-replace>
                <div class="flex items-center justify-center" mix-ttl="1500">
                    <p>Property deleted!</p>
                </div>
            </template>
            <template mix-function="closeModal"></template>
        """
    except Exception as ex:
        ic(ex)
    finally:
        if "db" in locals():
            db.close()

@get('/property/delete-pop-up/<property_pk>')
def _(property_pk):
    return f"""
        <template mix-target="#modal_content" mix-replace>
        <div id="modal_content">
            <h2>Are you sure you want to delete your property?</h2>
            <div>
                <button id="modal_close" class="border border-pink-400 bg-white p-4">Cancel</button>
                <form id='delete_property'>
                    <button mix-put="/property/delete/{property_pk}" mix-data='#delete_property' class="p-4">Confirm Deletion</button>
                </form>
            </div>
        </div>
        </template>
        <template mix-function="showModal"></template>
    """