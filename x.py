from bottle import request, response
from icecream import ic
import bcrypt
import os
import re
import json
import sqlite3
import pathlib
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import glob

##############################
def dict_factory(cursor, row):
    col_names = [col[0] for col in cursor.description]
    return {key: value for key, value in zip(col_names, row)}

##############################

def db():
    try:
        db = sqlite3.connect(str(pathlib.Path(__file__).parent.resolve())+"/database/company.db")  
        db.row_factory = dict_factory
        return db
    except Exception as ex:
        return 'server under maintenance'

##############################

def reset_db():
    try:
        database = db()
        database.executescript(
            """
            DROP TABLE IF EXISTS roles;
            CREATE TABLE roles(
                role_pk         TEXT,
                role_name       TEXT,
                PRIMARY KEY(role_pk)
            );

            DROP TABLE IF EXISTS users;
            CREATE TABLE users(
                user_pk             TEXT,
                user_role_fk        TEXT,
                user_username       TEXT,
                user_name           TEXT,
                user_last_name      TEXT,
                user_email          TEXT UNIQUE,
                user_password       TEXT,
                user_is_blocked     TEXT DEFAULT 0,
                user_is_verified    TEXT DEFAULT 0,
                user_created_at     TEXT DEFAULT CURRENT_TIMESTAMP,
                user_updated_at     TEXT DEFAULT CURRENT_TIMESTAMP,
                user_deleted_at     TEXT DEFAULT 0,
                FOREIGN KEY(user_role_fk) REFERENCES roles(role_pk) ON DELETE CASCADE
                PRIMARY KEY(user_pk)
            ) WITHOUT ROWID;

            DROP TABLE IF EXISTS properties;
            CREATE TABLE properties(
                property_pk                 TEXT UNIQUE,
                property_user_fk            TEXT,
                property_booking_fk         TEXT,
                property_name               TEXT,
                property_description        TEXT,
                property_price_pr_night     REAL,
                property_images             TEXT,
                property_rating             REAL,
                property_address            TEXT,
                property_country            TEXT,
                property_postal_code        TEXT,
                property_lat                TEXT,
                property_lon                TEXT,
                property_is_blocked         TEXT,
                property_created_at         INTEGER DEFAULT CURRENT_TIMESTAMP,
                property_updated_at         TEXT DEFAULT CURRENT_TIMESTAMP,
                property_deleted_at         TEXT DEFAULT 0,
                FOREIGN KEY(property_user_fk) REFERENCES users(user_pk) ON DELETE CASCADE,
                PRIMARY KEY(property_pk)
            ) WITHOUT ROWID;

            DROP TABLE IF EXISTS bookings;
            CREATE TABLE bookings(
                booking_pk              TEXT UNIQUE,
                booking_user_fk         TEXT,
                booking_property_fk     TEXT,
                booking_created_at      TEXT DEFAULT CURRENT_TIMESTAMP,
                booking_deleted_at      TEXT DEFAULT 0,
                FOREIGN KEY(booking_user_fk) REFERENCES users(user_pk) ON DELETE CASCADE,
                FOREIGN KEY(booking_property_fk) REFERENCES properties(property_pk) ON DELETE CASCADE,
                PRIMARY KEY(booking_pk)
            ) WITHOUT ROWID;

            CREATE TRIGGER update_property_booking_fk
            AFTER INSERT ON bookings
            FOR EACH ROW
            BEGIN
                UPDATE properties
                SET property_booking_fk = NEW.booking_pk
                WHERE property_pk = NEW.booking_property_fk;
            END;
            """
        )
        database.commit()
    except Exception as ex:
        ic(f"reset db error occurred: {ex}")
    finally:
        if "db" in locals():
            database.close()

##############################

