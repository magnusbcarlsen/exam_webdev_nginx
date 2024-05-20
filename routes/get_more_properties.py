from bottle import error, get, request, template
import sqlite3
from icecream import ic
import x
import json

@get ("/properties/page/<page_number>")
def _(page_number): 
    try:
        db = x.db()
        next_page = int(page_number) + 1
        offset = (int(page_number) - 1) * 3
        limit = 3
        html = ""
        is_admin = False
        try:
            is_admin = x.get_cookie_data()['user_role_fk'] == '2'
        except Exception as ex:
            ic(ex)
        if is_admin: 
            query = f"SELECT * FROM properties ORDER BY property_created_at LIMIT {limit} OFFSET {offset}"
        else: 
            query = f"SELECT * FROM properties WHERE property_is_blocked != '1' ORDER BY property_created_at LIMIT {limit} OFFSET {offset}"
        
        q = db.execute(query)
        properties = q.fetchall()
        
        
        for property in properties: html += template("_property", property=property, is_admin=is_admin)
        btn_more = f"""
        <button id="more" class='block bg-accentCol border border-transparent rounded-lg text-white hover:border-accentCol hover:text-accentCol hover:bg-transparent duration-100 w-1/3 py-2 mx-auto m-4'
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
        <template mix-function="addProperties">{json.dumps(properties)}</template>
        """
        
    except Exception as ex:
        ic(ex)
        return "no noo, more lemon pledge"
    finally: 
        if "db" in locals(): db.close()
    