from bottle import delete, get, put, post, request, response
import requests
from icecream import ic
import x

url = 'http://arangodb:8529/_api/'

def execute_query(query):
    body = { "query" : query }
    response = requests.post(url+"cursor", json = body)

    if response.status_code == 201:
        data = response.json()
        return data
    else:
        raise Exception(f'Request failed with status code: {response.status_code}')
    
    return result

# CREATE ####################################################
def create_item(collection, item_dict):
    # List comprehension (Fancy dictionary shortcut)
    item_data = ', '.join([f"'{key}': '{value}'" for key, value in item_dict.items()])
    query = f"""
        INSERT {{ {item_data} }} INTO {collection}
        RETURN NEW
    """
    return execute_query(query)
# READ ######################################################
def get_items(collection):
    query = f"""
            FOR doc IN {collection} 
            SORT doc._key DESC
            RETURN doc
        """
    return execute_query(query)
# UPDATE ####################################################
def update_item(collection, key, new_value):
    query = f"""
        FOR doc IN {collection} FILTER doc._key == '{key}'
        UPDATE doc WITH {new_value}  IN {collection}
        RETURN NEW
    """
    return execute_query(query)
# DELETE ####################################################
def delete_item(collection, key):
    query = f"""
        FOR doc in {collection} FILTER doc._key == '{key}' 
        REMOVE doc IN {collection}
        RETURN OLD
    """
    return execute_query(query)
############################################################
# ROUTES ###################################################
@get("/arango/<collection>")
def _(collection):
    try:
        return get_items(collection)
    except Exception as ex:
        ic(ex)
        return ex
    finally:
        pass

@post("/arango/create_collection/<collection_name>")
def create_collection(collection_name):
    collection_url = url + 'collection'
    body = { "name" : collection_name }
    response = requests.post(collection_url, json = body)

    if response.status_code == 200:
        return f"Collection with name: {collection_name} has been created!"
    else:
        raise Exception(f'Request failed with status code: {response.status_code}')

@post("/arango/<collection>")
def _(collection):
    try:
        document_body = dict(request.forms)
        return create_item(collection, document_body)
    except Exception as ex:
        ic(ex)
        return ex
    finally:
        pass

@put('/arango/<collection>/<key>')
def _(collection, key):
    try:
        document_body = dict(request.forms)
        return update_item(collection, key, document_body)
    except Exception as ex:
        ic(ex)
        return ex
    finally:
        pass

@delete("/arango/delete_collection/<collection_name>")
def delete_collection(collection_name):
    collection_url = url + f'collection/{collection_name}'
    ic(collection_url)
    response = requests.delete(collection_url)

    if response.status_code == 200:
        return f"Collection with name: {collection_name} has been deleted!"
    else:
        raise Exception(f'Request failed with status code: {response.status_code}')

@delete("/arango/<collection>/<key>")
def _(collection, key):
    try:
        return delete_item(collection, key)
    except Exception as ex:
        ic(ex)
        return ex
    finally:
        pass