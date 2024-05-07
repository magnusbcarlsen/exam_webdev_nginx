from bottle import error, get, request, template
import sqlite3
from icecream import ic
import x

@get ("/properties/page/<page_number>")
def _(page_number): 
    try:
        db = x.db()
        next_page = int(page_number) + 1
        offset = (int(page_number) - 1) * 3
        q = db.execute(f"""
        SELECT * FROM properties ORDER BY property_created_at LIMIT 3 OFFSET {offset}
        """)
        properties = q.fetchall()
        ic(properties)
        html = ""
        is_admin = False
        try:
            is_admin = x.get_cookie_data()['user_role_fk'] == '2'
        except:
            pass
        for property in properties: html += template("_property", property=property, is_admin=is_admin)
        btn_more = f"""
        <button id="more" class="block w-1/3 text-white bg-dragon-fruit mx-auto m-4"
                mix-get="/properties/page/{next_page}"
                mix-default="more"
                mix-await="Please wait..."
            >
                Load more
            </button>  
        """
        if len(properties) < 3: btn_more = ""
        
        return f"""
        <template mix-target="#property" mix-bottom>
            {html}
        </template>
        <template mix-target="#more" mix-replace>
            {btn_more}
        </template>
        """
        
    except Exception as ex:
        ic(ex)
        return "no noo, more lemon pledge"
    finally: 
        if "db" in locals(): db.close()
    