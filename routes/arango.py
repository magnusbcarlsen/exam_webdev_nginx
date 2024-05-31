from bottle import delete, get, put, post, request, response
import requests
from icecream import ic
import x

url = 'http://arangodb:8529/_api/cursor'

def execute_query(query):
    body = { "query" : query }
    response = requests.post(url, json = body)

    if response.status_code == 201:
        data = response.json()
        return data
    else:
        raise Exception(f'Request failed with status code: {response.status_code}')
    
    return result
############################################################
def create_item(item_name, item_description):
    query = f"""
        INSERT {{ 'item_name': '{item_name}', 'item_description': '{item_description}' }} INTO items
        RETURN NEW
    """
    return execute_query(query)
############################################################
def get_items():
    query = f"""
            FOR item IN items 
            SORT item._key DESC
            RETURN item
        """
    return execute_query(query)
############################################################
def update_item(key, attribute, new_value):
    query = f"""
        FOR item IN items FILTER item._key == '{key}'
        UPDATE item WITH {{ {attribute}: '{new_value}' }} IN items
        RETURN NEW
    """
    return execute_query(query)
############################################################
def delete_item(key):
    query = f"""
        FOR item in items FILTER item._key == '{key}' 
        REMOVE item IN items
        RETURN OLD
    """
    return execute_query(query)
############################################################
# ROUTES ###################################################
@get("/arango/items")
def _():
    try:
        return get_items()
    except Exception as ex:
        ic(ex)
        return ex
    finally:
        pass

@post("/arango/items")
def _():
    try:
        item_name = request.forms.get("frm_item_name")
        item_description = request.forms.get("frm_item_description")
        
        return create_item(item_name, item_description)
    except Exception as ex:
        ic(ex)
        return ex
    finally:
        pass

@put('/arango/items/item_name/<key>')
def _(key):
    try:
        new_item_name = request.forms.get(f"{key}_frm_item_name")

        return update_item(key, 'item_name', new_item_name)
    except Exception as ex:
        ic(ex)
        return ex
    finally:
        pass

@put('/arango/items/item_description/<key>')
def _(key):
    try:
        new_item_description = request.forms.get(f"{key}_frm_item_description")

        return update_item(key, 'item_description', new_item_description)
    except Exception as ex:
        ic(ex)
        return ex
    finally:
        pass

@delete("/arango/items/<key>")
def _(key):
    try:
        return delete_item(key)
    except Exception as ex:
        ic(ex)
        return ex
    finally:
        pass