def seed_db():
    try:
        database = db()
        salt = bcrypt.gensalt()
        password = '12345678'.encode()
        user_password_hashed = bcrypt.hashpw(password, salt)

        # Prepare the SQL statements
        insert_roles = "INSERT INTO roles VALUES(?, ?);"
        roles = [('0', 'customer'), ('1', 'partner'), ('2', 'admin')]

        insert_users = "INSERT INTO users(user_pk, user_role_fk, user_username, user_name, user_last_name, user_email, user_password, user_is_verified) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
        users = [('1', '1', 'dirty_ranch', 'ole', 'olesen', 'ole@partner.dk', user_password_hashed, '1'),
                 ('2', '0', 'cowboy', 'anders', 'andersen', 'anders@customer.dk', user_password_hashed, '0'),
                 ('3', '2', 'admin', 'admin', 'adminson', 'admin@company.dk', user_password_hashed, '1')]

        insert_properties = """
        INSERT INTO properties(
            property_pk, property_user_fk, property_booking_fk, property_name,
            property_description, property_price_pr_night, property_images, property_rating, 
            property_address, property_country, property_postal_code, property_lat, 
            property_lon, property_is_blocked)
        VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

        properties = [
            ('1', '1', '0', 'Pretty beach house', 'Nestled along the pristine coastline, the Pretty Beach House offers breathtaking ocean views and serene surroundings. This charming abode features a spacious open-plan living area, tastefully decorated with coastal-inspired furnishings. Guests can enjoy morning coffee on the large deck, take leisurely strolls along the sandy shore, and unwind in the peaceful ambiance of this seaside retreat.', 489, '1.webp,1-1.jpeg,1-2.webp,1-3.jpeg,1-4.webp', 4.5, 'Borgergade 45, Copenhagen', 'Denmark', '1300', 12.5683, 55.6761, '0'),
            ('2', '1', '0', 'Apartment in the Eye of Copenhagen', 'Located in the heart of Copenhagen, this modern apartment provides the perfect urban escape. With sleek, contemporary design and state-of-the-art amenities, the space offers comfort and convenience. Guests are just steps away from world-class dining, shopping, and cultural attractions, making it an ideal base for exploring the vibrant city.', 359, '2.webp,2-1.webp,2-2.webp,2-3.jpeg,2-4.webp', 4.8, 'Algade 23, Aarhus', 'Denmark', '8000', 12.5012, 55.7095, '0'),
            ('3', '1', '0', 'House Down by the Sea', 'The House Down by the Sea is a picturesque seaside home that promises tranquility and relaxation. Featuring spacious interiors, this property boasts large windows that frame stunning sea views. The outdoor area includes a private garden and direct beach access, making it perfect for family gatherings or romantic getaways.', 800, '3.webp,3-1.webp,3-2.jpeg,3-3.jpeg,3-4.jpeg', 4.1, 'Vestergade 7, Odense', 'Denmark', '5000', 10.3869, 55.3967, '0'),
            ('4', '1', '0', 'Cafe Apartment Near Nyhavn', 'This charming apartment, located near the iconic Nyhavn canal, exudes a cozy and inviting atmosphere. The space combines classic Danish design with modern comforts, offering a fully equipped kitchen and comfortable living area. Guests can enjoy the vibrant café culture of Nyhavn, with its colorful buildings and bustling waterfront.', 918, '4.webp,4-1.jpeg,4-2.webp,4-3.webp,4-4.jpeg', 4.2, 'Havnegade 39, Esbjerg', 'Denmark', '6700', 9.9217, 55.4663, '0'),
            ('5', '1', '0', 'Room in Famous Danish Bathing Hotel', 'Experience the charm of a historic Danish bathing hotel with a stay in this beautifully appointed room. The property retains its old-world elegance while providing modern amenities for a comfortable stay. Guests can indulge in spa treatments, savor gourmet dining, and explore the picturesque surroundings.', 479, '5.webp,5-1.webp,5-2.jpeg,5-3.jpeg,5-4.jpeg', 4.6, 'Østergade 21, Aalborg', 'Denmark', '9000', 9.5540, 55.6776, '0'),
            ('6', '1', '0', 'Two Chairs in Little Beach House', 'This quaint little beach house, complete with two comfortable chairs on the porch, is the perfect retreat for couples or solo travelers seeking peace and simplicity. The cozy interiors feature rustic décor and all the essentials for a relaxing stay. Enjoy sunsets from the porch or take a short walk to the nearby beach.', 345, '6.webp,6-1.jpeg,6-2.jpeg,6-3.webp,6-4.jpeg', 4.5, 'Nørregade 30, Randers', 'Denmark', '8900', 8.5100, 55.3911, '0'),
            ('7', '1', '0', 'West-Side Beach House', 'The West-Side Beach House offers a luxurious escape with stunning views of the western coastline. This spacious property features modern architecture, high-end finishes, and ample outdoor space for entertaining. Whether lounging by the private pool or enjoying sunset dinners on the terrace, guests are sure to have an unforgettable stay.', 899, '7.webp,7-1.webp,7-2.webp,7-3.jpeg,7-4.jpeg', 3.9, 'Bredgade 76, Kolding', 'Denmark', '6000', 8.4467, 55.4668, '0'),
            ('8', '1', '0', 'Renovated Apartment Near Amager', 'Situated in the trendy Amager district, this renovated apartment combines style and convenience. The interiors are thoughtfully designed with chic furnishings and modern amenities. Guests can explore nearby parks, visit the bustling local markets, and enjoy the vibrant nightlife of Amager.', 789, '8.webp,8-1.webp,8-2.jpeg,8-3.jpeg,8-4.webp', 2.2, 'Kirkegade 43, Vejle', 'Denmark', '7100', 8.5136, 55.7051, '0'),
            ('9', '1', '0', 'Family Vacation Sea-House', 'Perfect for family vacations, this sea-house offers ample space and a host of amenities for all ages. The property includes multiple bedrooms, a large kitchen, and a cozy living area. Outdoors, guests can enjoy a private garden, play area, and direct access to the beach, making it an ideal spot for fun-filled family holidays.', 239, '9.webp,9-1.jpeg,9-2.jpeg,9-3.webp,9-4.webp', 4.1, 'Park Alle 34, Horsens', 'Denmark', '8700', 9.9716, 55.5863, '0'),
            ('10', '1', '0', 'Lake-Side Home', 'The Lake-Side Home is a tranquil haven set against the backdrop of a serene lake. The property features spacious living areas with panoramic lake views, a well-equipped kitchen, and comfortable bedrooms. Guests can enjoy activities like kayaking, fishing, or simply relaxing by the water, soaking in the natural beauty of the surroundings.', 350, '10.webp,10-1.webp,10-2.jpeg,10-3.jpeg,10-4.jpeg', 4.8, 'Fjordvej 68, Fredericia', 'Denmark', '7000', 10.4024, 55.4038, '0')
        ]

        # Execute the SQL statements
        with database:
            database.executemany(insert_roles, roles)
            database.executemany(insert_users, users)
            database.executemany(insert_properties, properties)

        database.commit()

    except Exception as ex:
        ic(f"seed db error occured: {ex}")
    finally:
        if "db" in locals():
            database.close()

##############################
COOKIE_SECRET = "41ebeca46f3b-4d77-a8e2-554659075C6319a2fbfb-9a2D-4fb6-Afcad32abb26a5e0"
##############################

def create_cookie(name, data):
    response.set_cookie(name, data, secret=COOKIE_SECRET, httponly=True, secure=is_cookie_https())

##############################

def delete_cookie(name):
        response.delete_cookie(name, secret=COOKIE_SECRET)

##############################

def get_cookie_data():
    user_data = request.get_cookie("user", secret=COOKIE_SECRET)
    if user_data is not None:
        return json.loads(user_data)
    else:
        return None

##############################

def validate_user_logged():
    user = request.get_cookie("user", secret=COOKIE_SECRET)
    if user is None: raise Exception("user must login", 400)
    return user

##############################

def is_user_logged_in():
    user = request.get_cookie("user", secret=COOKIE_SECRET)
    if user:
        return True
    else:
        return False

##############################

def is_cookie_https():
    if 'PYTHONANYWHERE_DOMAIN' in os.environ:
        return True;
    else:
        return False;


##############################

def is_on_production():
    if 'PYTHONANYWHERE_DOMAIN' in os.environ:
        return True;
    else:
        return False;

##############################

def get_random_lat_lon_within_copenhagen():
    # Define the approximate borders of Copenhagen
    min_lat, max_lat = 55.6154, 55.7271
    min_lon, max_lon = 12.4534, 12.7343

    # Generate a random latitude and longitude within these borders
    lat = random.uniform(min_lat, max_lat)
    lon = random.uniform(min_lon, max_lon)

    return (lat, lon)

##############################

def delete_all_property_images(property_pk):
    # Get a list of all image files that start with the property_pk
    image_files = glob.glob(f'images/{property_pk}*')
    ic(image_files)
    # Iterate over the list and delete each file using delete_file function
    for image_file in image_files:
        image_file = image_file.split("images/")[1]
        ic('hej fra delete_all: ', image_file)
        delete_file(image_file, 'images/')

##############################

def remove_image_from_property(property_images, image_to_remove):
    # Split the string into a list
    images = property_images.split(',')

    # Remove the image name from the list
    if image_to_remove in images:
        images.remove(image_to_remove)
        delete_file(image_to_remove, 'images/')

    # Join the list back into a string
    new_property_images = ','.join(images)

    return new_property_images

##############################

def delete_file(filename, path):
    # Construct the full path to the file
    file_path = os.path.join(path, filename)
    # Delete the file
    try:
        ic("Removing file at: ", file_path)
        os.remove(file_path)
    except FileNotFoundError:
        print(f"The file {filename} does not exist")

##############################

USER_ID_LEN = 32
USER_ID_REGEX = "^[a-f0-9]{32}$"

def validate_user_id():
	error = f"user_id invalid"
	user_id = request.forms.get("user_id", "").strip()      
	if not re.match(USER_ID_REGEX, user_id): raise Exception(error, 400)
	return user_id


##############################

USER_EMAIL_MAX = 100
USER_EMAIL_REGEX = r"^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"

def validate_user_email():
    error = f"email invalid"
    user_email = request.forms.get("user_email", "").strip()
    if not re.match(USER_EMAIL_REGEX, user_email): raise Exception(error, 400)
    return user_email

##############################

USER_USERNAME_MIN = 2
USER_USERNAME_MAX = 20
USER_USERNAME_REGEX = "^[a-zA-Z0-9_.-]*$"

def validate_user_username():
    error = f"username {USER_USERNAME_MIN} to {USER_USERNAME_MAX} lowercase english letters"
    user_username = request.forms.get("user_username", "").strip()
    if not re.match(USER_USERNAME_REGEX, user_username): raise Exception(error, 400)
    return user_username

##############################

USER_NAME_MIN = 2
USER_NAME_MAX = 20
USER_NAME_REGEX = "^.{2,20}$"
def validate_user_name():
    error = f"name {USER_NAME_MIN} to {USER_NAME_MAX} characters"
    user_name = request.forms.get("user_name", "").strip()
    if not re.match(USER_USERNAME_REGEX, user_name): raise Exception(error, 400)
    return user_name

##############################

USER_LAST_NAME_MIN = 2
USER_LAST_NAME_MAX = 20
USER_LAST_NAME_REGEX = "^.{2,20}$"

def validate_user_last_name():
  error = f"last_name {USER_LAST_NAME_MIN} to {USER_LAST_NAME_MAX} characters"
  user_last_name = request.forms.get("user_last_name").strip()
  if not re.match(USER_USERNAME_REGEX, user_last_name): raise Exception(error, 400)
  return user_last_name

##############################

USER_PASSWORD_MIN = 6
USER_PASSWORD_MAX = 50
USER_PASSWORD_REGEX = "^.{6,50}$"

def validate_user_password():
    error = f"password {USER_PASSWORD_MIN} to {USER_PASSWORD_MAX} characters"
    user_password = request.forms.get("user_password", "").strip()
    if not re.match(USER_PASSWORD_REGEX, user_password): raise Exception(error, 400)
    return user_password

def validate_new_user_password():
        error = f"Password {USER_PASSWORD_MIN} to {USER_PASSWORD_MAX} characters"
        error2 = f"Passwords must match"
        user_new_password = request.forms.get("user_new_password","").strip()
        user_new_password_confirm = request.forms.get("user_new_password_confirm","").strip()
        if not re.match(USER_PASSWORD_REGEX, user_new_password): raise Exception(error, 400)
        if not re.match(USER_PASSWORD_REGEX, user_new_password_confirm): raise Exception(error, 400)
        if not user_new_password == user_new_password_confirm: raise Exception(error2, 400)
        return user_new_password

##############################

USER_ROLE_REGEX = "^[0-1]$"

def validate_user_role():
    user_role = request.forms.get("user_role", "")
    if not re.match(USER_ROLE_REGEX, user_role): raise Exception(400, "Invalid Role")
    return user_role

##############################

PROPERTY_NAME_REGEX = r"^[a-zA-Z0-9 _,.!?'\"-ÆØÅæøå]{3,30}$"

def validate_property_name():
    property_name = request.forms.get("property_name", "")
    if not re.match(PROPERTY_NAME_REGEX, property_name):
        raise Exception(400, "Invalid Property Name")
    return property_name

##############################

PROPERTY_DESCRIPTION_REGEX = r"^[a-zA-Z0-9 _,.!?'\"-ÆØÅæøå]{10,}$"

def validate_property_description():
    property_description = request.forms.get("property_description", "")
    if not re.match(PROPERTY_DESCRIPTION_REGEX, property_description):
        raise Exception(400, "Invalid Property Description")
    return property_description

##############################

PROPERTY_PRICE_PER_NIGHT_REGEX = "^[0-9]+\.?[0-9]*$"

def validate_property_price_pr_night():
    property_price_pr_night = request.forms.get("property_price_pr_night", "")
    if not re.match(PROPERTY_PRICE_PER_NIGHT_REGEX, property_price_pr_night):
        raise Exception(400, "Invalid Property Price Per Night")
    return property_price_pr_night

##############################

PROPERTY_ADDRESS_REGEX = r"^[a-zA-Z0-9\s,.'-ÆØÅæøå]+$"

def validate_property_address():
    property_address = request.forms.get("property_address", "")
    if not re.match(PROPERTY_ADDRESS_REGEX, property_address):
        raise Exception(400, "Invalid Property Address")
    return property_address

##############################

PROPERTY_COUNTRY_REGEX = r"^[a-zA-Z\s]+$"

def validate_property_country():
    property_country = request.forms.get("property_country", "")
    if not re.match(PROPERTY_COUNTRY_REGEX, property_country):
        raise Exception(400, "Invalid Property Country")
    return property_country

##############################

PROPERTY_POSTAL_CODE_REGEX = "^[0-9]{4}$"

def validate_property_postal_code():
    property_postal_code = request.forms.get("property_postal_code", "")
    if not re.match(PROPERTY_POSTAL_CODE_REGEX, property_postal_code):
        raise Exception(400, "Invalid Property Postal Code")
    return property_postal_code

##############################

def validate_added_property_images():
    property_images = request.files.getall('property_images')
    if not property_images:
        raise Exception(400, "No Images Uploaded")
    return property_images

##############################

def validate_edited_property_images():
    property_images = request.files.getall('property_images')
    return property_images

##############################

def confirm_user_password():
  error = f"password and confirm_user_password do not match"
  user_password = request.forms.get("user_password", "").strip()
  user_confirm_password = request.forms.get("user_confirm_password", "").strip()
  if user_password != user_confirm_password: raise Exception(error, 400)
  return user_confirm_password

##############################

def send_mail(to_email, from_email, email_subject, email_body):
    try:
        message = MIMEMultipart()
        message["To"] = to_email
        message["From"] = from_email
        message["Subject"] = email_subject


        messageText = MIMEText(email_body, 'html')
        message.attach(messageText)


        email = 'jachobwesth@gmail.com'
        password = 'xlcsplckzsaeinre'


        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo('Gmail')
        server.starttls()
        server.login(email,password)
        server.sendmail(from_email,to_email,message.as_string())
        server.quit()
    except Exception as ex:
        print(ex)
        return "error"