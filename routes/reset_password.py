from bottle import post, request, template
from icecream import ic
import x
import bcrypt
import uuid

@post("/reset_password")
def _():
    try:
        user_mail = x.validate_email()
        ic(user_mail)

        # TODO: Send email til provided email
        # Lav link, som peger til ny side med nyt password
        # Den skal kunne finde emailen i db og override det gamle password med det nye
        # Lav password og confirm password

        
    except Exception as ex:
        ic(ex)
        return ex
    finally:
        pass