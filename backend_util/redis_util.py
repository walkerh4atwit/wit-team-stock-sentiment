from redis import StrictRedis, Redis

def cache_connect(hostname: str, hostport: int) -> StrictRedis:
    client = StrictRedis(host=hostname, port=hostport)

    try: 
        client.ping()
        return client
    except ConnectionError as cerr:
        return None
    except Exception as e:
        return None