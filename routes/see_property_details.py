from bottle import get, template
from icecream import ic
import x

@get('/property/details/<property_pk>')
def _(property_pk):
    try:
        db = x.db()
        q = db.execute("SELECT * from properties WHERE property_pk = ?", (property_pk,))
        fetched_property = q.fetchone()

        property_images = fetched_property['property_images'].split(',')
        property_image_html = ''
        for property_image in property_images:
            property_image_html += f"""
                <div id="property_image_{property_image.split(".")[0]}" class="relative w-1/3 h-1/3 p-4 flex-shrink-0">
                    <img 
                        src='../images/{property_image}' 
                        alt='property image' 
                        class='property_image w-full aspect-square object-cover rounded-lg'
                    >
                </div>
            """
            
        return f"""
            <template mix-target="#modal_content" mix-replace>
                <div id="modal_content" class="flex flex-col gap-4">
                    <div class="flex items-center justify-start h-1/3 gap-6 overflow-y-scroll">
                        {property_image_html}
                    </div>
                    <div class="flex flex-col gap-2">
                        <p>{fetched_property['property_name']}</p>
                        <p>{fetched_property['property_description']}</p>
                        <p>{fetched_property['property_price_pr_night']}</p>
                        <p>{fetched_property['property_rating']}</p>
                        <p>{fetched_property['property_address']}</p>
                        <p>{fetched_property['property_country']}</p>
                        <p>{fetched_property['property_postal_code']}</p>
                    </div>
                </div>
            </template>
            <template mix-function="showModal"></template>
        """
    except Exception as ex:
        ic(ex)
    finally:
        if "db" in locals():
            db.close()

