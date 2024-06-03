from bottle import get, post
from icecream import ic
import uuid
import html
import os
import x

@get('/property/add-pop-up')
def _():
    return f"""
        <template mix-target='#modal_content' mix-replace>
            <div id="modal_content" class="flex flex-col">
                <form
                    id="add_property_form"
                    class="flex flex-col gap-4"
                >
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
                            placeholder="ex. Very cozy house down by the river..."
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
                            placeholder="ex. Street Name 123"
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
                            placeholder="ex. Danmark"
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
                            placeholder="ex. 1234"
                            mix-check="{html.escape(x.PROPERTY_POSTAL_CODE_REGEX)}"
                        />
                    </div>
                    <div class="flex flex-col gap-y-1">
                        <label class="text-dragon-fruit" for="property_price_pr_night">
                                <h2>Property price pr night</h2>
                        </label>
                        <input
                            id="property_price_pr_night"
                            name="property_price_pr_night"
                            class="w-full border"
                            type="text"
                            placeholder="ex. 1234"
                            mix-check="{html.escape(x.PROPERTY_PRICE_PER_NIGHT_REGEX)}"
                        />
                    </div>
                    <div id="property_error_message"></div>
                    <label for="property_images">Property Images (You must select at least 3 images - max 6) </label>
                    <input
                        name="property_images"
                        class="file-input"
                        type="file"
                        accept="image/*"
                        multiple
                    />

                    <div id="modal_buttons" class="flex flex-row gap-4">
                        <button
                            id='confirm_add_property'
                            class="flex items-center justify-center bg-accentCol w-2/3 text-white"
                            mix-post="/property"
                            mix-data="#add_property_form"
                        >
                            Add Property
                        </button>
                        <button id="modal_close" 
                        class="flex items-center justify-center border w-1/3 p-4"
                        >
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </template>
        <template mix-function="showModal"></template>
    """

@post('/property')
def _():
    try:
        random_id = uuid.uuid4().hex
        property_pk = random_id
        user_data = x.get_cookie_data()
        property_name = x.validate_property_name()
        property_description = x.validate_property_description()
        property_address = x.validate_property_address()
        property_country = x.validate_property_country()
        property_postal_code = x.validate_property_postal_code()
        property_price_pr_night = x.validate_property_price_pr_night()
        property_images = x.validate_added_property_images()
        property_lat, property_lon = x.get_random_lat_lon_within_copenhagen()

        if not isinstance(property_images, list) or len(property_images) < 3:
            return f"""
                <template mix-target='#property_error_message' mix-replace>
                    <div id="property_error_message" class="w-full p-2 border border-red-500 bg-pink-100">
                        <p class="text-red-500">Your property needs at least 3 images</p>
                    </div>
                </template>
            """
        
        if not isinstance(property_images, list) or len(property_images) > 6:
            return f"""
                <template mix-target='#property_error_message' mix-replace>
                    <div id="property_error_message" class="w-full p-2 border border-red-500 bg-pink-100">
                        <p class="text-red-500">Too many images! Max 6 images</p>
                    </div>
                </template>
            """

        # Add Property_Pk to the filename
        filenames = []
        for image in property_images:
            filename = property_pk + image.filename
            filenames.append(filename)
            directory_path = 'exam_webdev/images/' if x.is_on_production() else 'images'
            file_path = os.path.join(directory_path, filename)
            if(filename == 'empty'):
                    pass
            else:
                image.save(file_path)

        filenames_str = ",".join(filenames)

        db = x.db()
        q = db.execute("""
            INSERT INTO properties(property_pk, property_user_fk, property_booking_fk, property_name,
            property_description, property_price_pr_night, property_images, property_rating,
            property_address, property_country, property_postal_code, property_lat, 
            property_lon, property_is_blocked) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (property_pk, user_data['user_pk'], '0', property_name, property_description, property_price_pr_night, filenames_str, 4.5, property_address, property_country, property_postal_code, property_lon, property_lat, "0"))
        db.commit()
        
        return """
            <template mix-redirect="/profile"></template>
            <template mix-function="closeModal"></template>
        """
    except Exception as ex:
        ic('- - - - - AN ERROR HAPPENED: ', ex)
    finally:
        if "db" in locals():
            db.close()