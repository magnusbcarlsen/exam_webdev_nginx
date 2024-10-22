from bottle import get, template
from icecream import ic
import x
import json

@get("/properties/page/<page_number>")
def _(page_number): 
    try:
        try:
            page_number = int(page_number)
        except ValueError:
            return "Invalid page number"
        
        db = x.db()
        next_page = page_number + 1
        offset = (page_number - 1) * 4
        limit = 4
        html = ""
        is_admin = False
        is_partner = False
        is_customer = False

        try:
            # Fetch user role from cookie
            user_role = x.get_cookie_data().get('user_role_fk')
            is_customer = user_role == '0'
            is_partner = user_role == '1'
            is_admin = user_role == '2'
        except Exception as ex:
            ic(ex)
        
        cursor = db.cursor()

        # Adjusted query for PostgreSQL with proper parameterization
        if is_admin: 
            query = "SELECT * FROM properties ORDER BY property_created_at LIMIT %s OFFSET %s"
            cursor.execute(query, (limit, offset))
        else: 
            query = "SELECT * FROM properties WHERE property_is_blocked != %s AND property_deleted_at = %s ORDER BY property_created_at LIMIT %s OFFSET %s"
            cursor.execute(query, ('1', '0', limit, offset))
        
        properties = cursor.fetchall()

        # Generate HTML for each property
        for property in properties: 
            html += template("_property", property=property, is_admin=is_admin, is_partner=is_partner, is_customer=is_customer)

        # Handle 'Load More' button visibility based on property count
        btn_more = f"""
        <button id="more" class='block bg-accentCol border border-transparent rounded-lg text-white hover:border-accentCol hover:text-accentCol hover:bg-transparent duration-100 w-1/3 py-2 mx-auto m-4'
                mix-get="/properties/page/{next_page}"
                mix-default="more"
                mix-await="Please wait..."
            >
                Load more
            </button>
        """
        if len(properties) < 4: btn_more = ""

        # Return HTML and JSON for the properties
        return f"""
        <template mix-target="#property" mix-bottom>
            {html}
        </template>
        <template mix-target="#more" mix-replace>
            {btn_more}
        </template>
        <template mix-function="addProperties">{json.dumps(properties, default=x.datetime_converter)}</template>
        """

    except Exception as ex:
        ic(ex)
        return "System under maintenance."
    finally: 
        try:
            if "db" in locals():
                db.close()
        except Exception as ex:
            ic("Error closing database", ex)
