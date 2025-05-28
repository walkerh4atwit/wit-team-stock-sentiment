from backend_util.db_connect import db_connect
from flask import jsonify, make_response, Response
from redis import StrictRedis

def make_backend_response_cache_hit(func, *args, **kwargs):
    try:
        ...
    except:
        ...
    finally:
        return

# Function to call in all paths to generate a repsonse
def make_backend_response_cache_miss(func, *args, **kwargs):
    response: Response

    try:
        db_cnx = db_connect()

        if 'cnx' not in kwargs:
            kwargs['cnx'] = db_cnx

        data = func(*args, **kwargs)
        data = jsonify(data)

        if not data:
            raise Exception("Uncaught error on backend. No data retrieved!")

        response = make_response(data, 200)

    except KeyError as ke:
        raise ke
    except Exception as e:
        raise e
    # finally:

    return response
    
def cache_query(cache_client: StrictRedis, key: str) -> str | None:
    exists_data_boolean = cache_client.exists(key)
    if not exists_data_boolean:
        return None
    else:
        return cache_client.get(key)