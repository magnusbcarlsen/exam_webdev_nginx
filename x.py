from bottle import request, response
from icecream import ic
import bcrypt
import os
import re
import json
import sqlite3
import pathlib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

        insert_properties = "INSERT INTO properties(property_pk, property_user_fk, property_booking_fk, property_name, property_description, property_price_pr_night, property_images, property_rating, property_lat, property_lon, property_is_blocked, property_created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
        properties = [('1', '1', '0', 'one', 'one is a house', 1337, 'one.webp', 4.5, 12.5683, 55.6761, '0', 1),
                      ('2', '1', '0', 'two', 'two is a house', 1337, 'two.webp', 4.5, 12.5012, 55.7095, '0', 2),
                      ('3', '1', '0', 'three', 'three is a house', 1337, 'three.webp', 4.5, 10.3869, 55.3967, '0', 3),
                      ('4', '1', '0', 'four', 'four is a house', 1337, 'four.webp', 4.5, 9.9217, 55.4663, '0', 4),
                      ('5', '1', '0', 'five', 'five is a house', 1337, 'five.webp', 4.5, 9.5540, 55.6776, '0', 5),
                      ('6', '1', '0', 'six', 'six is a house', 1337, 'six.webp', 4.5, 8.5100, 55.3911, '0', 6),
                      ('7', '1', '0', 'seven', 'seven is a house', 1337, 'seven.webp', 4.5, 8.4467, 55.4668, '0', 7),
                      ('8', '1', '0', 'eight', 'eight is a house', 1337, 'eight.webp', 4.5, 8.5136, 55.7051, '0', 8),
                      ('9', '1', '0', 'nine', 'nine is a house', 1337, 'nine.webp', 4.5, 9.9716, 55.5863, '0', 9),
                      ('10', '1', '0', 'ten', 'ten is a house', 1337, 'ten.webp', 4.5, 10.4024, 55.4038, '0', 10)]

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

def validate_logged():
    # Prevent logged pages from caching
    response.add_header("Cache-Control", "no-cache, no-store, must-revalidate")
    response.add_header("Pragma", "no-cache")
    response.add_header("Expires", "0")  
    user = request.get_cookie("user", secret = COOKIE_SECRET)
    if not user: raise Exception("***** user not logged *****", 400)
    return user


##############################

def is_cookie_https():
    if 'PYTHONANYWHERE_DOMAIN' in os.environ:
        return True;
    else:
        return False;


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
















