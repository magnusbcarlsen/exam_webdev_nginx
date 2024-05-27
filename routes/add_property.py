from bottle import get, post, template
from icecream import ic
import uuid
import html
import os
import x

@get('/property/add-pop-up')
def _():
    return f"""
        <template mix-target='#add_property_button' mix-after>
            <div>
                <form
                    id="add_property_form"
                    class="flex flex-col gap-2 w-full"
                >
                    <input
                        id="property_name"
                        name="property_name"
                        class="w-full border"
                        type="text"
                        placeholder="Property name (3 - 30 characters)"
                        mix-check="{html.escape(x.PROPERTY_NAME_REGEX)}"
                    />
                    <input
                        id="property_description"
                        name="property_description"
                        class="w-full border"
                        type="text"
                        placeholder="Property description (min 10 characters)"
                        mix-check="{html.escape(x.PROPERTY_DESCRIPTION_REGEX)}"
                    />
                    <input
                        id="property_address"
                        name="property_address"
                        class="w-full border"
                        type="text"
                        placeholder="property address"
                        mix-check="{html.escape(x.PROPERTY_ADDRESS_REGEX)}"
                    />
                    <input
                        id="property_country"
                        name="property_country"
                        class="w-full border"
                        type="text"
                        placeholder="property country"
                        mix-check="{html.escape(x.PROPERTY_COUNTRY_REGEX)}"
                    />
                    <input
                        id="property_postal_code"
                        name="property_postal_code"
                        class="w-full border"
                        type="text"
                        placeholder="property postal code"
                        mix-check="{html.escape(x.PROPERTY_POSTAL_CODE_REGEX)}"
                    />
                    <input
                        id="property_price_pr_night"
                        name="property_price_pr_night"
                        class="w-full border"
                        type="text"
                        placeholder="property price pr night"
                        mix-check="{html.escape(x.PROPERTY_PRICE_PER_NIGHT_REGEX)}"
                    />
                    <label for="property_images">Property Images (You must select at least 3 images) </label>
                    <input
                        name="property_images"
                        class="file-input"
                        type="file"
                        accept="image/*"
                        multiple
                    />
                    <button
                        id='confirm_add_property'
                        class="w-full bg-accentCol text-white"
                        mix-post="/property"
                        mix-data="#add_property_form"
                    >
                        Add Property
                    </button
                </form>
            </div>
        </template>
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
        property_images = x.validate_property_images()

    
        property_lat, property_lon = x.get_random_lat_lon_within_copenhagen()

        ic("hej")

        if not isinstance(property_images, list) or len(property_images) < 3:
            return f"""
                <template mix-target='#property_error_message' mix-replace>
                    <div>
                        <p>Your property needs at least 3 images</p>
                    </div>
                </template>
            """

        filenames = []
        for image in property_images:
            filename = image.filename
            filenames.append(filename)
            file_path = os.path.join('images', filename)

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
            <template mix-target="#add_property_form" mix-after>
                <p>property has been added!</p>
            </template>
        """
    except Exception as ex:
        ic('- - - - - AN ERROR HAPPENED: ', ex)
    finally:
        if "db" in locals():
            db.close()