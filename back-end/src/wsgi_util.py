from backend_util.db_connect import db_connect
from flask import jsonify, make_response
from redis import Redis

def make_backend_response_cache_hit(func, *args: list, **kwargs: dict):
    try:
        ...
    except:
        ...
    finally:
        return

# Function to call in all paths to generate a repsonse
def make_backend_response_cache_miss(func, *args: list, **kwargs: dict):
    try:
        db_cnx = db_connect()

        if 'cnx' in kwargs:
            kwargs['cnx'] = db_cnx

        data = func(*args, **kwargs)
        data = jsonify(data)

        if not data:
            raise Exception("Uncaught error on backend. No data retrieved!")

        response = make_response(data, 200)

    except KeyError as ke:
        ...
    except Exception as e:
        ...
    finally:
        return response
    
def cache_query(cache_client: Redis, key: str) -> str | None:
    exists_data_boolean = cache_client.exists(key)
    if not exists_data_boolean:
        return None
    else:
        return cache_client.get(key)