from oci.response import Response as OCI_Response
import oci
import os
import base64
from zipfile import ZipFile

def stream_file(fname: str, http_response: OCI_Response):
    with open(fname, 'wb') as file:
        for chunk in http_response.data.raw.stream(1024 * 1024, decode_content=False):
            file.write(chunk)

# this function signs into oci and copies in the db wallet
def oci_util():
    key_bytes: bytes = base64.b64decode(os.environ.get("OCI_CLI_KEY_CONTENT"))
    key_content = key_bytes.decode()

    config = {
        "user": os.environ.get("OCI_CLI_USER"),
        "fingerprint": os.environ.get("OCI_CLI_FINGERPRINT"),
        "key_content": key_content,
        "tenancy": os.environ.get("OCI_CLI_TENANCY"),
        "region": os.environ.get("OCI_CLI_REGION")
    }

    client = oci.object_storage.ObjectStorageClient(config)

    response: OCI_Response = client.get_namespace()
    namespace = response.data
    bucket_name = 'sentiments-llm-bucket'
    object_name = 'Wallet-' + os.environ.get("BUILD_ENV") + '.zip'

    response = client.get_object(
        namespace,bucket_name,object_name     
    )

    stream_file(object_name, response)

    wallet = ZipFile(object_name, 'r')
    wallet.extractall(path="Database-Wallet")

    object_name = 'sentiments-llm.pth'

    response = client.get_object(
        namespace,bucket_name,object_name        
    )

    stream_file(object_name, response)

def oci_get_from_bucket(item_name: str):
    key_bytes_encoded = os.environ.get("OCI_CLI_KEY_CONTENT")

    # To help catch the error of not having key content
    if not key_bytes_encoded:
        raise KeyError("Key content not found.")

    key_bytes = base64.b64decode(key_bytes_encoded)
    key_content = key_bytes.decode()

    oci_config_cred = {
        "user": os.environ.get("OCI_CLI_USER"),
        "fingerprint": os.environ.get("OCI_CLI_FINGERPRINT"),
        "key_content": key_content,
        "tenancy": os.environ.get("OCI_CLI_TENANCY"),
        "region": os.environ.get("OCI_CLI_REGION")
    }

    # Checking if the config map is missing anything
    for key in oci_config_cred:
        if not oci_config_cred[key]:
            raise KeyError('Error: Could not find config variable named: '\
                           + key + ' from environment variables.')

    # Making a connection to the oci object storage server
    # TODO: Handle bad client creation to oci
    try:
        oci_object_storage_client = oci.object_storage.ObjectStorageClient(oci_config_cred)
    except Exception as e:
        ...
    
    namespace_response: OCI_Response = oci_object_storage_client.get_namespace()

    # TODO: Handle if namespace response is none
    if namespace_response is None:
        ...

    namespace = namespace_response.data

    bucket_file_response: OCI_Response = oci_object_storage_client.get_object(
        namespace_name=namespace,
        bucket_name='sentiments-llm-bucket',
        object_name=item_name
    )

    # TODO: Handle if object response is none
    if bucket_file_response is None:
        ...
    
    stream_file(fname=item_name, http_response=bucket_file_response)