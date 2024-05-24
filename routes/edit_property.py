from bottle import get, put, template
from icecream import ic
import x

@put('/property/edit/<property_pk>')
def _(property_pk):
    ic(property_pk)
    # try:
    #     db = x.db()
    # except Exception as ex:

    # finally:
    #     if "db" in locals():
    #         db.close()

@get('/property/edit-pop-up/<property_pk>')
def _(property_pk):
    try:
        db = x.db()
        q = db.execute("SELECT * FROM properties WHERE property_pk = ?", (property_pk,))
        property_to_edit = q.fetchone();
        property_images = property_to_edit['property_images'].split(',')
        property_image_html = ''
        for property_image in property_images:
            ic(property_image)
            property_image_html += f"""<img src='../images/{property_image}' alt='property image' class='property_image w-1/4 aspect-square object-cover rounded-lg'>"""
            ic(property_image_html)
        return f"""
        <template mix-target="#modal_content" mix-replace>
            <div id="modal_content" class="flex flex-col gap-4">
                <div class="flex flex-row gap-4">
                    {property_image_html}
                </div>
                <form id='delete_property'>
                    <div id="form_fields" class="flex flex-col gap-y-1">
                    <div class="flex flex-col gap-y-1">
                        <label class="text-dragon-fruit" for="property_name">
                            <h2>Property name (3 - 30 characters)</h2>
                        </label>
                        <input
                            id="property_name"
                            name="property_name"
                            class="w-full border"
                            type="text"
                            placeholder="ex. Cozy Village House"
                            mix-check="{x.PROPERTY_NAME_REGEX}"
                        />
                    </div>
                    <div class="flex flex-col gap-y-1">
                        <label class="text-dragon-fruit" for="property_description">
                            <h2>Property Description (min 10 characters)</h2>
                        </label>
                        <input
                            id="property_description"
                            name="property_description"
                            class="w-full border"
                            type="text"
                            placeholder="ex. Very cozy house down by the river..."
                            mix-check="{x.PROPERTY_DESCRIPTION_REGEX}"
                        />
                    </div>
                    <div class="flex flex-col gap-y-1">
                        <label class="text-dragon-fruit" for="property_address">
                            <h2>Property Address</h2>
                        </label>
                        <input
                            id="property_address"
                            name="property_address"
                            class="w-full border"
                            type="text"
                            placeholder="ex. Street Name 123"
                            mix-check="{x.PROPERTY_ADDRESS_REGEX}"
                        />
                    </div>
                    <div class="flex flex-col gap-y-1">
                        <label class="text-dragon-fruit" for="property_country">
                            <h2>Property Country</h2>
                        </label>
                        <input
                            id="property_country"
                            name="property_country"
                            class="w-full border"
                            type="text"
                            placeholder="ex. Danmark"
                            mix-check="{x.PROPERTY_COUNTRY_REGEX}"
                        />
                    </div>
                    <div class="flex flex-col gap-y-1">
                        <label class="text-dragon-fruit" for="property_postal_code">
                            <h2>Property postal code</h2>
                        </label>
                        <input
                            id="property_postal_code"
                            name="property_postal_code"
                            class="w-full border"
                            type="text"
                            placeholder="ex. 1234"
                            mix-check="{x.PROPERTY_POSTAL_CODE_REGEX}"
                        />
                    </div>
                    <div class="flex flex-col gap-y-1">
                        <label class="text-dragon-fruit" for="property_price_pr_night">
                                <h2>Property postal code</h2>
                        </label>
                        <input
                            id="property_price_pr_night"
                            name="property_price_pr_night"
                            class="w-full border"
                            type="text"
                            placeholder="ex. 1234"
                            mix-check="{x.PROPERTY_PRICE_PER_NIGHT_REGEX}"
                        />
                    </div>
                    <label for="property_images">Property Images (You must select at least 3 images) </label>
                    <input
                        name="property_images"
                        class="file-input"
                        type="file"
                        accept="image/*"
                        multiple
                    />
                    </div>
                    <div id="modal_buttons" class="flex flex-row gap-4">
                        <button class="flex items-center justify-center border p-4 bg-red-500 text-white" mix-put="/property/edit/{property_pk}" mix-data='#delete_property'>Confirm Deletion</button>
                        <button id="modal_close" class="flex items-center justify-center border p-4">Cancel</button>
                    </div>
                </div>
                </form>
            </div>
        </template>
        <template mix-function="showModal"></template>
    """
    except Exception as ex:
        ic(ex)
    finally:
        if "db" in locals():
            db.close()