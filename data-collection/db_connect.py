import os
import oracledb

def db_connect():
    # pulling env variables
    wallet_path = os.environ.get('DB_WALLET_PATH')
    wallet_pass = os.environ.get('DB_WALLET_PASS')
    db_user = os.environ.get('DB_USER')
    db_pass = os.environ.get('DB_USER_PASS')
    db_dsn_string = os.environ.get('DSN_STRING')

    # some error reporting
    if not wallet_path:
        raise KeyError('Error: Could not find environment variable DB_WALLET_PATH')
    
    if not wallet_pass:
        raise KeyError('Error: Could not find environment variable DB_WALLET_PASS')
    
    if not db_user:
        raise KeyError('Error: Could not find environment variable DB_USER')
    
    if not db_pass:
        raise KeyError('Error: Could not find environment variable DB_USER_PASS')
    
    if not db_dsn_string:
        raise KeyError('Error: Could not find environment variable DSN_STRING')

    connection=oracledb.connect(
        # wallet location for mTLS
        wallet_location=wallet_path,
        # wallet password
        wallet_password=wallet_pass,
        # duplicate below of the path
        config_dir=wallet_path,
        # database username in oci
        user=db_user,
        # the password for that user
        password=db_pass,
        # the dsn string for the database
        dsn=db_dsn_string
    )

    return connection