from bottle import post, request
from icecream import ic
import x

@post("/signup")
def _():
    try:
        # TODO: Get forms data, validate and parse into database
        user_email = x.validate_email()
        user_username = x.validate_user_username()
        user_name = x.validate_user_name()
        user_last_name = x.validate_last_name()
        user_password = x.validate_password()

        

    except Exception as ex:
        ic(ex)
        return ex
    finally:
        pass
