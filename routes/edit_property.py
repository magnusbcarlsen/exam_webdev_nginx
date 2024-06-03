from bottle import get, put, template
from icecream import ic
import html
import os
import x

@put('/property/remove_picture/<deleted_image>/<property_pk>')
def _(deleted_image, property_pk):
    try:
        db = x.db()
        property_query = db.execute('SELECT * FROM properties WHERE property_pk = ?', (property_pk,))
        property_to_edit = property_query.fetchone()

        new_property_images = x.remove_image_from_property(property_to_edit['property_images'], deleted_image)
        
        db.execute("UPDATE properties SET property_images = ? WHERE property_pk = ?", (new_property_images, property_pk))
        db.commit()

        return f"""
            <template mix-target="#property_image_{deleted_image.split('.')[0]}" mix-replace>
                <div class="flex items-center justify-center w-1/3 h-1/3 p-4 flex-shrink-0" mix-ttl="1500">
                    <p>Image deleted!</p>
                </div>
            </template>
        """
    except Exception as ex:
        ic(ex)
    finally:
        if "db" in locals():
            db.close()

@put('/property/edit/<property_pk>')
def _(property_pk):
    try:
        property_name = x.validate_property_name()
        property_description = x.validate_property_description()
        property_address = x.validate_property_address()
        property_country = x.validate_property_country()
        property_postal_code = x.validate_property_postal_code()
        property_price_pr_night = x.validate_property_price_pr_night()
        property_images = x.validate_property_images()

        db = x.db()
        images_q = db.execute('SELECT property_images FROM properties WHERE property_pk = ?', (property_pk,))
        old_property_images = images_q.fetchone()

        filenames = []
        for image in property_images:
            filename = image.filename
            filenames.append(filename)
            directory_path = 'exam_webdev/images/' if x.is_on_production() else 'images'
            file_path = os.path.join(directory_path, filename)
            if(filename == 'empty'):
                pass
            else:
                image.save(file_path, overwrite=True)
            
        filenames_str = ",".join(filenames)

        
        # 2. Combine strings
        # Concatenating strings to check their length
        old_images = old_property_images['property_images']
        combined_images = ''
        if (filenames_str == 'empty'):
            combined_images = old_images
        else:
            combined_images = old_images + ',' + filenames_str

        # 3. Check lengths
        if len(combined_images.split(',')) > 6:
            return f"""
                <template mix-target='#property_error_message' mix-replace>
                    <div id="property_error_message" class="w-full p-2 border border-red-500 bg-pink-100">
                        <p class="text-red-500">Too many images! Max 6 images</p>
                    </div>
                </template>
            """
        
        if len(combined_images.split(',')) < 3:
            return f"""
                <template mix-target='#property_error_message' mix-replace>
                    <div id="property_error_message" class="w-full p-2 border border-red-500 bg-pink-100">
                        <p class="text-red-500">Your property needs at least 3 images</p>
                    </div>
                </template>
            """
        # 4. Profit

        db.execute('''UPDATE properties SET 
            property_name = ?, property_description = ?, 
            property_address = ?, property_country = ?, 
            property_postal_code = ?, property_price_pr_night = ?,
            property_images = ?, property_updated_at = CURRENT_TIMESTAMP
            WHERE property_pk = ?''', 
            (property_name, property_description, 
            property_address, property_country, 
            property_postal_code, property_price_pr_night, 
            combined_images, property_pk))
        db.commit()


        return """
            <template mix-redirect="/profile"></template>
            <template mix-function="closeModal"></template>
        """
    except Exception as ex:
        ic(ex)
    finally:
        pass
        if "db" in locals():
            db.close()

@get('/property/edit-pop-up/<property_pk>')
def _(property_pk):
    try:
        db = x.db()
        q = db.execute("SELECT * FROM properties WHERE property_pk = ?", (property_pk,))
        property_to_edit = q.fetchone();
        property_images = property_to_edit['property_images'].split(',')
        property_image_html = ''
        for property_image in property_images:
            property_image_html += f"""
                <div id="property_image_{property_image.split(".")[0]}" class="relative w-1/3 h-1/3 p-4 flex-shrink-0">
                    <img 
                        src='../images/{property_image}' 
                        alt='property image' 
                        class='property_image w-full aspect-square object-cover rounded-lg'
                    >
                    <form id="remove_image">
                        <button class="absolute top-1 right-1 bg-red-500 h-8 w-8 rounded-full flex items-center justify-center"
                            mix-put="/property/remove_picture/{property_image}/{property_pk}"
                            mix-data="#remove_image"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" class="pointer-events-none" width="30" height="30" fill="#ffffff" class="bi bi-x" viewBox="0 0 16 16">
                                <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
                            </svg>
                        </button>
                    </form>
                </div>
            """
        return f"""
        <template mix-target="#modal_content" mix-replace>
            <div id="modal_content" class="flex flex-col gap-4">
                <div class="flex items-center justify-start h-1/3 gap-6 overflow-y-scroll">
                    {property_image_html}
                </div>
                <form id='edit_property'>
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
                                value="{property_to_edit['property_name']}"
                                mix-check="{html.escape(x.PROPERTY_NAME_REGEX)}"
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
                                value="{property_to_edit['property_description']}"
                                mix-check="{html.escape(x.PROPERTY_DESCRIPTION_REGEX)}"
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
                                value="{property_to_edit['property_address']}"
                                mix-check="{html.escape(x.PROPERTY_ADDRESS_REGEX)}"
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
                                value="{property_to_edit['property_country']}"
                                mix-check="{html.escape(x.PROPERTY_COUNTRY_REGEX)}"
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
                                value="{property_to_edit['property_postal_code']}"
                                mix-check="{html.escape(x.PROPERTY_POSTAL_CODE_REGEX)}"
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
                                value="{property_to_edit['property_price_pr_night']}"
                                mix-check="{html.escape(x.PROPERTY_PRICE_PER_NIGHT_REGEX)}"
                            />
                        </div>
                        <div id="property_error_message"></div>
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
                        <button class="flex items-center justify-center border p-4 bg-green-500 text-white" mix-put="/property/edit/{property_pk}" mix-data="#edit_property">Confirm update</button>
                        <button id="modal_close" class="flex items-center justify-center border p-4">Cancel</button>
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